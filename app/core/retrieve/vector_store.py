import numpy as np
from typing import List
from app.core.schemas.embedding import EmbeddedChunk

class VectorStore:
    """
    In memory vector store
    """

    def __init__(self):
        self.vectors: List[EmbeddedChunk]=[] #Stores embedded document chunks
    
    def add(self,embedded_chunk:EmbeddedChunk):
        self.vectors.append(embedded_chunk)
    
    def similarity_search(self,query_vector:list[float],top_k:int):
        query=np.array(query_vector)

        scored=[]
        for item in self.vectors:
            vec=np.array(item.embedding)
            score = np.dot(query, vec) / (np.linalg.norm(query) * np.linalg.norm(vec))
            scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in scored[:top_k]]
