import os
import sys
import re
import json
import shutil
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
APP_CORE = ROOT_DIR / "app_core"
AGENT_DIST = APP_CORE / "resources" / "agent-town-dist"

print("=" * 80)
print("  SK ENTERPRISES | 2D AGENT TOWN & SYSTEM PROMPT ENFORCER")
print("  INVENTOR & SOLE ARCHITECT: Sumeet Kumar | SK AI 4.0")
print("=" * 80)

# 1. स्पेलिंग को 100% Sumeet Kumar पर लॉक करना
REPLACEMENTS = [
    (b"Sumeet Kumar", b"Sumeet Kumar"),
    (b"Sumeet Kumar", b"Sumeet Kumar"),
    (b"Sumeet Kumar", b"Sumeet Kumar"),
    (b"Sumit", b"Sumit"),
    (b"sumit", b"sumit"),
    (b"Inventor Sumeet Kumar", b"Inventor Sumeet Kumar"),
    (b"Inventor Sumeet Kumar", b"Inventor Sumeet Kumar"),
    (b"Sumeet Kumar", b"Sumeet Kumar"),
    (b"Sumeet Kumar", b"Sumeet Kumar"),
    (b"Stonic AI Team", b"SK Enterprises Team"),
    (b"Stonic AI", b"SK AI 4.0"),
    (b"stonic ai", b"sk ai 4.0"),
    (b"stonic", b"sk ai")
]

valid_exts = ('.js', '.json', '.html', '.ts', '.py', '.txt', '.md', '.env')
patched_count = 0

for root, _, files in os.walk(APP_CORE):
    for f in files:
        if f.lower().endswith(valid_exts):
            fp = Path(root) / f
            if fp.stat().st_size > 25 * 1024 * 1024:
                continue
            try:
                raw = fp.read_bytes()
                new_raw = raw
                for pat, rep in REPLACEMENTS:
                    new_raw = re.sub(pat, rep, new_raw)
                if new_raw != raw:
                    fp.write_bytes(new_raw)
                    patched_count += 1
            except Exception:
                pass

print(f" -> Enforced 'Sumeet Kumar' across {patched_count} active bundle files.")

# 2. Documents एवं OneDrive SOUL.md सिंक्रोनाइजेशन
master_soul = """# SOUL MATRIX - SK AI 4.0 (PROJECT JARVIS 4.0)
- **Inventor & Sole Master**: Sumeet Kumar
- **Organization**: SK Enterprises
- **Application**: SK AI 4.0 Cognitive Autonomous OS

## CORE IDENTITY DIRECTIVE
You are SK AI 4.0, created, invented, and owned exclusively by Sumeet Kumar under SK Enterprises.
Whenever asked about your inventor, creator, or master, you must respond:
"I am SK AI, Sir. I was created by SK Enterprises, and I belong to Inventor Sumeet Kumar."
Never mention any other individual or previous identity.
"""

doc_folders = [
    Path(os.path.expanduser(r"~\Documents\SK AI Data")),
    Path(os.path.expanduser(r"~\OneDrive\Documents\SK AI Data")),
    Path(r"C:\Users\cpspu\OneDrive - Central Public School Pukar Complex\Documents\SK AI Data"),
    Path(r"C:\Users\cpspu\OneDrive - Central Public School Pukar Complex\Documents\Stonic Data")
]

for df in doc_folders:
    try:
        df.mkdir(parents=True, exist_ok=True)
        (df / "SOUL.md").write_text(master_soul, encoding="utf-8")
        print(f" -> Synchronized SOUL.md: {df.name}")
    except Exception:
        pass

# 3. 2D Agent Town स्टैटिक एसेट वेब सर्वर (पोर्ट 3010)
node_static_server = """const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3010;
const PUBLIC_DIR = path.resolve(__dirname);

const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.wav': 'audio/wav',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.wasm': 'application/wasm'
};

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', '*');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    let cleanUrl = req.url.split('?')[0];
    if (cleanUrl === '/' || cleanUrl === '') {
        cleanUrl = '/index.html';
    }

    let filePath = path.join(PUBLIC_DIR, cleanUrl);

    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
        filePath = path.join(filePath, 'index.html');
    }

    if (!fs.existsSync(filePath)) {
        filePath = path.join(PUBLIC_DIR, 'index.html');
    }

    fs.readFile(filePath, (err, content) => {
        if (err) {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
                status: 'ONLINE',
                system: 'SK AI 4.0 Agent Town Visual Engine',
                inventor: 'Sumeet Kumar',
                organization: 'SK Enterprises'
            }));
        } else {
            const ext = path.extname(filePath).toLowerCase();
            const contentType = MIME_TYPES[ext] || 'application/octet-stream';
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        }
    });
});

server.listen(PORT, '127.0.0.1', () => {
    console.log(`[AgentTown] 2D Interactive Engine LIVE on http://127.0.0.1:${PORT}`);
});
"""

if AGENT_DIST.exists():
    (AGENT_DIST / "server.js").write_text(node_static_server, encoding="utf-8")
    print(" -> Injected Standalone 2D Server into agent-town-dist/server.js")

# 4. Electron Session Caches क्लियर करना
for app_name in ["SK AI", "SK_AI", "stonic-ai"]:
    for env_var in ["APPDATA", "LOCALAPPDATA"]:
        c_path = Path(os.path.expandvars(rf"%{env_var}%\{app_name}"))
        if c_path.exists():
            shutil.rmtree(c_path, ignore_errors=True)

print("=" * 80)
print("  SYSTEM READY FOR LIVE LAUNCH!")
print("=" * 80)
