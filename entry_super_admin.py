"""
SK Enterprises | Super Admin Master Control Hub CLI
Founder, Inventor & Sole Architect: Sumeet Kumar
Platform V5.0 — Master Administration Suite
"""
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.super_admin_hub import SuperAdminHub

def run_super_admin_console():
    print("=" * 80)
    print("  👑 SK ENTERPRISES | SUPER ADMIN SOVEREIGN CONTROL HUB")
    print("  SOLE INVENTOR, FOUNDER & ARCHITECT: SUMEET KUMAR")
    print("=" * 80)
    
    while True:
        hub = SuperAdminHub.get_full_hub_status()
        print("\n--- MASTER DASHBOARD OVERVIEW ---")
        print(f"System Status: {hub['global_system_status']} | Total Users: {hub['total_users']} | Active: {hub['active_users']} | Disabled: {hub['disabled_users']}")
        print(f"Global Kill Switch: {'ACTIVE (ALL DISABLED)' if hub['global_kill_switch_active'] else 'INACTIVE (NOMINAL)'}")
        print(f"Anti-Extraction Shield: {hub['anti_extraction_shield']['status']} ({hub['anti_extraction_shield']['security_tier']})")
        print("-" * 60)
        print("1. Register New Client User (Generates 1-Year Key + EXE + APK + WhatsApp Link)")
        print("2. Search Isolated User Memory Reflection (Strict Zero Cross-Contamination)")
        print("3. Remote User Kill-Switch (Enable / Disable / Revoke User)")
        print("4. Toggle Master Global Kill-Switch (Emergency Lockdown)")
        print("5. View Full Users Registry")
        print("6. Exit")
        print("-" * 60)
        
        choice = input("Select Master Action (1-6): ").strip()
        
        if choice == "1":
            name = input("Client Name: ").strip() or "Client User"
            email = input("Client Email: ").strip() or "client@example.com"
            phone = input("Client Phone (for WhatsApp) [Default: 9153579997]: ").strip() or "9153579997"
            res = SuperAdminHub.register_user(name, email, phone)
            print("\n" + "👑" * 35)
            print(f"CLIENT REGISTERED: {name} ({email})")
            print(f"1-Year License Key:\n{res['license_key']}")
            print(f"Windows Package: {res['user']['windows_package']['installer_link']}")
            print(f"WhatsApp Dispatch URL:\n{res['whatsapp_dispatch_url']}")
            print("👑" * 35)
            
        elif choice == "2":
            q = input("Enter User Name or Email to Search Isolated Memory (e.g. 'Amit'): ").strip()
            iso = SuperAdminHub.get_user_isolated_memory(q)
            print("\n" + "🔍" * 35)
            print(f"SEARCH QUERY: '{q}' | FOUND: {iso['found']}")
            if iso["found"]:
                print("USER IDENTITY:", json.dumps(iso["user_identity"], indent=2))
                print(f"ISOLATED MEMORY RECORDS ({iso['total_records']} total):")
                print(json.dumps(iso["isolated_memory_records"], indent=2))
                print(f"SECURITY: {iso['security_lock']}")
            else:
                print(iso["message"])
            print("🔍" * 35)
            
        elif choice == "3":
            email = input("Enter Target User Email: ").strip()
            print("Available Statuses: ACTIVE, DISABLED, REVOKED")
            status = input("Enter New Status [DISABLED]: ").strip().upper() or "DISABLED"
            res = SuperAdminHub.set_user_status(email, status)
            print("\n" + "⚡" * 35)
            print("KILL-SWITCH RESULT:", res)
            print("⚡" * 35)
            
        elif choice == "4":
            current = hub["global_kill_switch_active"]
            new_state = not current
            res = SuperAdminHub.toggle_global_kill_switch(new_state)
            print("\n" + "🚨" * 35)
            print(f"GLOBAL KILL SWITCH SET TO: {res['global_kill_switch_active']}")
            print(f"SYSTEM STATUS: {res['system_status']}")
            print("🚨" * 35)
            
        elif choice == "5":
            print("\n" + "📋" * 35)
            print("FULL USERS REGISTRY:")
            for u in hub["users_registry"]:
                print(f"- {u['name']} | {u['email']} | Status: {u['status']} | Phone: {u.get('phone')} | Expires: {u.get('expires_at')}")
            print("📋" * 35)
            
        elif choice == "6":
            print("Exiting Super Admin Console.")
            break

if __name__ == "__main__":
    run_super_admin_console()
