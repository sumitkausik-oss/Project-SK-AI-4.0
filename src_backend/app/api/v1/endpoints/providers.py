"""
SK Enterprises | AI Provider Management Endpoints
Founder & Sole Architect: Sumeet Kumar
Platform: Jarvis Platform V5.0
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src_backend.app.services.provider_service import ProviderService

router = APIRouter(prefix="/providers", tags=["AI Provider Gateway"])

class ProviderToggleRequest(BaseModel):
    enabled: bool

@router.get("", summary="List Configured AI Providers")
def list_providers():
    return ProviderService.list_providers()

@router.post("/{provider_id}/test", summary="Test AI Provider Connection")
def test_provider(provider_id: str):
    res = ProviderService.test_provider_connection(provider_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@router.post("/{provider_id}/toggle", summary="Enable / Disable AI Provider")
def toggle_provider(provider_id: str, req: ProviderToggleRequest):
    res = ProviderService.toggle_provider(provider_id, req.enabled)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res
