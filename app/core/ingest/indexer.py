from app.core.ingest.loader import load_document
from app.core.ingest.chunker import chunk_document
from app.core.retrieve.embedder import embed_text
from app.core.retrieve.vector_store import VectorStore
from app.core.schemas.embedding import EmbeddedChunk


def build_index() -> VectorStore:
    """
    Builds the vector index by:
    1. Loading documents
    2. Chunking documents
    3. Embedding chunks
    4. Storing embeddings in a VectorStore
    """
    vector_store = VectorStore()
    documents = load_document()

    for document in documents:
        chunks = chunk_document(document)
        for chunk in chunks:
            embedding = embed_text(chunk.text)
            embedded_chunk = EmbeddedChunk(
                chunk_id=chunk.chunk_id,
                text=chunk.text,
                source=chunk.source,
                embedding=embedding
            )
            vector_store.add(embedded_chunk)
    return vector_store