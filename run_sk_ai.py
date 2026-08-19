import os
import sys
import time
import socket
import subprocess
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "src_frontend" / "index.html"
BACKEND = ROOT / "src_backend" / "engine.py"

def is_port_in_use(port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

print("=" * 80)
print("  SK ENTERPRISES | LAUNCHING SK AI 4.0 PLATFORM V5.0")
print("  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR")
print("=" * 80)

if not is_port_in_use(8000):
    subprocess.Popen([sys.executable, str(BACKEND)], cwd=str(ROOT))
    print("[BACKEND]: FastAPI Engine spawned on http://127.0.0.1:8000")
    time.sleep(1.5)
else:
    print("[BACKEND]: Engine already active on http://127.0.0.1:8000")

webbrowser.open(f"file:///{FRONTEND}")
print("[FRONTEND]: Cyber HUD & World Monitor LIVE.")
