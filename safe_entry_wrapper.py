import os
import sys
import ctypes
import traceback
from pathlib import Path

# 1. डायनामिक पाथ रिजॉल्यूशन (चाहे exe कहीं से भी चले)
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent

# 2. यूएसी सेफ डायरेक्टरी (C:\Program Files राइट ब्लॉक से बचने के लिए)
APPDATA_DIR = Path(os.path.expandvars(r"%APPDATA%\SK Enterprises\SK AI 4.0"))
LOGS_DIR = APPDATA_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
CRASH_LOG = LOGS_DIR / "startup_crash.log"

def show_error_dialog(title, message):
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10 | 0x0)
    except Exception:
        print(f"[{title}]: {message}")

def safe_startup():
    try:
        # एनवायरनमेंट डायरेक्टरी सेट करना
        os.chdir(str(APP_DIR))
        sys.path.insert(0, str(APP_DIR))
        
        # कोर मॉड्यूल्स को सुरक्षित लोड करना
        print("Starting SK AI 4.0 Engine...")
        
        # यदि कोई सब-प्रोसेस या GUI लोड करना हो
        exe_candidates = list(APP_DIR.glob("*.exe")) + list((APP_DIR / "_extracted_staging_temp").rglob("*.exe"))
        for exe in exe_candidates:
            if "main_sk" not in exe.name.lower() and "uninstall" not in exe.name.lower() and "setup" not in exe.name.lower():
                import subprocess
                subprocess.Popen(str(exe), cwd=str(exe.parent))
                return

    except Exception as e:
        err_msg = traceback.format_exc()
        CRASH_LOG.write_text(err_msg, encoding="utf-8")
        show_error_dialog(
            "SK AI 4.0 - Startup Error",
            f"An error occurred while launching SK AI 4.0:\n\n{str(e)}\n\nDetailed crash log saved to:\n{CRASH_LOG}"
        )

if __name__ == "__main__":
    safe_startup()
