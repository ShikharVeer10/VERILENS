from app.core.retrieve.retriever import retrieve_relevant_chunks

def retrieval_tool(query:str,vector_store):
    """
    Tool used by the agent to retrieve evidence.
    """
    return retrieve_relevant_chunks(query, vector_store)