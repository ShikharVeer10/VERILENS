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
        query_norm = np.linalg.norm(query)

        scored=[]
        for item in self.vectors:
            vec=np.array(item.embedding)
            vec_norm = np.linalg.norm(vec)
            
            # Avoid division by zero - if either norm is zero, similarity is 0
            if query_norm == 0 or vec_norm == 0:
                score = 0.0
            else:
                score = np.dot(query, vec) / (query_norm * vec_norm)
            scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in scored[:top_k]]
