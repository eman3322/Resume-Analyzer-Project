from pydantic import BaseModel
from typing import List


class AnalyzeResponse(BaseModel):
    match_score: int
    ats_score: int
    missing_keywords: List[str]
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    resume_text: str = ""


class RewriteRequest(BaseModel):
    bullet: str
    job_description: str = ""


class RewriteResponse(BaseModel):
    original: str
    improved: str


class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description: str
    tone: str = "professional"


class CoverLetterResponse(BaseModel):
    cover_letter: str


class InterviewRequest(BaseModel):
    resume_text: str
    job_description: str


class InterviewResponse(BaseModel):
    technical: List[str]
    behavioral: List[str]