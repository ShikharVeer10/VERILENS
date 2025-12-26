from typing import Optional, Tuple, List
from app.core.retrieve.retriever import retrieve_relevant_chunks
from app.core.reason.generator import generate_answer
from app.core.verify.verifier import AnswerVerifier
from app.core.schemas.embedding import EmbeddedChunk


class VeriLensAgent:
    """
    Main agent for document Q&A with verification capabilities.
    
    The agent retrieves relevant document chunks, generates answers,
    and optionally verifies that answers are grounded in evidence.
    """
    
    def __init__(self, vector_store, enable_verification: bool = False):
        """
        Initialize the VeriLens agent.
        
        Args:
            vector_store: The vector store containing document embeddings
            enable_verification: Whether to verify answers (slower but more reliable)
        """
        self.vector_store = vector_store
        self.enable_verification = enable_verification
        self.verifier = AnswerVerifier() if enable_verification else None
        self._last_chunks: List[EmbeddedChunk] = []
    
    def answer(self, query: str) -> str:
        """
        Generate an answer for the given query.
        
        Args:
            query: The user's question
            
        Returns:
            The generated answer with citations
        """
        self._last_chunks = retrieve_relevant_chunks(query, self.vector_store)
        
        if not self._last_chunks:
            return "I could not find any relevant information in the document to answer your question."

        answer = generate_answer(query, self._last_chunks)

        if self.enable_verification and self.verifier:
            verification = self.verifier.verify(answer, self._last_chunks, query)
            if verification.overall_status == "NOT_VERIFIED":
                answer += f"\n\n⚠️ VERIFICATION WARNING: This answer may not be fully grounded in the document. Confidence: {verification.confidence_score:.0%}"
            elif verification.overall_status == "PARTIALLY_VERIFIED":
                answer += f"\n\n📝 Note: Some claims could not be fully verified. Confidence: {verification.confidence_score:.0%}"
        
        return answer
    
    def answer_with_sources(self, query: str) -> Tuple[str, List[EmbeddedChunk]]:
        answer = self.answer(query)
        return answer, self._last_chunks
    
    def get_relevant_chunks(self, query: str, top_k: Optional[int] = None) -> List[EmbeddedChunk]:
        return retrieve_relevant_chunks(query, self.vector_store)
