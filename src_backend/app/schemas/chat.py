"""
SK Enterprises | SKAI Cognitive Chat & Command Schemas
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, example="open notepad")
    persona: str = Field(default="SKAI", example="SKAI")
    language: str = Field(default="en-US", example="en-US")
    user_email: Optional[str] = Field(default="sumeet.admin@skenterprises.ai")

class ChatResponse(BaseModel):
    status: Optional[str] = Field(default="COMPLETED")
    action: Optional[str] = Field(default=None)
    action_id: Optional[str] = Field(default=None)
    requires_confirmation: Optional[bool] = Field(default=False)
    category: Optional[str] = Field(default=None)
    params: Optional[Dict[str, Any]] = Field(default=None)
    result: Optional[Dict[str, Any]] = Field(default=None)
    thought_process: str
    response: str
    voice_text: str
    persona: str = "SKAI"
    inventor: str = "Sumeet Kumar"
    organization: str = "SK Enterprises"
