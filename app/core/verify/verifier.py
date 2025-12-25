"""
Answer Verification Module

This module provides functionality to verify that generated answers
are properly grounded in the source documents.
"""

from typing import List, Optional
from openai import OpenAI
from app.core.core.config import settings
from app.core.verify.base import VerificationIssue, VerificationResult
from app.core.schemas.embedding import EmbeddedChunk


client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

VERIFICATION_PROMPT = """
You are a fact-checking assistant. Your job is to verify if an answer is properly 
supported by the provided evidence chunks.

Analyze the answer and evidence, then provide a verification result.

For each claim in the answer, check if it's supported by the evidence.
Report any issues found.

Respond in the following JSON format:
{
    "document_type": "PDF/Text/Unknown",
    "overall_status": "VERIFIED/PARTIALLY_VERIFIED/NOT_VERIFIED",
    "issues": [
        {
            "check": "description of what was checked",
            "status": "PASS/FAIL/WARNING",
            "reason": "explanation"
        }
    ],
    "confidence_score": 0.0 to 1.0
}
"""


class AnswerVerifier:
    """
    Verifies that generated answers are grounded in source documents.
    """
    
    def __init__(self):
        self.client = client
    
    def verify(
        self, 
        answer: str, 
        evidence_chunks: List[EmbeddedChunk],
        query: str
    ) -> VerificationResult:
        """
        Verify that the answer is properly grounded in the evidence.
        
        Args:
            answer: The generated answer to verify
            evidence_chunks: The document chunks used as evidence
            query: The original query
            
        Returns:
            VerificationResult with status and any issues found
        """
        if not evidence_chunks:
            return VerificationResult(
                document_type="Unknown",
                overall_Status="NOT_VERIFIED",
                issues=[
                    VerificationIssue(
                        check="Evidence availability",
                        status="FAIL",
                        reason="No evidence chunks provided"
                    )
                ],
                confidence_score=0.0
            )
        
        # Build evidence context
        evidence_text = "\n\n".join(
            f"[Chunk {c.chunk_id} from {c.source}]:\n{c.text}"
            for c in evidence_chunks
        )
        
        try:
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": VERIFICATION_PROMPT},
                    {
                        "role": "user",
                        "content": f"""
Query: {query}

Answer to verify:
{answer}

Evidence chunks:
{evidence_text}

Verify if the answer is properly supported by the evidence.
"""
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            import json
            result_data = json.loads(result_text)
            
            issues = [
                VerificationIssue(
                    check=issue.get("check", "Unknown check"),
                    status=issue.get("status", "UNKNOWN"),
                    reason=issue.get("reason", "No reason provided")
                )
                for issue in result_data.get("issues", [])
            ]
            
            return VerificationResult(
                document_type=result_data.get("document_type", "Unknown"),
                overall_Status=result_data.get("overall_status", "NOT_VERIFIED"),
                issues=issues,
                confidence_score=float(result_data.get("confidence_score", 0.0))
            )
            
        except Exception as e:
            return VerificationResult(
                document_type="Unknown",
                overall_Status="ERROR",
                issues=[
                    VerificationIssue(
                        check="Verification process",
                        status="FAIL",
                        reason=f"Verification failed: {str(e)}"
                    )
                ],
                confidence_score=0.0
            )
    
    def quick_verify(
        self, 
        answer: str, 
        evidence_chunks: List[EmbeddedChunk]
    ) -> bool:
        """
        Quick check if answer appears to be grounded in evidence.
        Uses simple keyword matching for fast verification.
        
        Returns:
            True if answer appears grounded, False otherwise
        """
        if not evidence_chunks or not answer:
            return False
        
        # Combine all evidence text
        evidence_text = " ".join(c.text.lower() for c in evidence_chunks)
        
        # Extract key terms from answer (simple approach)
        answer_words = set(answer.lower().split())
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
            'as', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'under', 'again', 'further', 'then', 'once',
            'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either',
            'neither', 'not', 'only', 'own', 'same', 'than', 'too', 'very',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'whom', 'when', 'where',
            'why', 'how', 'all', 'each', 'every', 'any', 'some', 'no',
        }
        
        key_words = answer_words - stop_words
        
        if not key_words:
            return True  # No meaningful words to check
        
        # Check how many key words appear in evidence
        matches = sum(1 for word in key_words if word in evidence_text)
        match_ratio = matches / len(key_words)
        
        # Consider grounded if at least 30% of key words found
        return match_ratio >= 0.3
