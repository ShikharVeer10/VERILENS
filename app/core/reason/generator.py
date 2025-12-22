import json
import requests
from pydantic import ValidationError

from app.core.core.config import settings
from app.core.schemas.response import VerifiedAnswer
from app.core.reason.prompt import SYSTEM_PROMPT


def generate_verified_answer(query: str, chunks) -> VerifiedAnswer:
    """
    Generate a verification-first answer using Grok (xAI).
    """

    context = "\n\n".join(
        f"[SOURCE: {c.source} | CHUNK_ID: {c.chunk_id}]\n{c.text}"
        for c in chunks
    )

    user_prompt = f"""
Context:
{context}

Question:
{query}

Instructions:
- Use ONLY the context above
- Do NOT hallucinate
- Output STRICT JSON
- Follow this schema:

{{
  "answer": "<string>",
  "evidence": [
    {{
      "source": "<string>",
      "chunk_id": <int>,
      "text": "<string>"
    }}
  ]
}}
"""

    payload = {
        "model": settings.GROK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0
    }

    headers = {
        "Authorization": f"Bearer {settings.GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    raw_output = response.json()["choices"][0]["message"]["content"]

    try:
        parsed = json.loads(raw_output)
        return VerifiedAnswer(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError("Grok output failed verification") from e
