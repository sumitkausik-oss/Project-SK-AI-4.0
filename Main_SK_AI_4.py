"""
SK Enterprises | Project SK AI 4.0 (Project JARVIS 4.0)
Inventor & Sole Architect: Sumeet Kumar
Master Enterprise Entry Point & Runtime Orchestrator
"""
import os
import sys
import json
import traceback
from pathlib import Path

# Add Base Directory to sys.path
from core.system_paths import BASE_DIR, APPDATA_DIR, LOGS_DIR, CRASH_LOG, log_crash_and_notify

# NEW: Import standardized configuration
import config
from core.memory_manager import MemoryManager
from core.coral_brain_logic import CoralBrainSchema

sys.path.insert(0, str(BASE_DIR))

def run_headless_console():
    from core.commercial_auth_rbac import CommercialAccessGate
    from core.autonomous_learner import AutonomousLearningEngine
    from core.education_matrix import UniversalEducationMatrix
    from core.data_analyst_engine import DataAnalystSuite
    from core.cloud_admin_engine import CloudAdminActuator
    from core.astrology_engine import VedicAstrologyCore

    print("=" * 85)
    print("  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)")
    print("  INVENTOR & SOLE ARCHITECT: Sumeet Kumar | COMMERCIAL COGNITIVE OS")
    print("=" * 85)

    license_file = BASE_DIR / "config" / "license.key"
    if license_file.exists():
        print("[SECURITY]: Lifetime Admin Master License Verified for Sumeet Kumar.")
    
    identity_file = BASE_DIR / "config" / "system_identity.json"
    if identity_file.exists():
        ident = json.loads(identity_file.read_text(encoding="utf-8"))
        print(f"[IDENTITY]: {ident.get('system_name')} | Creator: {ident.get('inventor')} ({ident.get('organization')})")

    memory = MemoryManager()
    print("[SYSTEM]: Central Memory Core ACTIVE.")
    learner = AutonomousLearningEngine()
    learner.start_daemon()
    print("[COGNITION]: 24x7 Self-Learning & Skill Expansion Daemon ACTIVE.")

    coral_brain = CoralBrainSchema()

    edu = UniversalEducationMatrix()
    data_suite = DataAnalystSuite()
    cloud_admin = CloudAdminActuator()
    astro = VedicAstrologyCore()

    coral_brain.integrate_core_engine('EducationMatrix', edu)
    coral_brain.integrate_core_engine('DataAnalystSuite', data_suite)
    coral_brain.integrate_core_engine('CloudAdmin', cloud_admin)
    coral_brain.integrate_core_engine('VedicAstrology', astro)
    
    print("[ENGINES LOADED]:")
    print(f" -> Education Matrix: {len(edu.curriculum)} Core Tracks Online.")
    print(f" -> Data Analyst Suite: Ready (EDA, Cleaning, BI Visuals, SQL Gen).")
    print(f" -> Cloud Admin Actuator: Google Workspace & M365 Zero-Trust Enforced.")
    print(f" -> Vedic Astrology: Ephemeris & Kundali Engine Synchronized.")

    print("\n[SYSTEM READY]: Project SK AI 4.0 Operational in Master Enterprise Mode.")

def main():
    try:
        # Change working directory to BASE_DIR so relative resource lookup always works
        os.chdir(str(BASE_DIR))

        # Check if CLI/headless mode is requested
        if "--headless" in sys.argv or "--cli" in sys.argv:
            run_headless_console()
            return

        # Default: Launch GUI Dashboard
        from core.gui_dashboard import launch_gui
        launch_gui()

    except Exception as e:
        log_crash_and_notify("SK AI 4.0 Startup Error", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
