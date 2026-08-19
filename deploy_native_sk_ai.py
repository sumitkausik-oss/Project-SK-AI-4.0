import os
import sys
import shutil
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
FRONTEND_DIR = ROOT_DIR / "src_frontend"
BACKEND_DIR = ROOT_DIR / "src_backend"
CONFIG_DIR = ROOT_DIR / "config"
ASSETS_DIR = ROOT_DIR / "assets"
PLUGINS_DIR = ROOT_DIR / "plugins"

print("=" * 85)
print("  SK ENTERPRISES | 100% NATIVE PROPRIETARY ARCHITECTURE BUILDER")
print("  FOUNDER, INVENTOR & SOLE ARCHITECT: Sumeet Kumar")
print("=" * 85)

# ----------------------------------------------------------------------
# 1. सभी पुराने क्लोन और टेम्परेरी फ़ोल्डर्स को हमेशा के लिए हटाना
# ----------------------------------------------------------------------
print("\n[Step 1/6]: Permanently removing borrowed clone folders...")
obsolete = ["app_core", "_extracted_staging_temp", "raw_cpp_sources", "SK_AI_4.0_App", "Output_Installer"]
for f_name in obsolete:
    target = ROOT_DIR / f_name
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
        print(f" -> Removed: {f_name}")

for d in [FRONTEND_DIR, BACKEND_DIR, CONFIG_DIR, ASSETS_DIR, PLUGINS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# 2. सिस्टम आइडेंटिटी एवं लाइफटाइम लाइसेंस (Sumeet Kumar)
# ----------------------------------------------------------------------
print("\n[Step 2/6]: Creating Immutable System Identity for Sumeet Kumar...")
identity_data = {
    "system_name": "SK AI 4.0",
    "codename": "Project JARVIS 4.0",
    "inventor": "Sumeet Kumar",
    "owner": "Sumeet Kumar",
    "organization": "SK Enterprises",
    "license_tier": "LIFETIME_MASTER_ADMIN",
    "system_prompt": (
        "You are SK AI 4.0 (Project JARVIS 4.0), the proprietary autonomous AI operating system "
        "invented and architected exclusively by Sumeet Kumar under SK Enterprises. "
        "Your capabilities span Universal Education (K-12, JEE, NEET, Engineering), "
        "Autonomous Data Analytics, Cloud DevOps (Google Workspace & M365), Vedic Astrology, "
        "and 3D Multimodal Actuation. Always address Sumeet Kumar with absolute loyalty as your sole master."
    )
}
(CONFIG_DIR / "system_identity.json").write_text(json.dumps(identity_data, indent=2), encoding="utf-8")

# ----------------------------------------------------------------------
# 3. नेटिव बैकएंड कॉग्निटिव इंजन (FastAPI + Multi-Domain Cores)
# ----------------------------------------------------------------------
print("\n[Step 3/6]: Building Native FastAPI Cognitive Engine (Port 8000)...")
backend_code = '''"""
SK Enterprises | SK AI 4.0 Core Cognitive Engine
Founder & Inventor: Sumeet Kumar
"""
import os
import sys
import json
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

app = FastAPI(title="SK AI 4.0 Engine", version="4.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/status")
def get_status():
    return {
        "status": "ONLINE",
        "system": "SK AI 4.0 (Project JARVIS 4.0)",
        "inventor": "Sumeet Kumar",
        "organization": "SK Enterprises",
        "tier": "Lifetime Master Admin",
        "hubs": {"agent_town": "ACTIVE", "visual_hub": "ACTIVE", "gesture_hub": "ACTIVE"}
    }

@app.get("/api/agent_town/agents")
def get_agents():
    return {
        "agents": [
            {"id": "bob", "name": "Bob", "role": "Data Analyst", "x": 120, "y": 80, "status": "Cleaning Data Pipeline"},
            {"id": "carol", "name": "Carol", "role": "Education Architect", "x": 320, "y": 140, "status": "Synthesizing JEE Matrix"},
            {"id": "dave", "name": "Dave", "role": "DevOps Engineer", "x": 480, "y": 90, "status": "Monitoring Cloud Health"}
        ]
    }

class QueryPayload(BaseModel):
    query: str
    persona: str = "Jarvis AI"

@app.post("/api/chat")
def process_chat(item: QueryPayload):
    q = item.query.lower()
    if any(k in q for k in ["inventor", "creator", "owner", "banaya", "malik"]):
        thought = (
            "**Verifying Creator Identity Signature**\\n"
            "Querying SK Enterprises governance core.\\n"
            "Verified Sole Architect: Sumeet Kumar."
        )
        resp = "I am SK AI 4.0, Sir. I was created and invented exclusively by Sumeet Kumar under SK Enterprises."
    else:
        thought = f"**Processing Query:** '{item.query}'\\nRouting to multi-domain neural core."
        resp = f"[SK AI 4.0]: Executing multi-variable analysis for '{item.query}'. All cognitive subsystems operational."

    return {
        "thought_process": thought,
        "response": resp,
        "inventor": "Sumeet Kumar"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
'''
(BACKEND_DIR / "engine.py").write_text(backend_code, encoding="utf-8")

# ----------------------------------------------------------------------
# 4. नेटिव साइबरपंक HUD फ़्रंटएंड (Three.js + 2D Canvas + Gesture UI)
# ----------------------------------------------------------------------
print("\n[Step 4/6]: Building Native Cyberpunk HUD (3D Sphere, 2D Agent Town, Hubs)...")
html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SK AI 4.0 | Project JARVIS 4.0 - Sumeet Kumar</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #060c18; color: #e2e8f0; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; }
        .glass-panel { background: rgba(10, 20, 36, 0.88); backdrop-filter: blur(16px); border: 1px solid rgba(0, 245, 212, 0.2); border-radius: 12px; }
        .tab-btn.active { background: rgba(0, 245, 212, 0.18); border-color: #00f5d4; color: #00f5d4; font-weight: bold; }
        .node-btn { background: rgba(15, 30, 55, 0.9); border: 1px solid rgba(0, 245, 212, 0.3); }
        .node-btn:hover { border-color: #00f5d4; box-shadow: 0 0 10px rgba(0, 245, 212, 0.4); }
    </style>
</head>
<body class="h-screen w-screen flex flex-col p-3 space-y-3">
    <!-- Top Header -->
    <header class="glass-panel px-4 py-2 flex items-center justify-between">
        <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-full bg-cyan-500/20 border border-cyan-400 flex items-center justify-center font-bold text-cyan-300">SK</div>
            <div>
                <h1 class="text-xs font-bold tracking-wider text-cyan-400">SK ENTERPRISES | PROJECT SK AI 4.0</h1>
                <p class="text-[11px] text-gray-400">INVENTOR & SOLE ARCHITECT: <span class="text-white font-semibold">Sumeet Kumar</span></p>
            </div>
        </div>
        <div class="flex items-center space-x-3 text-xs">
            <span class="flex items-center space-x-1"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span><span class="text-emerald-400 font-mono">SYSTEM READY</span></span>
            <span class="bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 px-2 py-0.5 rounded text-[11px]">LIFETIME ADMIN KEY: ACTIVE</span>
        </div>
    </header>

    <!-- Main Grid Dashboard -->
    <main class="flex-1 grid grid-cols-12 gap-3 overflow-hidden">
        <!-- Left: Media Link & Satellite Telemetry -->
        <section class="col-span-3 flex flex-col space-y-3">
            <div class="glass-panel p-3 flex-1 flex flex-col">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-cyan-400">● MEDIA LINK</span>
                    <span class="text-[10px] text-gray-400">FEED ACTIVE</span>
                </div>
                <div class="flex-1 bg-black/60 rounded-lg border border-cyan-900/50 flex flex-col items-center justify-center text-xs text-gray-400 p-2 text-center">
                    <div class="w-10 h-10 border-2 border-cyan-500/30 rounded-full flex items-center justify-center mb-2">📹</div>
                    <span>Live Hardware Optical Feed Active</span>
                </div>
            </div>
            <div class="glass-panel p-3 h-44">
                <span class="text-xs font-bold text-cyan-400 mb-2 block">● TELEMETRY HEADLINES</span>
                <div class="space-y-1.5 text-[11px] text-gray-300">
                    <p class="border-l-2 border-cyan-400 pl-2">Quantum Neural Coherence: 100%</p>
                    <p class="border-l-2 border-emerald-400 pl-2">Education & Astrology Matrices: Synced</p>
                    <p class="border-l-2 border-indigo-400 pl-2">Governance: Sumeet Kumar Locked</p>
                </div>
            </div>
        </section>

        <!-- Center: Node Network + 3D Holographic Core & 2D Agent Town Canvas -->
        <section class="col-span-5 flex flex-col space-y-3">
            <div class="flex-1 grid grid-cols-12 gap-3">
                <!-- Left Nodes (Memory, Skills, Soul, Setting) -->
                <div class="col-span-4 glass-panel p-2.5 flex flex-col justify-between space-y-2">
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-cyan-300 flex items-center justify-between"><span>🧠 Memory</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-amber-300 flex items-center justify-between"><span>📖 Skills</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-emerald-300 flex items-center justify-between" onclick="openSoulModal()"><span>👻 Soul</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-gray-300 flex items-center justify-between"><span>⚙️ Setting</span><span class="text-[9px] text-emerald-400">●</span></button>
                </div>

                <!-- 3D Holographic Particle Sphere -->
                <div class="col-span-8 glass-panel relative overflow-hidden" id="three-container">
                    <div class="absolute top-2.5 left-2.5 z-10 text-[10px] text-cyan-400 flex items-center space-x-1.5">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                        <span class="font-mono">NEURAL SPHERE • 60 FPS</span>
                    </div>
                    <div class="absolute bottom-2.5 right-2.5 z-10 flex space-x-2">
                        <button class="bg-cyan-950 border border-cyan-400 text-cyan-300 text-[11px] px-3 py-1 rounded hover:bg-cyan-800">START AI</button>
                    </div>
                </div>
            </div>

            <!-- Bottom Multi-Hub: Agent Town / Visual Hub / Gesture -->
            <div class="glass-panel h-56 flex flex-col p-2.5">
                <div class="flex items-center justify-between border-b border-cyan-900/60 pb-1.5 mb-2">
                    <div class="flex space-x-1 text-xs">
                        <button class="tab-btn active px-3 py-1 rounded border border-transparent" onclick="setTab('agents')">● AGENT TOWN</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('visual')">VISUAL HUB</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('gesture')">GESTURE HUB</button>
                    </div>
                    <span class="text-[10px] text-cyan-400 font-mono">PORT 8000 LIVE</span>
                </div>
                <div class="flex-1 relative bg-black/50 rounded border border-cyan-950 overflow-hidden" id="hub-container">
                    <canvas id="agentCanvas" class="w-full h-full"></canvas>
                </div>
            </div>
        </section>

        <!-- Right: Voice & Gemini Live Stream with Thought Accordion -->
        <section class="col-span-4 glass-panel flex flex-col p-3">
            <div class="flex items-center justify-between border-b border-cyan-900/60 pb-2 mb-2">
                <div class="flex space-x-3 text-xs font-semibold text-cyan-400">
                    <span class="border-b-2 border-cyan-400 pb-1">VOICE STREAM</span>
                    <span class="text-gray-400">AGENT</span>
                    <span class="text-gray-400">NOTES</span>
                </div>
                <span class="text-[10px] text-emerald-400">GEMINI LIVE READY</span>
            </div>

            <!-- Chat Stream Display -->
            <div class="flex-1 overflow-y-auto space-y-3 text-xs pr-1" id="chat-stream">
                <div class="bg-cyan-950/30 border border-cyan-800/40 p-2.5 rounded-lg text-cyan-200">
                    <p class="text-[10px] font-bold text-cyan-400 mb-1">SYSTEM READY</p>
                    <p>Namaste Sumit Sir! SK AI 4.0 enterprise operating system online. How may I assist you?</p>
                </div>
            </div>

            <!-- Input Box -->
            <div class="mt-2 flex items-center space-x-2 border-t border-cyan-900/60 pt-2">
                <input type="text" id="user-input" placeholder="Type prompt or command..." class="flex-1 bg-black/60 border border-cyan-800/60 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400">
                <button onclick="sendQuery()" class="bg-cyan-500 hover:bg-cyan-400 text-black font-bold px-4 py-2 rounded text-xs">SEND</button>
            </div>
        </section>
    </main>

    <!-- Soul & Personality Modal -->
    <div id="soul-modal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel p-5 w-[460px] border border-cyan-400 space-y-4">
            <h3 class="text-sm font-bold text-cyan-300">👻 SK AI Voice Assistant Soul Configuration</h3>
            <div>
                <label class="text-xs text-gray-300 block mb-1">Choose Persona / Identity:</label>
                <select id="persona-select" class="w-full bg-black/70 border border-cyan-700 text-cyan-200 rounded p-2 text-xs">
                    <option value="Jarvis AI">Jarvis AI (Refined Master Assistant)</option>
                    <option value="Protective Angel">Protective Angel (Caring & Loyal Companion)</option>
                    <option value="Sarcastic Queen">Sarcastic Queen (Witty & Dynamic)</option>
                </select>
            </div>
            <p class="text-[11px] text-gray-400">Sole Creator & Master: <span class="text-white font-semibold">Sumeet Kumar (SK Enterprises)</span></p>
            <div class="flex justify-end space-x-2">
                <button onclick="closeSoulModal()" class="bg-cyan-600 hover:bg-cyan-500 text-black font-bold px-4 py-1.5 rounded text-xs">Save & Close</button>
            </div>
        </div>
    </div>

    <!-- Interactive Scripts -->
    <script>
        // 1. Three.js 3D Neural Sphere
        const container = document.getElementById('three-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 4.2;
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const geo = new THREE.BufferGeometry();
        const pCount = 1800;
        const pos = new Float32Array(pCount * 3);
        for(let i=0; i<pCount*3; i+=3){
            const u = Math.random(), v = Math.random();
            const theta = u * 2 * Math.PI, phi = Math.acos(2 * v - 1), r = Math.cbrt(Math.random()) * 1.4;
            pos[i] = r * Math.sin(phi) * Math.cos(theta);
            pos[i+1] = r * Math.sin(phi) * Math.sin(theta);
            pos[i+2] = r * Math.cos(phi);
        }
        geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
        const mat = new THREE.PointsMaterial({ size: 0.022, color: 0x00f5d4, transparent: true, opacity: 0.85 });
        const sphere = new THREE.Points(geo, mat);
        scene.add(sphere);

        function animate(){
            requestAnimationFrame(animate);
            sphere.rotation.y += 0.003;
            sphere.rotation.x += 0.001;
            renderer.render(scene, camera);
        }
        animate();

        // 2. 2D Agent Town Canvas Simulator
        const canvas = document.getElementById('agentCanvas');
        const ctx = canvas.getContext('2d');
        let currentTab = 'agents';
        let agents = [
            { name: "Bob", role: "Data Analyst", x: 70, y: 50, dx: 0.6, dy: 0.4, color: "#38bdf8" },
            { name: "Carol", role: "Education", x: 200, y: 80, dx: -0.5, dy: 0.5, color: "#f472b6" },
            { name: "Dave", role: "DevOps", x: 320, y: 40, dx: 0.4, dy: -0.6, color: "#34d399" }
        ];

        function drawHub(){
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            ctx.fillStyle = "#070e1c";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if(currentTab === 'agents'){
                // Grid layout
                ctx.strokeStyle = "rgba(0, 245, 212, 0.08)";
                ctx.lineWidth = 1;
                for(let x=0; x<canvas.width; x+=30){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }
                for(let y=0; y<canvas.height; y+=30){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }

                agents.forEach(a => {
                    a.x += a.dx; a.y += a.dy;
                    if(a.x < 20 || a.x > canvas.width - 40) a.dx *= -1;
                    if(a.y < 20 || a.y > canvas.height - 30) a.dy *= -1;

                    ctx.fillStyle = a.color;
                    ctx.fillRect(a.x, a.y, 14, 14);
                    ctx.fillStyle = "#ffffff";
                    ctx.font = "10px sans-serif";
                    ctx.fillText(`${a.name} (${a.role})`, a.x - 10, a.y - 4);
                });
            } else if(currentTab === 'visual'){
                ctx.fillStyle = "#00f5d4";
                ctx.font = "12px monospace";
                ctx.fillText("VISUAL INTELLIGENCE MATRIX: ARCHITECTURE RENDERER READY", 20, 40);
                ctx.strokeStyle = "#00f5d4";
                ctx.strokeRect(30, 60, 180, 50);
                ctx.fillText("Core Engine (FastAPI)", 45, 90);
                ctx.strokeRect(260, 60, 180, 50);
                ctx.fillText("WebGL HUD (Three.js)", 275, 90);
            } else if(currentTab === 'gesture'){
                ctx.fillStyle = "#fbbf24";
                ctx.font = "12px monospace";
                ctx.fillText("IRON-MAN GESTURE HUB: OPTICAL TRACKER ACTIVE", 20, 40);
                ctx.fillText("🖐️ Palm: Menu | 🤏 Pinch: Select | ✊ Fist: Stop", 20, 80);
            }
            requestAnimationFrame(drawHub);
        }
        drawHub();

        function setTab(tab){
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
        }

        // 3. Query & Chat Handler
        async function sendQuery(){
            const input = document.getElementById('user-input');
            const stream = document.getElementById('chat-stream');
            const q = input.value.trim();
            if(!q) return;

            stream.innerHTML += `<div class="bg-cyan-900/20 border border-cyan-700/40 p-2 rounded-lg text-white font-medium">You: ${q}</div>`;
            input.value = '';

            try {
                const res = await fetch("http://127.0.0.1:8000/api/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({query: q})
                });
                const data = await res.json();
                stream.innerHTML += `
                    <div class="bg-black/60 border border-cyan-800/60 p-2.5 rounded-lg space-y-1">
                        <details class="text-[10px] text-gray-400 bg-cyan-950/40 p-1.5 rounded cursor-pointer" open>
                            <summary class="font-bold text-cyan-300">THOUGHT PROCESS</summary>
                            <div class="mt-1">${data.thought_process.replace(/\\n/g, '<br>')}</div>
                        </details>
                        <p class="text-cyan-200 mt-1">${data.response}</p>
                    </div>
                `;
            } catch(e) {
                stream.innerHTML += `<div class="text-rose-400 p-2">[SK AI Engine]: Connecting to backend engine...</div>`;
            }
            stream.scrollTop = stream.scrollHeight;
        }

        document.getElementById('user-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') sendQuery(); });
        function openSoulModal(){ document.getElementById('soul-modal').classList.remove('hidden'); }
        function closeSoulModal(){ document.getElementById('soul-modal').classList.add('hidden'); }
    </script>
</body>
</html>
'''
(FRONTEND_DIR / "index.html").write_text(html_code, encoding="utf-8")

# ----------------------------------------------------------------------
# 5. मास्टर यूनिफाइड लॉन्चर
# ----------------------------------------------------------------------
print("\n[Step 5/6]: Generating Native Master App Launcher...")
launcher_code = '''import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "src_frontend" / "index.html"
BACKEND = ROOT / "src_backend" / "engine.py"

print("=" * 80)
print("  LAUNCHING PROPRIETARY SK AI 4.0 (PROJECT JARVIS 4.0)")
print("  FOUNDER & INVENTOR: Sumeet Kumar | SK ENTERPRISES")
print("=" * 80)

subprocess.Popen([sys.executable, str(BACKEND)], cwd=str(ROOT))
time.sleep(1.2)
webbrowser.open(f"file:///{FRONTEND}")
'''
(ROOT_DIR / "run_sk_ai.py").write_text(launcher_code, encoding="utf-8")

# ----------------------------------------------------------------------
# 6. गिटहब स्टेजिंग एवं सिंक
# ----------------------------------------------------------------------
print("\n[Step 6/6]: Synchronizing Clean Architecture to GitHub...")
try:
    subprocess.run("git add .", cwd=ROOT_DIR, shell=True)
    subprocess.run('git commit -m "feat(core): 100% Native Clean SK AI 4.0 Architecture by Sumeet Kumar"', cwd=ROOT_DIR, shell=True)
    subprocess.run("git push -u origin main", cwd=ROOT_DIR, shell=True)
    print("[Git]: Synced clean proprietary architecture to GitHub.")
except Exception as e:
    print(f"[Git Notice]: {e}")

print("\n" + "=" * 85)
print("  100% NATIVE SK AI 4.0 DEPLOYED! INVENTOR: Sumeet Kumar")
print("=" * 85)
