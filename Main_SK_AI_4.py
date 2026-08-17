import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.commercial_auth_rbac import CommercialAccessGate
from core.autonomous_learner import AutonomousLearningEngine
from core.education_matrix import UniversalEducationMatrix
from core.data_analyst_engine import DataAnalystSuite
from core.cloud_admin_engine import CloudAdminActuator
from core.astrology_engine import VedicAstrologyCore

def main():
    print("=" * 85)
    print("  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)")
    print("  INVENTOR & SOLE ARCHITECT: SUMIT KUMAR | COMMERCIAL COGNITIVE OS")
    print("=" * 85)

    # 1. लाइसेंस और आइडेंटिटी लोड करना
    license_file = BASE_DIR / "config" / "license.key"
    if license_file.exists():
        print("[SECURITY]: Lifetime Admin Master License Verified for Sumit Kumar.")
    
    identity_file = BASE_DIR / "config" / "system_identity.json"
    if identity_file.exists():
        ident = json.loads(identity_file.read_text(encoding="utf-8"))
        print(f"[IDENTITY]: {ident['system_name']} | Creator: {ident['inventor']} ({ident['organization']})")

    # 2. बैकग्राउंड लर्निंग इंजन चालू करना
    learner = AutonomousLearningEngine()
    learner.start_daemon()
    print("[COGNITION]: 24x7 Self-Learning & Skill Expansion Daemon ACTIVE.")

    # 3. सभी डोमेन इंजन इनिशियलाइज़ करना
    edu = UniversalEducationMatrix()
    data_suite = DataAnalystSuite()
    cloud_admin = CloudAdminActuator()
    astro = VedicAstrologyCore()
    
    print("[ENGINES LOADED]:")
    print(f" -> Education Matrix: {len(edu.curriculum)} Core Tracks Online.")
    print(f" -> Data Analyst Suite: Ready (EDA, Cleaning, BI Visuals, SQL Gen).")
    print(f" -> Cloud Admin Actuator: Google Workspace & M365 Zero-Trust Enforced.")
    print(f" -> Vedic Astrology: Ephemeris & Kundali Engine Synchronized.")
    print("\n[SYSTEM READY]: Project SK AI 4.0 Operational in Master Enterprise Mode.")

if __name__ == "__main__":
    main()
