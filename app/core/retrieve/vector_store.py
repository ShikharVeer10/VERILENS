import numpy as np
import pickle
from pathlib import Path
from typing import List, Optional
from app.core.schemas.embedding import EmbeddedChunk
from app.core.core.config import logger


class VectorStore:
    """
    In-memory vector store with persistence support.
    
    Stores embedded document chunks and provides similarity search.
    Can save/load state to disk for caching.
    """
    
    def __init__(self):
        self.vectors: List[EmbeddedChunk] = []
        self._source_file: Optional[str] = None
    
    def add(self, embedded_chunk: EmbeddedChunk):
        """Add an embedded chunk to the store."""
        self.vectors.append(embedded_chunk)
    
    def clear(self):
        """Clear all vectors from the store."""
        self.vectors = []
        self._source_file = None
    
    def __len__(self) -> int:
        """Return the number of chunks in the store."""
        return len(self.vectors)
    
    def similarity_search(self, query_vector: List[float], top_k: int) -> List[EmbeddedChunk]:
        """
        Find the top-k most similar chunks to the query vector.
        
        Args:
            query_vector: The query embedding
            top_k: Number of results to return
            
        Returns:
            List of most similar EmbeddedChunks
        """
        if not self.vectors:
            return []
            
        query = np.array(query_vector)
        query_norm = np.linalg.norm(query)

        scored = []
        for item in self.vectors:
            vec = np.array(item.embedding)
            vec_norm = np.linalg.norm(vec)
            
            # Avoid division by zero
            if query_norm == 0 or vec_norm == 0:
                score = 0.0
            else:
                score = np.dot(query, vec) / (query_norm * vec_norm)
            scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in scored[:top_k]]
    
    def save(self, path: str) -> bool:
        """
        Save the vector store to disk.
        
        Args:
            path: File path to save to (will use .pkl extension)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            save_path = Path(path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                pickle.dump({
                    'vectors': self.vectors,
                    'source_file': self._source_file
                }, f)
            
            logger.info(f"Vector store saved to {save_path} ({len(self.vectors)} chunks)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save vector store: {e}")
            return False
    
    def load(self, path: str) -> bool:
        """
        Load the vector store from disk.
        
        Args:
            path: File path to load from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            load_path = Path(path)
            
            if not load_path.exists():
                logger.warning(f"Vector store file not found: {load_path}")
                return False
            
            with open(load_path, 'rb') as f:
                data = pickle.load(f)
            
            self.vectors = data.get('vectors', [])
            self._source_file = data.get('source_file')
            
            logger.info(f"Vector store loaded from {load_path} ({len(self.vectors)} chunks)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            return False
    
    @staticmethod
    def get_cache_path(source_file: str, cache_dir: str = ".verilens_cache") -> str:
        """
        Generate a cache file path for a source document.
        
        Args:
            source_file: Original document filename
            cache_dir: Directory for cache files
            
        Returns:
            Path string for the cache file
        """
        import hashlib
        file_hash = hashlib.md5(source_file.encode()).hexdigest()[:8]
        safe_name = Path(source_file).stem
        return str(Path(cache_dir) / f"{safe_name}_{file_hash}.pkl")
