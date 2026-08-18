"""
SK Enterprises | 1-Year Client Cryptographic License Engine
Founder & Architect: Sumit Kumar
"""
import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta

MASTER_SALT = "SK_ENTERPRISES_SUMIT_KUMAR_2026_SOVEREIGN_SECRET"

class SKLicenseKeyEngine:
    @staticmethod
    def generate_client_key(client_name: str, client_email: str, tier: str = "PRO_COMMERCIAL") -> dict:
        issued_date = datetime.now()
        expiry_date = issued_date + timedelta(days=365)
        
        payload = {
            "license_id": f"SK4-CLIENT-{issued_date.strftime('%Y%m%d%H%M%S')}",
            "client_name": client_name,
            "client_email": client_email,
            "tier": tier,
            "issuer": "SK Enterprises (Sumit Kumar)",
            "issued_at": issued_date.strftime("%Y-%m-%d"),
            "expires_at": expiry_date.strftime("%Y-%m-%d"),
            "valid_days": 365
        }
        
        raw_str = json.dumps(payload, sort_keys=True)
        sig = hmac.new(MASTER_SALT.encode(), raw_str.encode(), hashlib.sha256).hexdigest()
        token = base64.b64encode(json.dumps({"payload": payload, "sig": sig}).encode()).decode()
        
        return {
            "license_key": token,
            "details": payload
        }

    @staticmethod
    def validate_key(token: str) -> dict:
        try:
            data = json.loads(base64.b64decode(token.encode()).decode())
            payload = data["payload"]
            sig = data["sig"]
            
            raw_str = json.dumps(payload, sort_keys=True)
            expected_sig = hmac.new(MASTER_SALT.encode(), raw_str.encode(), hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(sig, expected_sig):
                return {"valid": False, "reason": "Invalid Digital Signature"}
                
            expiry = datetime.strptime(payload["expires_at"], "%Y-%m-%d")
            if datetime.now() > expiry:
                return {"valid": False, "reason": "License Expired"}
                
            return {"valid": True, "payload": payload}
        except Exception as e:
            return {"valid": False, "reason": f"Corrupted Key: {str(e)}"}
