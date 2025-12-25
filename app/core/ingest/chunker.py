from typing import List
from app.core.schemas.document import Document, DocumentChunk
from app.core.core.config import settings


def chunk_document(document: Document) -> List[DocumentChunk]:
    chunks = []
    text = document.content

    chunk_size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP
    if overlap >= chunk_size:
        raise ValueError(
            f"Invalid chunk config: CHUNK_OVERLAP ({overlap}) "
            f"must be smaller than CHUNK_SIZE ({chunk_size})"
        )

    start = 0
    chunk_id = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk_text = text[start:end]

        chunks.append(
            DocumentChunk(
                chunk_id=chunk_id,
                text=chunk_text,
                source=document.source
            )
        )

        chunk_id += 1

        start = end - overlap

    return chunks
