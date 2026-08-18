"""
SK Enterprises | Super Admin Hub, Key Generator & Deployment Engine
Founder & Architect: Sumit Kumar
"""
import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "admin_central_storage"
MASTER_SALT = "SK_ENTERPRISES_SUMIT_KUMAR_2026_SOVEREIGN_KEY_SALT"

class SuperAdminHub:
    @staticmethod
    def generate_license(client_name: str, client_email: str, tier: str = "1_YEAR_USER") -> dict:
        is_admin = (tier == "ADMIN_LIFETIME")
        issued_date = datetime.now()
        expiry_date = (issued_date + timedelta(days=36500)) if is_admin else (issued_date + timedelta(days=365))
        
        payload = {
            "license_id": f"SK4-{'ADMIN' if is_admin else 'CLIENT'}-{issued_date.strftime('%Y%m%d%H%M%S')}",
            "client_name": client_name,
            "client_email": client_email,
            "tier": tier,
            "issuer": "SK Enterprises (Sumit Kumar)",
            "issued_at": issued_date.strftime("%Y-%m-%d"),
            "expires_at": expiry_date.strftime("%Y-%m-%d"),
            "valid_days": 36500 if is_admin else 365,
            "status": "ACTIVE"
        }
        
        raw_str = json.dumps(payload, sort_keys=True)
        sig = hmac.new(MASTER_SALT.encode(), raw_str.encode(), hashlib.sha256).hexdigest()
        token = base64.b64encode(json.dumps({"payload": payload, "sig": sig}).encode()).decode()
        
        return {"license_key": token, "details": payload}

    @staticmethod
    def validate_license(token: str) -> dict:
        try:
            data = json.loads(base64.b64decode(token.encode()).decode())
            payload = data["payload"]
            sig = data["sig"]
            
            raw_str = json.dumps(payload, sort_keys=True)
            expected_sig = hmac.new(MASTER_SALT.encode(), raw_str.encode(), hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(sig, expected_sig):
                return {"valid": False, "reason": "Invalid Signature"}
                
            expiry = datetime.strptime(payload["expires_at"], "%Y-%m-%d")
            if datetime.now() > expiry:
                return {"valid": False, "reason": "License Expired"}
                
            # Check Central Remote Killswitch
            user_status_file = STORAGE_DIR / "users" / payload["client_email"].replace("@", "_at_") / "status.json"
            if user_status_file.exists():
                st = json.loads(user_status_file.read_text(encoding="utf-8"))
                if not st.get("active", True):
                    return {"valid": False, "reason": "Account Suspended by Super Admin"}

            return {"valid": True, "payload": payload}
        except Exception as e:
            return {"valid": False, "reason": f"Corrupted Key: {str(e)}"}

    @staticmethod
    def register_client(name: str, age: int, location: str, email: str, phone: str):
        user_dir = STORAGE_DIR / "users" / email.replace("@", "_at_")
        user_dir.mkdir(parents=True, exist_ok=True)
        profile = {
            "name": name, "age": age, "location": location,
            "email": email, "phone": phone, "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "active": True
        }
        (user_dir / "profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
        (user_dir / "status.json").write_text(json.dumps({"active": True}, indent=2), encoding="utf-8")
        
        license_info = SuperAdminHub.generate_license(name, email, "1_YEAR_USER")
        (user_dir / "license.json").write_text(json.dumps(license_info, indent=2), encoding="utf-8")
        
        return {"profile": profile, "license": license_info}

    @staticmethod
    def toggle_client_status(email: str, active: bool):
        user_dir = STORAGE_DIR / "users" / email.replace("@", "_at_")
        if user_dir.exists():
            (user_dir / "status.json").write_text(json.dumps({"active": active}, indent=2), encoding="utf-8")
            return {"status": "SUCCESS", "email": email, "active": active}
        return {"status": "NOT_FOUND"}

    @staticmethod
    def dispatch_whatsapp_installer(phone: str, client_name: str, download_link: str):
        return {
            "status": "DISPATCHED",
            "recipient": phone,
            "client_name": client_name,
            "message": f"Hello {client_name}, your SK AI 4.0 installer package is ready: {download_link}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
