from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os


env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseModel):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL: str = "llama-3.3-70b-versatile"  

    TOP_K: int = 3
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100

settings = Settings()
# API key loaded silently - no print to avoid cluttering output
