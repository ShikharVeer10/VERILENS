from pydantic import BaseModel
from typing import List

class Evidence(BaseModel):
    source:str
    chunk_id:int
    text:str

class VerifiedAnswer(BaseModel):
    answer:str
    evidence:List[Evidence]