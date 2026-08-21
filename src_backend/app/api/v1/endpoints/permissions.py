"""
SK Enterprises | SKAI Safety & Permissions REST Endpoints
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System
"""
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src_backend.app.database.base import get_db
from src_backend.app.services.permission_service import PermissionService
from src_backend.app.services.assistant_service import AssistantService

router = APIRouter(prefix="/permissions", tags=["Safety & Permissions"])

class PolicyUpdateRequest(BaseModel):
    auto_approve_read_only: bool = Field(default=True)
    auto_approve_reversible: bool = Field(default=True)
    require_confirmation_for_destructive: bool = Field(default=True)
    require_confirmation_for_terminal: bool = Field(default=True)
    web_tools_enabled: bool = Field(default=False)
    allowed_directories: List[str] = Field(default_factory=list)

class ConfirmActionRequest(BaseModel):
    action_id: str = Field(..., example="act_9a8b7c6d")
    approved: bool = Field(..., example=True)

@router.get("", summary="Get Current Safety Policies")
def get_permissions_policy():
    return PermissionService.get_policy()

@router.post("", summary="Update Safety Policies")
def update_permissions_policy(req: PolicyUpdateRequest):
    return PermissionService.save_policy(req.model_dump())

@router.get("/pending", summary="List Pending Destructive Confirmation Actions")
def list_pending_actions():
    return {
        "count": len(PermissionService.list_pending_actions()),
        "pending_actions": PermissionService.list_pending_actions()
    }

@router.post("/confirm", summary="Approve or Reject a Pending High-Impact Action")
def confirm_action(req: ConfirmActionRequest, db: Session = Depends(get_db)):
    res = AssistantService.execute_confirmed_action(db, req.action_id, req.approved)
    if not res.get("success") and "not found" in res.get("error", "").lower():
        raise HTTPException(status_code=404, detail=res["error"])
    return res
