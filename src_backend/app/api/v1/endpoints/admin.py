"""
SK Enterprises | Super Admin & Licensing Endpoints
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src_backend.app.database.base import get_db
from src_backend.app.schemas.admin import OnboardPayload, ToggleUserPayload, LicensePayload
from src_backend.app.services.admin_service import AdminService

router = APIRouter(tags=["Super Admin & Licensing"])

@router.post("/admin/onboard_client", summary="Register and Onboard New Client")
def onboard_client(p: OnboardPayload, db: Session = Depends(get_db)):
    return AdminService.onboard_client(db, p.name, p.age, p.location, p.email, p.phone)

@router.post("/admin/generate_license", summary="Generate Cryptographic License Key")
def generate_license(
    name: str = Query(..., example="Sumeet Kumar"),
    email: str = Query(..., example="sumeet.admin@skenterprises.ai"),
    tier: str = Query(default="USER_ANNUAL_365", example="USER_ANNUAL_365")
):
    return AdminService.generate_license(name, email, tier)

@router.post("/admin/toggle_user", summary="Toggle Client Active Status / Remote Killswitch")
def toggle_user(p: ToggleUserPayload, db: Session = Depends(get_db)):
    return AdminService.toggle_user_status(db, p.email, p.active)

@router.post("/admin/dispatch_whatsapp", summary="Create WhatsApp Dispatch Link")
def dispatch_whatsapp(
    phone: str = Query(..., example="+919153579997"),
    name: str = Query(..., example="Sumeet Kumar"),
    link: str = Query(..., example="https://skenterprises.ai/installer")
):
    from src_backend.super_admin_hub import SuperAdminHub
    return SuperAdminHub.dispatch_whatsapp_installer(phone, name, link)

@router.post("/license/validate", summary="Cryptographically Validate Any License Token")
def validate_license(p: LicensePayload):
    res = AdminService.validate_license(p.token)
    if not res.get("valid"):
        raise HTTPException(status_code=403, detail=res.get("error", "Invalid or expired license key"))
    return res

@router.get("/admin/clients", summary="List All Registered Clients")
def list_clients(db: Session = Depends(get_db)):
    return AdminService.list_clients(db)
