from pydantic import BaseModel

class Document(BaseModel):
    """
    Raw document is loaded from the disk.
    """
    content:str
    source:str

class DocumentChunk(BaseModel):
    """
    Represents a chunk created from the document.
    """
    chunk_id:int
    text:str
    source:str