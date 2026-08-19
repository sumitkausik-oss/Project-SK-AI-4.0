"""
SK Enterprises | Cloud DevOps & Admin Schemas
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class CloudTaskRequest(BaseModel):
    action: str = Field(default="ENFORCE_MFA_CONDITIONAL_ACCESS", example="ENFORCE_MFA_CONDITIONAL_ACCESS")
    target_user: Optional[str] = Field(default="admin@skenterprises.org")

class CloudTaskResponse(BaseModel):
    action: str
    target: Optional[str]
    compliance: str
    google_workspace_status: str
    microsoft_365_status: str
    audit_log: str
    timestamp: str

class OnboardPayload(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=30)
    location: str = Field(..., example="Delhi")
    email: str = Field(..., example="john@example.com")
    phone: Optional[str] = Field(default="+919153579997")

class ToggleUserPayload(BaseModel):
    email: str = Field(..., example="john@example.com")
    active: bool = Field(..., example=True)

class LicensePayload(BaseModel):
    token: str = Field(..., example="SK_AI_4_KEY_...")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    role: str
    tier: str
    status: str
    created_at: Optional[str]
