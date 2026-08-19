"""
SK Enterprises | Super Admin & Client Licensing Service
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from src_backend.app.repositories.user_repo import UserRepository
from src_backend.app.repositories.memory_repo import AuditRepository
from src_backend.super_admin_hub import SuperAdminHub
from src_backend.key_generator_master import MasterKeyGenerator

class AdminService:
    @staticmethod
    def onboard_client(db: Session, name: str, age: int, location: str, email: str, phone: Optional[str] = None) -> Dict[str, Any]:
        # 1. Register in file-based storage registry (backward compatibility)
        reg_res = SuperAdminHub.register_user(name, email, phone or "")
        
        # 2. Persist in SQLite database
        existing = UserRepository.get_by_email(db, email)
        if not existing:
            UserRepository.create(
                db=db,
                name=name,
                email=email,
                phone=phone,
                location=location,
                age=age,
                role="USER",
                tier="USER_ANNUAL_365"
            )
            
        AuditRepository.log_event(
            db=db,
            event_type="CLIENT_ONBOARD",
            description=f"Client onboarded: {name} ({email})",
            severity="INFO",
            actor="SUPER_ADMIN"
        )
        return reg_res

    @staticmethod
    def generate_license(name: str, email: str, tier: str = "USER_ANNUAL_365", phone: str = "") -> Dict[str, Any]:
        if "ADMIN" in tier.upper() or "LIFETIME" in tier.upper():
            return MasterKeyGenerator.generate_admin_lifetime_key(name, email)
        return MasterKeyGenerator.generate_user_annual_key(name, email, phone)

    @staticmethod
    def validate_license(token: str) -> Dict[str, Any]:
        return MasterKeyGenerator.validate_any_key(token)

    @staticmethod
    def toggle_user_status(db: Session, email: str, is_active: bool) -> Dict[str, Any]:
        status_str = "ACTIVE" if is_active else "DISABLED"
        SuperAdminHub.set_user_status(email, status_str)
        UserRepository.update_status(db, email, is_active)
        AuditRepository.log_event(
            db=db,
            event_type="USER_STATUS_TOGGLE",
            description=f"User {email} status changed to {status_str}",
            severity="WARNING",
            actor="SUPER_ADMIN"
        )
        return {"success": True, "email": email, "status": status_str}

    @staticmethod
    def list_clients(db: Session) -> List[Dict[str, Any]]:
        users = UserRepository.list_all(db)
        return [u.to_dict() for u in users]
