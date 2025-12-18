from openai import OpenAI
from app.core.schemas.response import VerifiedAnswer,Evidence #Used for evidence tracking and verification of answer
from app.core.reason.prompt import SYSTEM_PROMPT #Controls tone, rules
from app.core.config import settings

client=OpenAI(api_key=settings.OPENAI_API_KEY) #Initializing OpenAI key

def generate_verifiable_answer(query:str,chunks):
    """
    Generate a verified evidential answer
    """
    context="\n\n".join(
        f"[{c.source} | chunk {c.chunk_id}]\n{c.text}"
        for c in chunks
    )

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
        ]
    )

    return response.choices[0].message.content
