from openai import OpenAI
from app.core.core.config import settings

client=OpenAI(api_key=settings.OPENAI_API_KEY)

def embed_text(text:str)->list[float]:
    """
    Generating a embedding for a piece of text
    """

    response=client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding