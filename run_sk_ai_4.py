"""
SK Enterprises | SKAI Desktop Master Launcher
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI — Powered by SK Enterprises
"""
import os
import sys
import time
import socket
import subprocess
import webbrowser
import urllib.request
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND_FILE = ROOT / "frontend" / "index.html"
if not FRONTEND_FILE.exists():
    FRONTEND_FILE = ROOT / "src_frontend" / "index.html"

BACKEND_FILE = ROOT / "backend" / "main.py"
if not BACKEND_FILE.exists():
    BACKEND_FILE = ROOT / "src_backend" / "main_engine.py"

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_backend_healthy() -> bool:
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/health")
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data.get("status") == "HEALTHY"
    except Exception:
        return False
    return False

def free_port_if_stale(port: int):
    try:
        res = subprocess.run(
            f"powershell -Command \"(Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue).OwningProcess\"",
            shell=True, capture_output=True, text=True
        )
        pids = [p.strip() for p in res.stdout.splitlines() if p.strip() and p.strip() != '0']
        for pid in pids:
            try:
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
                print(f"[PROCESS CLEANUP]: Freed port {port} by terminating PID {pid}")
            except Exception:
                pass
    except Exception:
        pass

def main():
    print("=" * 85)
    print("  SK ENTERPRISES | SKAI (SKAI — Powered by SK Enterprises)")
    print("  FOUNDER & SOLE ARCHITECT: Sumeet Kumar | LOCAL-FIRST DESKTOP AI ASSISTANT")
    print("=" * 85)

    backend_ready = False

    if is_port_in_use(8000):
        if check_backend_healthy():
            print("[BACKEND]: Existing SKAI FastAPI Engine verified on http://127.0.0.1:8000")
            backend_ready = True
        else:
            print("[PORT RECOVERY]: Stale process found on port 8000. Releasing socket...")
            free_port_if_stale(8000)
            time.sleep(1)

    if not backend_ready:
        print("[BACKEND]: Spawning FastAPI Autonomous Engine on http://127.0.0.1:8000...")
        subprocess.Popen([sys.executable, str(BACKEND_FILE)], cwd=str(ROOT))
        
        for _ in range(12):
            time.sleep(0.5)
            if check_backend_healthy():
                backend_ready = True
                print("[BACKEND ONLINE]: OS Control, Memory, & Safety Gate Active.")
                break

    # Launch Desktop HUD in browser or electron
    frontend_uri = f"file:///{FRONTEND_FILE.as_posix()}"
    print(f"[FRONTEND]: Launching SKAI Command Center HUD at:\n{frontend_uri}")
    webbrowser.open(frontend_uri)
    print("\n[SYSTEM ACTIVE]: SKAI running. Founder & Sole Architect: Sumeet Kumar.")

if __name__ == "__main__":
    main()
