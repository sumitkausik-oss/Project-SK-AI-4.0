"""
SK Enterprises | 1-Click Automated Windows EXE Compiler
Founder & Architect: Sumeet Kumar
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist" / "SK_AI_4.0_Executable"
DIST_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("  SK ENTERPRISES | 1-CLICK STANDALONE WINDOWS EXE BUILDER")
print("  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR")
print("=" * 80)

# 1. PyInstaller चेक व इंस्टॉलेशन
try:
    import PyInstaller
except ImportError:
    print("[Setup]: Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

# 2. PyInstaller सिंगल-कमांड बाइनरी पैकेजिंग
print("[Compiling]: Building Standalone Python-Window Binary...")
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--onedir",
    "--windowed",
    "--name", "SK_AI_4.0",
    f"--distpath={str(ROOT / 'dist')}",
    f"--workpath={str(ROOT / 'build')}",
    f"--add-data=src_frontend;src_frontend",
    f"--add-data=config;config",
    f"--add-data=assets;assets",
    str(ROOT / "run_sk_ai.py")
]
subprocess.run(cmd, cwd=str(ROOT))

print("\n" + "=" * 80)
print("  EXE BUILD COMPLETED!")
print(f"  Executable Location: {ROOT / 'dist' / 'SK_AI_4.0' / 'SK_AI_4.0.exe'}")
print("=" * 80)
