from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("verilens")


env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseModel):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    
    # Retrieval settings
    TOP_K: int = 3
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    
    # Retry settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0


settings = Settings()

# Validate API key on startup
if not settings.GROQ_API_KEY:
    logger.warning("GROQ_API_KEY not set. Please add it to your .env file.")
