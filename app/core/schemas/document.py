from pydantic import BaseModel

class Document(BaseModel):
    content:str
    source:str

class DocumentChunk(BaseModel):
    chunk_id:int
    text:str
    source:str