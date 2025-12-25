# app/core/ingest/indexer.py
from app.core.retrieve.embedder import embed_texts_batch, add_to_corpus, fit_vectorizer
from app.core.schemas.embedding import EmbeddedChunk


def index_chunks(chunks, vector_store):
    """
    Takes DocumentChunk objects, generates embeddings,
    and stores them in the vector store as EmbeddedChunk objects.
    """
    # Collect all texts for batch processing
    texts = [chunk.text for chunk in chunks]
    
    for text in texts:
        add_to_corpus(text)
    fit_vectorizer()

    # Generate all embeddings in one batch (much faster)
    embeddings = embed_texts_batch(texts)

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunk = EmbeddedChunk(
            chunk_id=chunk.chunk_id,
            text=chunk.text,
            source=chunk.source,
            embedding=embedding
        )
        vector_store.add(embedded_chunk)
