import time
from typing import List
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from app.core.reason.prompt import SYSTEM_PROMPT
from app.core.core.config import settings, logger
from app.core.schemas.embedding import EmbeddedChunk


client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def generate_answer(
    query: str, 
    chunks: List[EmbeddedChunk],
    max_retries: int = None
) -> str:
    """
    Generate an answer using the LLM with automatic retries.
    
    Args:
        query: The user's question
        chunks: Retrieved document chunks for context
        max_retries: Maximum retry attempts (defaults to settings.MAX_RETRIES)
        
    Returns:
        Generated answer string
        
    Raises:
        Exception: If all retry attempts fail
    """
    if max_retries is None:
        max_retries = settings.MAX_RETRIES
        
    context = "\n\n".join(
        f"[{c.source} | chunk {c.chunk_id}]\n{c.text}"
        for c in chunks
    )
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion:\n{query}"
                    }
                ]
            )
            return response.choices[0].message.content
            
        except RateLimitError as e:
            last_error = e
            wait_time = settings.RETRY_DELAY * (2 ** attempt)  # Exponential backoff
            logger.warning(f"Rate limited. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
            
        except APIConnectionError as e:
            last_error = e
            wait_time = settings.RETRY_DELAY * (2 ** attempt)
            logger.warning(f"Connection error. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
            
        except APIError as e:
            last_error = e
            logger.error(f"API error: {e}")
            if attempt < max_retries - 1:
                time.sleep(settings.RETRY_DELAY)
            else:
                break
    
    logger.error(f"Failed after {max_retries} attempts: {last_error}")
    raise Exception(f"Failed to generate answer after {max_retries} attempts: {last_error}")
