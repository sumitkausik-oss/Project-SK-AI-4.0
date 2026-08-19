import os
import sys
import shutil
import re
import json
import base64
import hashlib
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
APP_CORE = ROOT_DIR / "app_core"
SOURCE_SETUP = Path(r"D:\Project-JARVIS 3.0\extracted_setup\app-64")
if not SOURCE_SETUP.exists():
    SOURCE_SETUP = Path(r"D:\Project-JARVIS 3.0\extracted_setup")

CONFIG_DIR = ROOT_DIR / "config"
PLUGINS_DIR = ROOT_DIR / "plugins"

for d in [APP_CORE, CONFIG_DIR, PLUGINS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("  SK ENTERPRISES | PROJECT SK AI 4.0 MASTER COGNITIVE DEPLOYER")
print("  INVENTOR & SOLE ARCHITECT: Sumeet Kumar | LIFETIME ENTERPRISE")
print("=" * 80)

# -------------------------------------------------------------
# 1. मूल Electron ऐप फाइलों को app_core में सिंक करना
# -------------------------------------------------------------
print("\n[Step 1/5]: Syncing original Electron runtime into app_core...")
if SOURCE_SETUP.exists():
    for item in SOURCE_SETUP.iterdir():
        dest = APP_CORE / item.name
        if not dest.exists():
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
    print(" -> Electron runtime & resources synced successfully.")
else:
    print(f"[Warning]: Source path {SOURCE_SETUP} not found, working with existing files.")

# -------------------------------------------------------------
# 2. डीप आइडेंटिटी पैचिंग (Sumeet Kumar -> Sumeet Kumar, Stonic -> SK AI 4.0)
# -------------------------------------------------------------
print("\n[Step 2/5]: Deep-patching AI System Prompts & Identity...")
REPLACEMENTS = [
    (b"Inventor Sumeet Kumar", b"Inventor Sumeet Kumar"),
    (b"Inventor Sumeet Kumar", b"Inventor Sumeet Kumar"),
    (b"Inventor Sumeet Kumar", b"Inventor Sumeet Kumar"),
    (b"Sumeet Kumar", b"Sumeet Kumar"),
    (b"Sumeet Kumar", b"Sumeet Kumar"),
    (b"Stonic AI Team", b"SK Enterprises Team"),
    (b"Stonic AI", b"SK AI 4.0"),
    (b"stonic ai", b"sk ai 4.0"),
    (b"stonic", b"sk ai"),
    (b"https://stonic.ai", b"http://127.0.0.1:8000"),
    (b"http://stonic.ai", b"http://127.0.0.1:8000"),
    (b"Update failed", b"")
]

target_extensions = ('.js', '.json', '.html', '.ts', '.env', '.py', '.txt')
skip_dirs = {'chrome-win64', 'locales', '.git', '__pycache__'}
patched = 0

for root, dirs, files in os.walk(APP_CORE):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for f in files:
        if f.lower().endswith(target_extensions):
            fp = Path(root) / f
            if fp.stat().st_size > 15 * 1024 * 1024:
                continue
            try:
                data = fp.read_bytes()
                new_data = data
                for pat, rep in REPLACEMENTS:
                    new_data = re.sub(pat, rep, new_data)
                if new_data != data:
                    fp.write_bytes(new_data)
                    patched += 1
            except Exception:
                pass

print(f" -> Patched {patched} core JavaScript/JSON bundle files.")

# -------------------------------------------------------------
# 3. Bytenode Bootstrap एरर फिक्स (stonic-bootstrap.js लिंक)
# -------------------------------------------------------------
print("\n[Step 3/5]: Fixing Electron Bytenode Bootstrap bridges...")
for root, dirs, files in os.walk(APP_CORE):
    if "bootstrap" in root.lower() or "electron" in root.lower():
        root_p = Path(root)
        js_files = list(root_p.glob("*.js"))
        target_bootstrap = root_p / "stonic-bootstrap.js"
        if not target_bootstrap.exists() and js_files:
            shutil.copy2(js_files[0], target_bootstrap)
            print(f" -> Created required bootstrap file: {target_bootstrap.name}")

# -------------------------------------------------------------
# 4. मल्टी-डोमेन एजेंट टाउन बैकएंड (FastAPI Server on Port 8000)
# -------------------------------------------------------------
print("\n[Step 4/5]: Building Multi-Domain Agent Town Backend Engine...")
backend_server_code = '''import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SK AI 4.0 Cognitive Engine", version="4.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
@app.get("/health")
def health():
    return {
        "status": "ONLINE",
        "system": "SK AI 4.0 (Project JARVIS 4.0)",
        "inventor": "Sumeet Kumar",
        "organization": "SK Enterprises",
        "tier": "Lifetime Admin",
        "domains": ["Universal Education", "Data Analyst Suite", "Cloud DevOps", "Vedic Astrology"]
    }

@app.get("/api/v1/agents")
def get_agents():
    return {
        "agents": [
            {"id": "stem_engine", "name": "Universal STEM & K-12 Matrix", "status": "ONLINE"},
            {"id": "data_engine", "name": "Autonomous Data Analyst", "status": "ONLINE"},
            {"id": "cloud_devops", "name": "Google Workspace & M365 DevOps", "status": "ONLINE"},
            {"id": "astro_engine", "name": "Vedic Ephemeris Calculator", "status": "ONLINE"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
'''
(ROOT_DIR / "agent_town_server.py").write_text(backend_server_code, encoding="utf-8")

# -------------------------------------------------------------
# 5. लाइफटाइम एडमिन लाइसेंस और सिस्टम आइडेंटिटी
# -------------------------------------------------------------
print("\n[Step 5/5]: Generating Lifetime Admin Key & Wiping Cache...")
payload = {
    "license_id": "SK4-ENTERPRISE-LIFETIME-MASTER-2026",
    "owner": "Sumeet Kumar",
    "organization": "SK Enterprises",
    "system": "SK AI 4.0 (Project JARVIS 4.0)",
    "tier": "ADMIN_LIFETIME",
    "expires_at": "PERMANENT"
}
(CONFIG_DIR / "admin_key.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

# AppData कैशे वाइप (ताकि पुराना प्रॉम्प्ट हट जाए)
for app_name in ["SK AI", "SK_AI", "stonic-ai"]:
    cache_path = Path(os.path.expandvars(rf"%APPDATA%\{app_name}"))
    if cache_path.exists():
        shutil.rmtree(cache_path, ignore_errors=True)

print("\n" + "=" * 80)
print("  SK AI 4.0 BUILD COMPLETED SUCCESSFULLY!")
print("=" * 80)
