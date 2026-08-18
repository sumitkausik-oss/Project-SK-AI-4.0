"""
SK Enterprises | Master Key Generator Unit
Founder, Inventor & Sole Architect: Sumeet Kumar
Platform V5.0 — Sovereign Cryptographic Licensing Suite

Provides:
- Lifetime Sovereign Admin Keys (Unrestricted Super Admin Privileges)
- 1-Year (365-Day) Commercial User License Keys
- Cryptographic HMAC-SHA256 & SHA3 Digital Signatures
"""
import json
import base64
import hmac
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Any

ADMIN_MASTER_SECRET = "SK_ENTERPRISES_SUMEET_KUMAR_2026_MASTER_SUPER_ADMIN_KEY"
USER_LICENSE_SECRET = "SK_ENTERPRISES_SUMEET_KUMAR_2026_USER_LICENSE_SALT"

class MasterKeyGenerator:
    """
    Generates cryptographic lifetime admin keys and 1-year user license keys.
    """

    @classmethod
    def generate_admin_lifetime_key(cls, admin_name: str = "Sumeet Kumar", admin_email: str = "sumeet.admin@skenterprises.ai") -> Dict[str, Any]:
        """
        Generates an immutable Lifetime Super Admin Sovereign Key.
        """
        issued_date = datetime.now()
        payload = {
            "key_type": "SUPER_ADMIN_LIFETIME",
            "license_id": f"SK-SUPER-ADMIN-{issued_date.strftime('%Y%m%d%H%M%S')}",
            "admin_name": admin_name,
            "admin_email": admin_email,
            "role": "SOVEREIGN_SUPER_ADMIN",
            "organization": "SK Enterprises",
            "founder": "Sumeet Kumar",
            "issued_at": issued_date.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": "LIFETIME_NEVER_EXPIRES",
            "lifetime_access": True,
            "super_powers": [
                "GLOBAL_KILL_SWITCH", "EXE_BUILDER", "APK_DISPATCHER",
                "REMOTE_USER_LOCK", "CENTRAL_MEMORY_HUB", "UNRESTRICTED_ACCESS"
            ]
        }
        
        raw_payload = json.dumps(payload, sort_keys=True)
        signature = hmac.new(ADMIN_MASTER_SECRET.encode('utf-8'), raw_payload.encode('utf-8'), hashlib.sha256).hexdigest()
        token = base64.b64encode(json.dumps({"payload": payload, "sig": signature, "v": "5.0"}).encode('utf-8')).decode('utf-8')
        
        return {
            "key_type": "SUPER_ADMIN_LIFETIME",
            "license_key": token,
            "details": payload,
            "status": "ACTIVE_LIFETIME"
        }

    @classmethod
    def generate_user_annual_key(cls, user_name: str, user_email: str, phone: str = "9153579997", tier: str = "PRO_COMMERCIAL") -> Dict[str, Any]:
        """
        Generates a 1-Year (365-Day) Commercial User License Key.
        """
        issued_date = datetime.now()
        expiry_date = issued_date + timedelta(days=365)
        
        payload = {
            "key_type": "USER_ANNUAL_365",
            "license_id": f"SK4-USER-{issued_date.strftime('%Y%m%d%H%M%S')}",
            "user_name": user_name,
            "user_email": user_email,
            "phone": phone,
            "tier": tier,
            "organization": "SK Enterprises",
            "inventor": "Sumeet Kumar",
            "issued_at": issued_date.strftime("%Y-%m-%d"),
            "expires_at": expiry_date.strftime("%Y-%m-%d"),
            "valid_days": 365,
            "active_status": True
        }
        
        raw_payload = json.dumps(payload, sort_keys=True)
        signature = hmac.new(USER_LICENSE_SECRET.encode('utf-8'), raw_payload.encode('utf-8'), hashlib.sha256).hexdigest()
        token = base64.b64encode(json.dumps({"payload": payload, "sig": signature, "v": "5.0"}).encode('utf-8')).decode('utf-8')
        
        return {
            "key_type": "USER_ANNUAL_365",
            "license_key": token,
            "details": payload,
            "expires_at": expiry_date.strftime("%Y-%m-%d"),
            "status": "ACTIVE_365_DAYS"
        }

    @classmethod
    def validate_any_key(cls, key_token: str) -> Dict[str, Any]:
        """
        Validates whether a key is an authentic Lifetime Admin Key or a valid User Annual Key.
        """
        try:
            raw_data = json.loads(base64.b64decode(key_token.encode('utf-8')).decode('utf-8'))
            payload = raw_data["payload"]
            sig = raw_data["sig"]
            key_type = payload.get("key_type")
            
            raw_payload = json.dumps(payload, sort_keys=True)
            
            if key_type == "SUPER_ADMIN_LIFETIME":
                expected_sig = hmac.new(ADMIN_MASTER_SECRET.encode('utf-8'), raw_payload.encode('utf-8'), hashlib.sha256).hexdigest()
                if not hmac.compare_digest(sig, expected_sig):
                    return {"valid": False, "reason": "Invalid Admin Digital Signature"}
                return {"valid": True, "type": "SUPER_ADMIN", "payload": payload}
                
            elif key_type == "USER_ANNUAL_365":
                expected_sig = hmac.new(USER_LICENSE_SECRET.encode('utf-8'), raw_payload.encode('utf-8'), hashlib.sha256).hexdigest()
                if not hmac.compare_digest(sig, expected_sig):
                    return {"valid": False, "reason": "Invalid User Digital Signature"}
                
                # Check expiration
                expiry = datetime.strptime(payload["expires_at"], "%Y-%m-%d")
                if datetime.now() > expiry:
                    return {"valid": False, "reason": "1-Year License Has Expired"}
                
                return {"valid": True, "type": "USER_ANNUAL", "payload": payload}
            else:
                return {"valid": False, "reason": "Unrecognized License Key Format"}
        except Exception as e:
            return {"valid": False, "reason": f"Corrupted or Invalid Key: {str(e)}"}

if __name__ == "__main__":
    admin_key = MasterKeyGenerator.generate_admin_lifetime_key()
    print("Generated Admin Key:", admin_key["license_key"][:30] + "...")
    user_key = MasterKeyGenerator.generate_user_annual_key("Amit Sharma", "amit@example.com", "9153579997")
    print("Generated User Key:", user_key["license_key"][:30] + "...")
    print("Validation Admin:", MasterKeyGenerator.validate_any_key(admin_key["license_key"])["valid"])
    print("Validation User:", MasterKeyGenerator.validate_any_key(user_key["license_key"])["valid"])
