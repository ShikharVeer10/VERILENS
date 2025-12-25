# Retrieval module for embeddings and vector search
from .embedder import embed_text, add_to_corpus, fit_vectorizer
from .vector_store import VectorStore
from .retriever import retrieve_relevant_chunks

__all__ = ["embed_text", "add_to_corpus", "fit_vectorizer", "VectorStore", "retrieve_relevant_chunks"]
