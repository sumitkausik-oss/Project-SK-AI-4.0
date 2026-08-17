import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "src_frontend" / "index.html"
BACKEND = ROOT / "src_backend" / "engine.py"

print("=" * 80)
print("  LAUNCHING PROPRIETARY SK AI 4.0 (PROJECT JARVIS 4.0)")
print("  FOUNDER & INVENTOR: SUMEET KUMAR | SK ENTERPRISES")
print("=" * 80)

subprocess.Popen([sys.executable, str(BACKEND)], cwd=str(ROOT))
time.sleep(1.2)
webbrowser.open(f"file:///{FRONTEND}")
