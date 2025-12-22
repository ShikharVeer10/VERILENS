from typing import List
from app.core.schemas.document import Document,DocumentChunk
from app.core.core.config import settings

def chunk_document(document:Document) ->List[DocumentChunk]:
    chunks=[]
    start=0
    chunk_id=0
    text=document.content

    while start<len(text):
        end=start+settings.CHUNK_SIZE
        chunk_text=text[start:end]

        chunks.append(
            DocumentChunk(
                chunk_id=chunk_id,
                text=chunk_text,
                source=document.source
            )
        )

        chunk_id += 1
        start = end - settings.CHUNK_OVERLAP

    return chunks

