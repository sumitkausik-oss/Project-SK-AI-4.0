"""
SK Enterprises | Project SK AI 4.0 Native Launcher
Founder, Inventor & Sole Architect: Sumeet Kumar
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
FRONTEND = ROOT / "src_frontend" / "index.html"
BACKEND = ROOT / "src_backend" / "main_engine.py"

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_backend_healthy() -> bool:
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/system/status")
        with urllib.request.urlopen(req, timeout=1.2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data.get("status") == "ONLINE"
    except Exception:
        pass
    try:
        req2 = urllib.request.Request("http://127.0.0.1:8000/api/status")
        with urllib.request.urlopen(req2, timeout=1.2) as response:
            if response.status == 200:
                return True
    except Exception:
        pass
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
                print(f"[SOCKET RECOVERY]: Freed port {port} (Terminated stale PID {pid})")
            except Exception:
                pass
    except Exception:
        pass

def main():
    print("=" * 85)
    print("  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)")
    print("  FOUNDER, INVENTOR & SOLE ARCHITECT: SUMEET KUMAR")
    print("=" * 85)

    backend_ready = False

    if is_port_in_use(8000):
        if check_backend_healthy():
            print("[BACKEND ONLINE]: Existing SK AI 4.0 Engine active on http://127.0.0.1:8000")
            backend_ready = True
        else:
            print("[SOCKET]: Port 8000 busy with non-responsive process. Cleaning socket...")
            free_port_if_stale(8000)
            time.sleep(1)

    if not backend_ready:
        print("[BACKEND]: Spawning Native Cognitive Core on http://127.0.0.1:8000...")
        subprocess.Popen([sys.executable, str(BACKEND)], cwd=str(ROOT))
        
        for _ in range(8):
            time.sleep(0.4)
            if check_backend_healthy():
                backend_ready = True
                print("[BACKEND READY]: Multi-Domain Cognitive Matrix Online.")
                break

    # Launch WebGL Three.js HUD
    frontend_uri = f"file:///{FRONTEND.as_posix()}"
    print(f"[FRONTEND]: Opening 3D Holographic HUD & 2D Agent Town at:\n{frontend_uri}")
    webbrowser.open(frontend_uri)
    print("\n[SYSTEM LIVE]: SK AI 4.0 Operational. Creator: Sumeet Kumar.")

if __name__ == "__main__":
    main()
