"""
SK Enterprises | System Paths & Crash Interception Infrastructure
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI — Powered by SK Enterprises
"""
import os
import sys
import ctypes
import traceback
import json
from pathlib import Path

# 1. Bulletproof Dynamic Path Resolution
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# 2. UAC-Safe AppData Directory Mapping
APPDATA_DIR = Path(os.path.expandvars(r"%APPDATA%\SK Enterprises\SKAI"))
LOCALAPPDATA_DIR = Path(os.path.expandvars(r"%LOCALAPPDATA%\SKAI"))

for d in [APPDATA_DIR, LOCALAPPDATA_DIR]:
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

LOGS_DIR = APPDATA_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
CRASH_LOG = LOGS_DIR / "startup_crash.log"
RUNTIME_LOG = LOGS_DIR / "runtime.log"

def get_base_path(relative_path: str) -> Path:
    """Resolve a path relative to BASE_DIR."""
    return BASE_DIR / relative_path

def get_appdata_path(relative_path: str) -> Path:
    """Resolve a path inside writable %APPDATA%."""
    target = APPDATA_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    return target

def show_native_error_dialog(title: str, message: str):
    """Display native Windows MessageBox without crashing silently."""
    try:
        # MB_ICONERROR (0x10) | MB_OK (0x0) | MB_SYSTEMMODAL (0x1000)
        ctypes.windll.user32.MessageBoxW(0, str(message), str(title), 0x10 | 0x0 | 0x1000)
    except Exception:
        print(f"[{title}]: {message}", file=sys.stderr)

def log_crash_and_notify(title: str, exc: Exception):
    """Log full traceback to AppData logs and show native error dialog."""
    tb = traceback.format_exc()
    try:
        with open(CRASH_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n[{title} - Timestamp: {os.times()}]\n")
            f.write(tb)
            f.write("\n" + "=" * 80 + "\n")
    except Exception:
        pass
    
    msg = (
        f"A critical exception occurred in SKAI:\n\n"
        f"{str(exc)}\n\n"
        f"Full crash logs have been saved to:\n{CRASH_LOG}\n\n"
        f"Founder: Sumeet Kumar (SK Enterprises)"
    )
    show_native_error_dialog(title, msg)
