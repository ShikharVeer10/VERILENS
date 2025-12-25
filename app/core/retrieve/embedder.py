from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List

_vectorizer = None
_corpus = []

def _get_vectorizer():
    """Get or create the TF-IDF vectorizer"""
    global _vectorizer
    if _vectorizer is None:
        _vectorizer = TfidfVectorizer(
            max_features=512,  
            stop_words='english',
            ngram_range=(1, 2)  
        )
    return _vectorizer

def add_to_corpus(text: str):
    global _corpus
    _corpus.append(text)

def fit_vectorizer():
    """Fit the vectorizer on all collected texts"""
    global _vectorizer, _corpus
    if _corpus:
        _vectorizer = TfidfVectorizer(
            max_features=512,
            stop_words='english',
            ngram_range=(1, 2)
        )
        _vectorizer.fit(_corpus)

def embed_texts_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts in one batch (much faster).
    """
    vectorizer = _get_vectorizer()
    
    try:
        vectors = vectorizer.transform(texts).toarray()
        return [v.tolist() for v in vectors]
    except Exception:
        # Fallback for each text
        result = []
        for text in texts:
            np.random.seed(hash(text) % (2**32))
            result.append(np.random.rand(512).tolist())
        return result

def embed_text(text: str) -> list[float]:
    """
    Generate an embedding for text using TF-IDF.
    Falls back to simple vector if vectorizer not fitted.
    """
    vectorizer = _get_vectorizer()
    
    try:
        vector = vectorizer.transform([text]).toarray()[0]
        return vector.tolist()
    except Exception:
        np.random.seed(hash(text) % (2**32))
        return np.random.rand(512).tolist()