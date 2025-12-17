from pathlib import Path
from typing import List
from app.core.schemas.document import Document

DOCUMENT_PATHS=Path("data/documents")

def load_document()->List[Document]:
    documents=[]

    for file in DOCUMENT_PATHS.glob("*.txt"):
        documents.append(
            Document(
                content=file.read_text(encoding="UTF-8"),
                source=file.name
            )
        )

    return documents


