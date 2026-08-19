"""
SK Enterprises | Universal STEM & Education Schemas
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EducationTestRequest(BaseModel):
    subject: str = Field(default="Physics", example="Physics")
    standard: str = Field(default="Class 12", example="Class 12")
    difficulty: str = Field(default="Hard", example="Hard")
    topic: Optional[str] = Field(default="Electrodynamics & Quantum Mechanics")

class EducationLectureRequest(BaseModel):
    topic: str = Field(default="Quantum Mechanics & Schrödinger Wave Equations")

class AssessmentSection(BaseModel):
    section: str
    questions_count: int
    marks_per_question: int
    sample_question: str

class EducationTestResponse(BaseModel):
    title: str
    curriculum: str
    difficulty: str
    total_marks: int
    duration_minutes: int
    architect: str
    sections: List[AssessmentSection]
