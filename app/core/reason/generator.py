from openai import OpenAI
from app.core.reason.prompt import SYSTEM_PROMPT
from app.core.core.config import settings


client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_answer(query, chunks):
    context = "\n\n".join(
        f"[{c.source} | chunk {c.chunk_id}]\n{c.text}"
        for c in chunks
    )

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
