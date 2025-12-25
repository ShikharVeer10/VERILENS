from pydantic import BaseModel
from typing import List

class VerificationIssue(BaseModel):
    check:str
    status:str
    reason:str

class VerificationResult(BaseModel):
    document_type:str
    overall_Status:str
    issues:List[VerificationIssue]
    confidence_score:float