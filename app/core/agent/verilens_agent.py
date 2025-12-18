from app.core.agent.tools import retrieval_tool
from app.core.reason.generator import generate_verified_answer

class VeriLensAgent:
    """
    Orchestrates retrieval + reasoning.
    """

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def answer(self, query: str):
        chunks = retrieval_tool(query, self.vector_store)
        return generate_verified_answer(query, chunks)
