"""
SK Enterprises | Cognitive Chat Schemas
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import Optional
from pydantic import BaseModel, Field

class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, example="Explain quantum entanglement")
    persona: str = Field(default="JARVIS", example="JARVIS")
    language: str = Field(default="hi-IN", example="hi-IN")
    user_email: Optional[str] = Field(default="sumeet.admin@skenterprises.ai")

class ChatResponse(BaseModel):
    thought_process: str
    response: str
    voice_text: str
    persona: str = "JARVIS"
    inventor: str = "Sumeet Kumar"
    organization: str = "SK Enterprises"
