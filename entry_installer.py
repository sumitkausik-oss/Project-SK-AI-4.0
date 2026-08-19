"""
SK Enterprises | Interactive Windows Setup Installer Runner
Founder, Inventor & Sole Architect: Sumeet Kumar
Platform V5.0 — Windows Setup Wizard
"""
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.installer_wizard_app import SetupInstallerWizard

def run_interactive_installer():
    print("=" * 80)
    print("  👑 SK ENTERPRISES | SK AI 4.0 (PROJECT JARVIS 4.0) INSTALLER WIZARD")
    print("  SOLE INVENTOR, FOUNDER & ARCHITECT: Sumeet Kumar")
    print("=" * 80)
    
    # STEP 1: License Agreement
    print(SetupInstallerWizard.LICENSE_TERMS)
    agree = input("Do you accept the License Agreement and Sovereign Terms? (y/n) [y]: ").strip().lower() or "y"
    if agree != "y":
        print("[!] Installation Aborted. You must accept terms to proceed.")
        return
    res1 = SetupInstallerWizard.process_step_1_agreement(True)
    print(f"[*] Step 1 Complete: {res1['message']}\n")
    
    # STEP 2: Identification
    print("-" * 60)
    print("  STEP 2: USER IDENTIFICATION")
    print("-" * 60)
    name = input("Enter Your Full Name: ").strip() or "Sumeet Kumar"
    age_str = input("Enter Your Age: ").strip() or "30"
    age = int(age_str) if age_str.isdigit() else 30
    place = input("Enter Your Place / City: ").strip() or "Patna, Bihar"
    
    res2 = SetupInstallerWizard.process_step_2_user_info(name, age, place)
    if not res2["success"]:
        print(f"[!] Error: {res2['reason']}")
        return
    print(f"[*] Step 2 Complete: User Identified as {name}, Age: {age}, Place: {place}\n")
    
    # STEP 3: Google Auth
    print("-" * 60)
    print("  STEP 3: EMAIL & GOOGLE OAUTH2 AUTHENTICATION")
    print("-" * 60)
    email = input("Enter Your Email Address: ").strip() or "user@skenterprises.ai"
    print("Authenticating with Google OAuth2 Protocol...")
    time.sleep(0.5)
    res3 = SetupInstallerWizard.process_step_3_google_auth(email, trigger_browser=False)
    if not res3["success"]:
        print(f"[!] Error: {res3['reason']}")
        return
    print(f"[*] Step 3 Complete: {email} Authenticated via Google Sign-In.\n")
    
    # STEP 4: Product Key
    print("-" * 60)
    print("  STEP 4: PRODUCT KEY VALIDATION (1-Year Commercial or Admin Key)")
    print("-" * 60)
    from src_backend.key_generator_master import MasterKeyGenerator
    default_test_key = MasterKeyGenerator.generate_user_annual_key(name, email)["license_key"]
    print("Enter your 1-Year or Lifetime Product License Key.")
    print(f"(Press Enter to use newly issued sample key for this session)")
    pkey = input("Product Key: ").strip() or default_test_key
    
    res4 = SetupInstallerWizard.process_step_4_product_key(pkey, email)
    if not res4["success"]:
        print(f"[!] Error: {res4['reason']}")
        return
    print(f"[*] Step 4 Complete: Key Type '{res4['key_type']}' Verified with HMAC-SHA256 Digital Signature.\n")
    
    # STEP 5: Anti-Extraction Lock & Final Unpack
    print("-" * 60)
    print("  STEP 5: ANTI-EXTRACTION SHIELD & FINAL UNPACK")
    print("-" * 60)
    print("Locking Bytecode & Activating Anti-Extraction Defense Layer...")
    time.sleep(0.5)
    session_data = {
        "name": name, "age": age, "place": place,
        "email": email, "product_key": pkey, "key_type": res4["key_type"]
    }
    res5 = SetupInstallerWizard.process_step_5_finalize_install(session_data)
    print(f"[*] {res5['message']}")
    print(f"[*] Security Status: {res5['shield']['status']} (Defense Tier: {res5['shield']['security_tier']})")
    print("=" * 80)
    print("  👑 SK AI 4.0 IS NOW FULLY INSTALLED AND READY FOR LAUNCH!")
    print("  Launch Command: python run_sk_ai.py")
    print("=" * 80)

if __name__ == "__main__":
    run_interactive_installer()
