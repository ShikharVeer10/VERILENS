from pydantic import BaseModel
from typing import List

class EmbeddedChunk(BaseModel):
    chunk_id:int
    text:str
    source:str
    embedding:List[float]