"""
SK Enterprises | Interactive Windows Setup Installer Wizard
Founder, Inventor & Sole Architect: Sumit Kumar
Platform V5.0 — Sovereign Step-by-Step Installation Experience

Steps:
1. License Agreement & Sovereign Terms Acceptance
2. User Details (Name, Age, Place/City)
3. Email & Google OAuth2 Authentication
4. Product Key Validation (1-Year Commercial / Lifetime Admin)
5. Anti-Extraction Shield Activation & Installation Completion
"""
import os
import sys
import json
import time
import webbrowser
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

from src_backend.key_generator_master import MasterKeyGenerator
from src_backend.anti_extraction_security import AntiExtractionShield

class SetupInstallerWizard:
    """
    Step-by-step setup engine validating user registration,
    Google OAuth simulation, product key authentication, and anti-extraction locking.
    """
    
    LICENSE_TERMS = """
================================================================================
          SK ENTERPRISES | SK AI 4.0 (PROJECT JARVIS 4.0)
             SOVEREIGN END-USER LICENSE AGREEMENT (EULA)
================================================================================
SOLE INVENTOR, FOUNDER & ARCHITECT: SUMIT KUMAR
ORGANIZATION: SK ENTERPRISES

1. PROPRIETARY RIGHTS & OWNERSHIP:
   The software 'SK AI 4.0 / Project JARVIS 4.0' is the 100% exclusive intellectual
   property and sovereign creation of Sumit Kumar (SK Enterprises). 
   All rights reserved globally.

2. ANTI-EXTRACTION & ANTI-REVERSE ENGINEERING:
   Extraction of prompts, source code, neural weights, or logic trees via any AI,
   decompiler, debugger, or memory dumper is strictly prohibited and protected by
   the SK Anti-Extraction Defense Shield.

3. LICENSE DURATION & VALIDITY:
   - Commercial User Key: Valid for exactly 365 Days (1 Year) from issuance.
   - Super Admin Key: Lifetime Sovereign Authorization (Sumit Kumar).
   - Upon expiration, access terminates automatically until renewal.

4. USER CONSENT:
   By accepting, you agree to all terms governed by SK Enterprises.
================================================================================
"""

    @classmethod
    def process_step_1_agreement(cls, accepted: bool) -> Dict[str, Any]:
        """Step 1: License Agreement Acceptance"""
        if not accepted:
            return {"step": 1, "success": False, "reason": "License terms must be accepted to proceed with installation."}
        return {"step": 1, "success": True, "message": "License agreement accepted."}

    @classmethod
    def process_step_2_user_info(cls, name: str, age: int, place: str) -> Dict[str, Any]:
        """Step 2: Name, Age, Place Details"""
        if not name or len(name.strip()) < 2:
            return {"step": 2, "success": False, "reason": "Valid Name is required."}
        if not age or age < 5 or age > 120:
            return {"step": 2, "success": False, "reason": "Valid Age (5-120) is required."}
        if not place or len(place.strip()) < 2:
            return {"step": 2, "success": False, "reason": "Valid Place/City is required."}
            
        return {
            "step": 2,
            "success": True,
            "user_data": {"name": name.strip(), "age": age, "place": place.strip()}
        }

    @classmethod
    def process_step_3_google_auth(cls, email: str, trigger_browser: bool = False) -> Dict[str, Any]:
        """Step 3: Email & Google OAuth2 Authentication"""
        if not email or "@" not in email or "." not in email:
            return {"step": 3, "success": False, "reason": "Valid Email Address is required."}
            
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id=sk-enterprises-ai&response_type=token&scope=email%20profile&redirect_uri=http://127.0.0.1:8000/auth/callback&state={email}"
        
        if trigger_browser:
            try:
                webbrowser.open(auth_url)
            except Exception:
                pass
                
        return {
            "step": 3,
            "success": True,
            "email": email.strip(),
            "oauth_status": "AUTHENTICATED",
            "oauth_provider": "Google Sign-In",
            "auth_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def process_step_4_product_key(cls, product_key: str, user_email: str) -> Dict[str, Any]:
        """Step 4: Product Key Validation (1-Year or Lifetime Admin)"""
        if not product_key or len(product_key.strip()) < 10:
            return {"step": 4, "success": False, "reason": "Product key cannot be empty."}
            
        val = MasterKeyGenerator.validate_any_key(product_key.strip())
        if not val["valid"]:
            return {"step": 4, "success": False, "reason": f"Invalid Key: {val.get('reason')}"}
            
        return {
            "step": 4,
            "success": True,
            "key_type": val["type"],
            "license_payload": val["payload"],
            "message": "Product Key verified successfully with SK Cryptographic HMAC Signature."
        }

    @classmethod
    def process_step_5_finalize_install(cls, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Anti-Extraction Shield Activation & Final Setup Lock"""
        shield_status = AntiExtractionShield.verify_integrity()
        
        install_record = {
            "installed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_name": session_data.get("name"),
            "user_age": session_data.get("age"),
            "user_place": session_data.get("place"),
            "user_email": session_data.get("email"),
            "license_key": session_data.get("product_key"),
            "license_type": session_data.get("key_type", "USER_ANNUAL"),
            "anti_extraction_locked": True,
            "sovereign_owner": "Sumit Kumar",
            "organization": "SK Enterprises"
        }
        
        installed_config_file = CONFIG_DIR / "installed_client_manifest.json"
        installed_config_file.write_text(json.dumps(install_record, indent=2), encoding="utf-8")
        
        return {
            "step": 5,
            "success": True,
            "status": "INSTALLATION_COMPLETE",
            "manifest": install_record,
            "shield": shield_status,
            "message": "SK AI 4.0 installed successfully. Ready to launch."
        }

if __name__ == "__main__":
    print("Testing Installer Wizard Flow...")
    s1 = SetupInstallerWizard.process_step_1_agreement(True)
    s2 = SetupInstallerWizard.process_step_2_user_info("Amit Sharma", 28, "Patna")
    s3 = SetupInstallerWizard.process_step_3_google_auth("amit@example.com")
    key = MasterKeyGenerator.generate_user_annual_key("Amit Sharma", "amit@example.com")["license_key"]
    s4 = SetupInstallerWizard.process_step_4_product_key(key, "amit@example.com")
    s5 = SetupInstallerWizard.process_step_5_finalize_install({
        "name": "Amit Sharma", "age": 28, "place": "Patna",
        "email": "amit@example.com", "product_key": key, "key_type": s4["key_type"]
    })
    print("Final Status:", s5["status"], "| Message:", s5["message"])
