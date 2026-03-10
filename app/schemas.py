from pydantic import BaseModel
from typing import List


class AnalysisResponse(BaseModel):
    """Response model for PDF analysis"""
    summary: str
    key_points: List[str]
    success: bool
    message: str = ""


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    message: str
