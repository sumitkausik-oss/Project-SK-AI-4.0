"""
SK Enterprises | 1-Click Automated Windows EXE Compiler
Founder & Architect: Sumeet Kumar
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
print("=" * 80)
print("  BUILDING STANDALONE WINDOWS EXE: SK_AI_4.0_Setup.exe")
print("=" * 80)

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
print(f"Executable built at: {ROOT / 'dist' / 'SK_AI_4.0' / 'SK_AI_4.0.exe'}")
