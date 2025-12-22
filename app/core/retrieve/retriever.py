from app.core.retrieve.embedder import embed_text #Converts raw text to embedded text
from app.core.retrieve.vector_store import VectorStore 
from app.core.core.config import settings #It takes TOP_K as to see how many chunks are retrieved

def retrieve_relevant_chunks(
        query:str, #The user question
        vector_store:VectorStore
):
    
    query_embedding=embed_text(query)
    return vector_store.similarity_search(
        query_embedding,
        settings.TOP_K
    )
