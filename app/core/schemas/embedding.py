from pydantic import BaseModel
from typing import List

class EmbeddedChunk(BaseModel):
    """
    A document chunk + its vector embedding:
    """
    chunk_id:int
    text:str
    source:str
    embedding:List[float]