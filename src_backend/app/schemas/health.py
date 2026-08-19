"""
SK Enterprises | Health & Liveness Schemas
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(..., example="HEALTHY")
    version: str = Field(..., example="5.0.0")
    timestamp: str
    uptime_seconds: float
    system: str = "SK AI 4.0"
    inventor: str = "Sumeet Kumar"

class ReadinessResponse(BaseModel):
    status: str = Field(..., example="READY")
    database: str = Field(..., example="CONNECTED")
    version: str = "5.0.0"
    active_nodes: int = 4
    lifetime_license: str = "ACTIVE - VERIFIED"
    timestamp: str
