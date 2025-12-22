from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseModel):
    # Embeddings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Grok (xAI)
    GROK_API_KEY: str = os.getenv("GROK_API_KEY")
    GROK_MODEL: str = "grok-2-latest"

    # RAG config
    TOP_K: int = 3
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100

settings = Settings()
print("API KEY LOADED:", settings.OPENAI_API_KEY[:10])
