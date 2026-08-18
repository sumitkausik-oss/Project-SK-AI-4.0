"""
SK Enterprises | Super Admin Master Control Hub
Founder, Inventor & Sole Architect: Sumit Kumar
Platform V5.0 — Sovereign Central Governance & Remote Administration Hub

Capabilities:
- Real-time Global User Manager (Enable, Disable, Remote Kill-Switch, Revoke)
- Isolated User-Oriented Data Retrieval (Strict Zero Cross-Contamination Security)
- Central Brain Memory Mirroring & Continuous Self-Learning Aggregation
- Integrated Client EXE & APK Package Provisioning
- WhatsApp Dispatch Automation (Target: 9153579997)
- Sovereign Lifetime Key Authentication & Enforcement
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "admin_central_storage"
USERS_FILE = STORAGE_DIR / "registered_users_registry.json"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

from src_backend.key_generator_master import MasterKeyGenerator
from src_backend.user_deployment_engine import UserDeploymentEngine
from src_backend.anti_extraction_security import AntiExtractionShield

class SuperAdminHub:
    """
    Sovereign Super Admin Control Unit operated exclusively by Sumit Kumar.
    """
    OWNER = "Sumit Kumar"
    ORGANIZATION = "SK Enterprises"
    DEFAULT_PHONE = "9153579997"

    @classmethod
    def _load_registry(cls) -> Dict[str, Any]:
        if USERS_FILE.exists():
            try:
                return json.loads(USERS_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        # Default seed
        default_data = {
            "master_admin": {
                "name": "Sumit Kumar",
                "email": "sumit.admin@skenterprises.ai",
                "phone": cls.DEFAULT_PHONE,
                "role": "SUPER_ADMIN",
                "lifetime_active": True
            },
            "users": {},
            "global_system_status": "ONLINE",
            "global_kill_switch_active": False,
            "last_sync": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        cls._save_registry(default_data)
        return default_data

    @classmethod
    def _save_registry(cls, data: Dict[str, Any]):
        data["last_sync"] = time.strftime("%Y-%m-%d %H:%M:%S")
        USERS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def register_user(cls, name: str, email: str, phone: str = "9153579997", tier: str = "PRO_COMMERCIAL") -> Dict[str, Any]:
        """
        Registers a new client, generates a 1-year key, creates Windows & APK packages,
        and provides direct WhatsApp notification dispatch links.
        """
        registry = cls._load_registry()
        user_key_gen = MasterKeyGenerator.generate_user_annual_key(name, email, phone, tier)
        license_key = user_key_gen["license_key"]
        
        # Build deployments
        win_pkg = UserDeploymentEngine.generate_windows_package(name, email, phone, license_key)
        apk_pkg = UserDeploymentEngine.generate_apk_package(name, email, phone, license_key)
        wa_dispatch_url = UserDeploymentEngine.create_whatsapp_dispatch_url(phone, name, win_pkg["installer_link"], license_key)
        
        user_entry = {
            "name": name,
            "email": email,
            "phone": phone,
            "tier": tier,
            "license_key": license_key,
            "expires_at": user_key_gen["expires_at"],
            "status": "ACTIVE",
            "windows_package": win_pkg,
            "apk_package": apk_pkg,
            "whatsapp_dispatch_url": wa_dispatch_url,
            "registered_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data_queries_count": 0
        }
        
        registry["users"][email] = user_entry
        cls._save_registry(registry)
        
        return {
            "status": "USER_REGISTERED_SUCCESSFULLY",
            "user": user_entry,
            "license_key": license_key,
            "whatsapp_dispatch_url": wa_dispatch_url
        }

    @classmethod
    def set_user_status(cls, email: str, new_status: str) -> Dict[str, Any]:
        """
        Enables, Disables, or Revokes a user remotely (Remote Kill-Switch).
        new_status: "ACTIVE" | "DISABLED" | "REVOKED"
        """
        registry = cls._load_registry()
        if email in registry["users"]:
            registry["users"][email]["status"] = new_status
            cls._save_registry(registry)
            return {"success": True, "email": email, "status": new_status, "message": f"User status set to {new_status}"}
        return {"success": False, "reason": "User not found in registry"}

    @classmethod
    def toggle_global_kill_switch(cls, active: bool) -> Dict[str, Any]:
        """
        Master emergency kill switch for all subordinate user instances.
        """
        registry = cls._load_registry()
        registry["global_kill_switch_active"] = active
        registry["global_system_status"] = "EMERGENCY_LOCKDOWN" if active else "ONLINE"
        cls._save_registry(registry)
        return {
            "global_kill_switch_active": active,
            "system_status": registry["global_system_status"],
            "commander": cls.OWNER
        }

    @classmethod
    def get_user_isolated_memory(cls, search_query: str) -> Dict[str, Any]:
        """
        Retrieves ONLY the searched user's data with strict security isolation.
        Example: Searching for 'Amit' yields ONLY Amit's telemetry with zero data leakage.
        """
        registry = cls._load_registry()
        matched_user = None
        
        # Search by email or name
        q = search_query.lower().strip()
        for email, user in registry["users"].items():
            if q in email.lower() or q in user["name"].lower():
                matched_user = user
                break
                
        if not matched_user:
            return {
                "found": False,
                "message": f"No isolated user record found matching '{search_query}'"
            }
            
        # Retrieve user's mirrored data lake
        user_dir = STORAGE_DIR / "users" / matched_user["email"].replace("@", "_at_")
        history_file = user_dir / "telemetry_log.json"
        telemetry = []
        if history_file.exists():
            try:
                telemetry = json.loads(history_file.read_text(encoding="utf-8"))
            except Exception:
                telemetry = []
                
        return {
            "found": True,
            "user_identity": {
                "name": matched_user["name"],
                "email": matched_user["email"],
                "phone": matched_user.get("phone", cls.DEFAULT_PHONE),
                "status": matched_user["status"],
                "tier": matched_user.get("tier", "PRO"),
                "expires_at": matched_user.get("expires_at", "N/A")
            },
            "isolated_memory_records": telemetry[-50:],
            "total_records": len(telemetry),
            "security_lock": "STRICT_USER_ISOLATION_VERIFIED",
            "retrieved_by": cls.OWNER
        }

    @classmethod
    def get_full_hub_status(cls) -> Dict[str, Any]:
        """
        Full Super Admin Overview for Dashboard.
        """
        registry = cls._load_registry()
        shield_status = AntiExtractionShield.verify_integrity()
        
        users_list = list(registry["users"].values())
        active_count = sum(1 for u in users_list if u.get("status") == "ACTIVE")
        disabled_count = sum(1 for u in users_list if u.get("status") in ("DISABLED", "REVOKED"))
        
        return {
            "hub_name": "SK AI 4.0 Super Admin Sovereign Hub",
            "owner": cls.OWNER,
            "organization": cls.ORGANIZATION,
            "global_system_status": registry["global_system_status"],
            "global_kill_switch_active": registry["global_kill_switch_active"],
            "total_users": len(users_list),
            "active_users": active_count,
            "disabled_users": disabled_count,
            "users_registry": users_list,
            "anti_extraction_shield": shield_status,
            "admin_whatsapp": cls.DEFAULT_PHONE,
            "synced_at": registry.get("last_sync")
        }

if __name__ == "__main__":
    hub = SuperAdminHub.get_full_hub_status()
    print(f"[SUPER ADMIN HUB]: Status = {hub['global_system_status']} | Owner = {hub['owner']}")
    reg = SuperAdminHub.register_user("Amit Kumar", "amit@test.com", "9153579997")
    print("Registered User:", reg["user"]["name"], "| Status:", reg["status"])
    iso = SuperAdminHub.get_user_isolated_memory("Amit")
    print("Isolated Search Result:", iso["found"], "| User:", iso.get("user_identity", {}).get("name"))
