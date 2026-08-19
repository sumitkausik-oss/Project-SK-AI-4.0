"""
SK Enterprises | Master Desktop Application Lifecycle Coordinator
Founder & Sole Architect: Sumeet Kumar
Platform: Jarvis Platform V5.0
"""
import os
import sys
import time
import socket
import subprocess
import urllib.request
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_FILE = ROOT / "frontend" / "index.html"
if not FRONTEND_FILE.exists():
    FRONTEND_FILE = ROOT / "src_frontend" / "index.html"

BACKEND_MODULE = "backend.main"
BACKEND_FILE = ROOT / "backend" / "main.py"
if not BACKEND_FILE.exists():
    BACKEND_FILE = ROOT / "src_backend" / "main_engine.py"

def is_port_open(port: int = 8000) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_backend_readiness(port: int = 8000) -> bool:
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/v1/health")
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data.get("status") == "HEALTHY"
    except Exception:
        return False
    return False

def recycle_stale_port(port: int = 8000):
    if sys.platform == "win32":
        try:
            res = subprocess.run(
                f"powershell -Command \"(Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue).OwningProcess\"",
                shell=True, capture_output=True, text=True
            )
            pids = [p.strip() for p in res.stdout.splitlines() if p.strip() and p.strip() != '0']
            for pid in pids:
                try:
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
                    print(f"[PROCESS CLEANUP]: Released port {port} by terminating PID {pid}")
                except Exception:
                    pass
        except Exception:
            pass

def launch_desktop():
    print("=" * 80)
    print("⚡ SK ENTERPRISES | SK AI 4.0 (PROJECT JARVIS 4.0)")
    print("   FOUNDER & SOLE ARCHITECT: SUMEET KUMAR | DESKTOP RUNTIME")
    print("=" * 80)

    backend_ready = False

    if is_port_open(8000):
        if check_backend_readiness(8000):
            print("[BACKEND]: Existing SK AI 4.0 FastAPI Engine verified on http://127.0.0.1:8000")
            backend_ready = True
        else:
            print("[PORT RECOVERY]: Stale process found on port 8000. Releasing socket...")
            recycle_stale_port(8000)
            time.sleep(1)

    backend_proc = None
    if not backend_ready:
        print("[BACKEND]: Spawning FastAPI Autonomous Core on http://127.0.0.1:8000...")
        backend_proc = subprocess.Popen([sys.executable, str(BACKEND_FILE)], cwd=str(ROOT))
        
        # Wait up to 6 seconds for backend readiness
        for _ in range(12):
            time.sleep(0.5)
            if check_backend_readiness(8000):
                backend_ready = True
                print("[BACKEND ONLINE]: 5-Layer Intelligence Graph, Agent Registry & Telemetry Active.")
                break

    # Launch Desktop Shell Window
    from desktop.app_window import open_desktop_window
    frontend_uri = f"file:///{FRONTEND_FILE.as_posix()}"
    print(f"[DESKTOP SHELL]: Opening Cyberpunk Command Center HUD at:\n  {frontend_uri}")
    
    try:
        open_desktop_window(frontend_uri, title="SK AI 4.0 | Project JARVIS 4.0 — Sumeet Kumar")
    finally:
        pass

if __name__ == "__main__":
    launch_desktop()
