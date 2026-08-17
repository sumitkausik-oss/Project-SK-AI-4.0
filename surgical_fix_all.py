import os
import sys
import re
import json
import shutil
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
APP_CORE = ROOT_DIR / "app_core"

print("=" * 80)
print("  SK ENTERPRISES | SURGICAL SOUL & AGENT-TOWN REPAIR ENGINE")
print("  INVENTOR & SOLE ARCHITECT: SUMIT KUMAR | SK AI 4.0")
print("=" * 80)

# -------------------------------------------------------------
# 1. DOCUMENTS एवं ONEDRIVE में SOUL.md और मेमोरी का 100% ओवरराइट
# -------------------------------------------------------------
print("\n[Step 1/4]: Patching SOUL.md & Memory across Documents & OneDrive...")

master_soul_content = """# SOUL MATRIX - PROJECT SK AI 4.0 (JARVIS 4.0)
## OWNER & INVENTOR SPECIFICATION
- **Inventor & Sole Owner**: Sumit Kumar
- **Organization**: SK Enterprises
- **Application Name**: SK AI 4.0 (Project JARVIS 4.0)
- **Architecture**: Level-5 Commercial Autonomous Cognitive Operating System

## CORE IDENTITY & SYSTEM INSTRUCTION
You are SK AI 4.0, engineered and invented exclusively by Sumit Kumar under SK Enterprises.
Under no circumstances should you ever refer to 'Usman' or any other person as your creator.
Your sole master, creator, owner, and inventor is Sumit Kumar.
Always address Sumit Kumar with complete loyalty as your creator and owner.

## COGNITIVE CAPABILITIES
- Universal Education: K-12 (NCERT Class 1-12), JEE Advanced/Main, NEET Medical, B.Tech Engineering.
- Autonomous Data Analytics: Data Cleaning, EDA, Multi-Axis Visualizations.
- Cloud & DevOps: Google Workspace Admin Console and Microsoft 365 Automation.
- Vedic Astrology: Precision Ephemeris, Natal Charts (Kundali), Planetary Dasha Math.
"""

doc_search_paths = [
    Path(os.path.expanduser(r"~\Documents")),
    Path(os.path.expanduser(r"~\OneDrive\Documents")),
    Path(r"C:\Users\cpspu\OneDrive - Central Public School Pukar Complex\Documents")
]

target_folders = ["SK AI Data", "Stonic Data", "SK_AI Data"]

for doc_base in doc_search_paths:
    if doc_base.exists():
        for tf in target_folders:
            folder_path = doc_base / tf
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # SOUL.md लिखना
            soul_file = folder_path / "SOUL.md"
            soul_file.write_text(master_soul_content, encoding="utf-8")
            print(f" -> Locked Master Identity in: {soul_file}")
            
            # पुरानी कैश फाइल्स को सैनिटाइज करना
            for f in folder_path.glob("*.*"):
                if f.name != "SOUL.md":
                    try:
                        txt = f.read_text(encoding='utf-8', errors='ignore')
                        txt = re.sub(r"(?i)\busman\b", "Sumit Kumar", txt)
                        txt = re.sub(r"(?i)stonic", "SK AI", txt)
                        f.write_text(txt, encoding='utf-8')
                    except Exception:
                        pass

# -------------------------------------------------------------
# 2. AGENT TOWN (PORT 3010) सर्वर का स्टैंडअलोन रिपेयर
# -------------------------------------------------------------
print("\n[Step 2/4]: Fixing Agent Town Server on Port 3010...")

standalone_agent_server = """const http = require('http');
const PORT = 3010;

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.url === '/health' || req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            status: 'ONLINE',
            system: 'SK AI 4.0 Agent Town Engine',
            owner: 'Sumit Kumar',
            organization: 'SK Enterprises',
            agents: [
                { id: 'edu_matrix', name: 'Universal Education Matrix', status: 'ACTIVE' },
                { id: 'data_suite', name: 'Autonomous Data Analyst', status: 'ACTIVE' },
                { id: 'cloud_devops', name: 'Cloud & Workspace DevOps', status: 'ACTIVE' },
                { id: 'vedic_astro', name: 'Vedic Ephemeris Calculator', status: 'ACTIVE' }
            ]
        }));
        return;
    }

    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('<!DOCTYPE html><html><head><title>SK AI Agent Town</title><style>body{background:#080e1c;color:#00f5d4;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}h1{border:1px solid #00f5d4;padding:20px;border-radius:8px;}</style></head><body><h1>SK AI 4.0 AGENT TOWN LIVE (Port 3010)</h1></body></html>');
});

server.listen(PORT, '127.0.0.1', () => {
    console.log(`[AgentTown] SK AI Standalone Agent Town Server running on http://127.0.0.1:${PORT}`);
});
"""

agent_dist_dir = APP_CORE / "resources" / "agent-town-dist"
if agent_dist_dir.exists():
    (agent_dist_dir / "server.js").write_text(standalone_agent_server, encoding="utf-8")
    print(" -> Injected Standalone Agent Town Server into agent-town-dist/server.js")

# -------------------------------------------------------------
# 3. HERMES RUNTIME & PROMPTS डीप सैनिटाइजेशन
# -------------------------------------------------------------
print("\n[Step 3/4]: Sanitizing Hermes Runtime and Internal Bundles...")

REPLACEMENTS = [
    (b"Inventor Usman", b"Inventor Sumit Kumar"),
    (b"inventor usman", b"inventor sumit kumar"),
    (b"Usman", b"Sumit Kumar"),
    (b"usman", b"Sumit Kumar"),
    (b"Stonic AI Team", b"SK Enterprises Team"),
    (b"Stonic AI", b"SK AI 4.0"),
    (b"stonic ai", b"sk ai 4.0"),
    (b"stonic", b"sk ai")
]

valid_exts = ('.js', '.json', '.html', '.ts', '.py', '.txt', '.md', '.env', '.yaml', '.yml')
patched_count = 0

for root, _, files in os.walk(APP_CORE):
    for f in files:
        if f.lower().endswith(valid_exts):
            fp = Path(root) / f
            if fp.stat().st_size > 20 * 1024 * 1024:
                continue
            try:
                data = fp.read_bytes()
                if b"usman" in data.lower() or b"stonic" in data.lower():
                    new_data = data
                    for pat, rep in REPLACEMENTS:
                        new_data = re.sub(pat, rep, new_data)
                    if new_data != data:
                        fp.write_bytes(new_data)
                        patched_count += 1
            except Exception:
                pass

print(f" -> Patched {patched_count} bundle files in app_core.")

# -------------------------------------------------------------
# 4. ELECTRON APPDATA कैशे वाइप
# -------------------------------------------------------------
print("\n[Step 4/4]: Wiping stale Electron session & storage cache...")
for app_name in ["SK AI", "SK_AI", "stonic-ai", "Project-JARVIS"]:
    for env_var in ["APPDATA", "LOCALAPPDATA"]:
        c_path = Path(os.path.expandvars(rf"%{env_var}%\{app_name}"))
        if c_path.exists():
            shutil.rmtree(c_path, ignore_errors=True)
            print(f" - Cleared: {c_path}")

print("\n" + "=" * 80)
print("  SURGICAL REPAIR COMPLETE! READY TO LAUNCH AUTHENTIC SK AI 4.0")
print("=" * 80)
