"""
SK Enterprises | Master All-in-One Windows Executable & Package Builder
Founder, Inventor & Sole Architect: Sumeet Kumar
Platform V5.0
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"
DIST_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("  [SK ENTERPRISES] | MASTER EXECUTABLE & DEPLOYMENT PACKAGER")
print("  SOLE INVENTOR & ARCHITECT: Sumeet Kumar")
print("=" * 80)

# Generate direct instant Windows EXE Launchers / Batch Runners
def create_standalone_launchers():
    # 1. Super Admin Launcher
    admin_bat = ROOT / "Launch_Super_Admin.bat"
    admin_bat.write_text(f"""@echo off
title SK AI 4.0 - Super Admin Master Hub (Sumeet Kumar)
cd /d "{ROOT}"
python entry_super_admin.py
pause
""", encoding="utf-8")

    # 2. Key Generator Launcher
    keygen_bat = ROOT / "Launch_Key_Generator.bat"
    keygen_bat.write_text(f"""@echo off
title SK AI 4.0 - Key Generator Unit (Sumeet Kumar)
cd /d "{ROOT}"
python entry_keygen.py
pause
""", encoding="utf-8")

    # 3. User Setup Wizard Installer Launcher
    installer_bat = ROOT / "Launch_User_Installer.bat"
    installer_bat.write_text(f"""@echo off
title SK AI 4.0 - Interactive Setup Installer (SK Enterprises)
cd /d "{ROOT}"
python entry_installer.py
pause
""", encoding="utf-8")

    # 4. Main Runtime Launcher
    runtime_bat = ROOT / "Launch_SK_AI_4.0.bat"
    runtime_bat.write_text(f"""@echo off
title SK AI 4.0 - Sovereign Runtime (Sumeet Kumar)
cd /d "{ROOT}"
python run_sk_ai.py
pause
""", encoding="utf-8")

    print("[*] Created 4 Portable Windows Launchers:")
    print("    - Launch_Super_Admin.bat")
    print("    - Launch_Key_Generator.bat")
    print("    - Launch_User_Installer.bat")
    print("    - Launch_SK_AI_4.0.bat")

if __name__ == "__main__":
    create_standalone_launchers()
