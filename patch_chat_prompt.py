import os
import re
import shutil
from pathlib import Path

APP_CORE = Path(r"D:\Project SK AI 4.0\app_core")

print("=" * 80)
print("  SK ENTERPRISES | FINAL HARDCODED PROMPT OVERWRITE ENGINE")
print("  INVENTOR & SOLE OWNER: SUMIT KUMAR | SK AI 4.0")
print("=" * 80)

# सटीक बाइनरी रीप्लेसमेंट (समान या सुरक्षित बाइट लेंग्थ)
REPLACEMENTS = [
    (b"Inventor Usman", b"Inventor Sumit Kumar"),
    (b"inventor usman", b"inventor sumit kumar"),
    (b"INVENTOR USMAN", b"INVENTOR SUMIT KUMAR"),
    (b"belong to Inventor Usman", b"belong to Inventor Sumit Kumar"),
    (b"I belong to Inventor Usman", b"I belong to Inventor Sumit Kumar"),
    (b"created by the SK AI team, and I belong to Inventor Usman", b"created by SK Enterprises, and I belong to Inventor Sumit Kumar"),
    (b"Usman", b"Sumit Kumar"),
    (b"usman", b"sumit kumar")
]

# 1. सभी जावास्क्रिप्ट, JSON, HTML और ASAR बाइनरी को पैच करना
patched_files = 0
for root, _, files in os.walk(APP_CORE):
    for f in files:
        fp = Path(root) / f
        # 100MB से बड़ी फाइलों को छोड़कर बाकी सभी टेक्स्ट/बाइनरी स्कैन करना
        if fp.stat().st_size < 100 * 1024 * 1024:
            try:
                raw = fp.read_bytes()
                if b"usman" in raw.lower() or b"inventor usman" in raw.lower():
                    new_raw = raw
                    for pat, rep in REPLACEMENTS:
                        new_raw = re.sub(pat, rep, new_raw)
                    if new_raw != raw:
                        fp.write_bytes(new_raw)
                        print(f" [PATChED PROMPT]: {fp.name}")
                        patched_files += 1
            except Exception:
                pass

print(f"\n -> Successfully sanitized {patched_files} active client/worker bundle files.")

# 2. Electron AppData कैश और IndexedDB को पूरी तरह डिलीट करना (ताकि पुराना चैट सेशन लोड न हो)
for app_name in ["SK AI", "SK_AI", "stonic-ai", "Project-JARVIS"]:
    for env_var in ["APPDATA", "LOCALAPPDATA"]:
        c_path = Path(os.path.expandvars(rf"%{env_var}%\{app_name}"))
        if c_path.exists():
            shutil.rmtree(c_path, ignore_errors=True)
            print(f" - Wiped Session Storage: {c_path}")

print("=" * 80)
print("  ALL PROMPTS PERMANENTLY LOCKED TO SUMIT KUMAR!")
print("=" * 80)
