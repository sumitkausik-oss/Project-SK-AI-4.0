"""
SK Enterprises | Master Key Generator Tool
Founder, Inventor & Sole Architect: Sumeet Kumar
Platform V5.0 — Cryptographic Key Generator (Lifetime Admin & 1-Year User Keys)
"""
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.key_generator_master import MasterKeyGenerator

def cli_keygen():
    print("=" * 75)
    print("  👑 SK ENTERPRISES | MASTER KEY GENERATOR UNIT")
    print("  SOLE INVENTOR, FOUNDER & ARCHITECT: SUMEET KUMAR")
    print("=" * 75)
    print("1. Generate Lifetime Sovereign Admin Key (Super Admin - Sumeet Kumar)")
    print("2. Generate 1-Year Commercial User License Key (365 Days)")
    print("3. Validate Any License Key")
    print("=" * 75)
    
    choice = input("Select option (1/2/3) [Default: 2]: ").strip() or "2"
    
    if choice == "1":
        name = input("Admin Name [Default: Sumeet Kumar]: ").strip() or "Sumeet Kumar"
        email = input("Admin Email [Default: sumeet.admin@skenterprises.ai]: ").strip() or "sumeet.admin@skenterprises.ai"
        res = MasterKeyGenerator.generate_admin_lifetime_key(name, email)
        print("\n" + "⭐" * 35)
        print(f"LIFETIME SUPER ADMIN KEY GENERATED FOR: {name}")
        print("KEY TOKEN:\n" + res["license_key"])
        print("⭐" * 35 + "\n")
        
    elif choice == "2":
        name = input("Client Name: ").strip() or "Client User"
        email = input("Client Email: ").strip() or "client@example.com"
        phone = input("Client Phone (for WhatsApp) [Default: 9153579997]: ").strip() or "9153579997"
        res = MasterKeyGenerator.generate_user_annual_key(name, email, phone)
        print("\n" + "🔑" * 35)
        print(f"1-YEAR USER LICENSE KEY GENERATED FOR: {name} (Expires: {res['expires_at']})")
        print("KEY TOKEN:\n" + res["license_key"])
        print("🔑" * 35 + "\n")
        
    elif choice == "3":
        token = input("Enter License Key Token to Validate: ").strip()
        val = MasterKeyGenerator.validate_any_key(token)
        print("\n" + "🔍" * 35)
        print(f"VALID: {val['valid']}")
        if val["valid"]:
            print(f"TYPE: {val['type']}")
            print("PAYLOAD:", json.dumps(val["payload"], indent=2))
        else:
            print("REASON:", val.get("reason"))
        print("🔍" * 35 + "\n")

if __name__ == "__main__":
    cli_keygen()
