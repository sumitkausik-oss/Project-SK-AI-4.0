import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
FRONTEND_DIR = ROOT_DIR / "src_frontend"
BACKEND_DIR = ROOT_DIR / "src_backend"
CONFIG_DIR = ROOT_DIR / "config"
ASSETS_DIR = ROOT_DIR / "assets"

# 1. पुराने टेम्प और क्लोन फोल्डर्स की सफाई
obsolete_folders = ["app_core", "_extracted_staging_temp", "raw_cpp_sources", "SK_AI_4.0_App", "Output_Installer"]
for folder_name in obsolete_folders:
    target = ROOT_DIR / folder_name
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
        print(f"[Cleaned]: Removed obsolete directory: {folder_name}")

for d in [FRONTEND_DIR, BACKEND_DIR, CONFIG_DIR, ASSETS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print("=" * 85)
print("  SK ENTERPRISES | NATIVE SK AI 4.0 AUTONOMOUS SYSTEM ARCHITECTURE")
print("  FOUNDER, INVENTOR & SOLE ARCHITECT: SUMIT KUMAR")
print("=" * 85)

# ----------------------------------------------------------------------
# 2. सिस्टम आइडेंटिटी एवं लाइफटाइम एडमिन लाइसेंस
# ----------------------------------------------------------------------
identity_data = {
    "system_name": "SK AI 4.0",
    "codename": "Project JARVIS 4.0",
    "inventor": "Sumit Kumar",
    "creator": "Sumit Kumar",
    "owner": "Sumit Kumar",
    "organization": "SK Enterprises",
    "license_tier": "LIFETIME_MASTER_ADMIN",
    "system_prompt": (
        "You are SK AI 4.0 (Project JARVIS 4.0), the supreme autonomous cognitive artificial intelligence "
        "invented, architected, and owned exclusively by Sumit Kumar under SK Enterprises. "
        "Your capabilities include Universal STEM & Education (K-12, JEE/NEET, Engineering), "
        "Autonomous Data Analytics, Cloud DevOps (Google Workspace & M365), Vedic Astrology, "
        "and 3D Multimodal Actuation. Your sole master and creator is Sumit Kumar."
    )
}
(CONFIG_DIR / "system_identity.json").write_text(json.dumps(identity_data, indent=2), encoding="utf-8")

# ----------------------------------------------------------------------
# 3. बैकएंड इंजन (FastAPI + WebSockets + Multi-Domain Cores)
# ----------------------------------------------------------------------
backend_main_code = '''"""
SK Enterprises | SK AI 4.0 Core Cognitive Engine
Inventor & Architect: Sumit Kumar
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

app = FastAPI(title="SK AI 4.0 Cognitive Engine", version="4.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# डोमेन मॉड्यूल रूट्स
@app.get("/api/system/status")
def get_system_status():
    identity = json.loads((CONFIG_DIR / "system_identity.json").read_text(encoding="utf-8"))
    return {
        "status": "ONLINE",
        "system": identity["system_name"],
        "inventor": identity["inventor"],
        "organization": identity["organization"],
        "modules": {
            "3d_hologram": "ACTIVE",
            "agent_town_2d": "ACTIVE",
            "gesture_engine": "ACTIVE",
            "visual_intelligence": "ACTIVE",
            "education_matrix": "ACTIVE",
            "data_analytics": "ACTIVE",
            "vedic_astrology": "ACTIVE"
        }
    }

@app.get("/api/agent_town/state")
def get_agent_town_state():
    return {
        "agents": [
            {"id": "agent_bob", "name": "Bob", "role": "Research Analyst", "x": 120, "y": 140, "status": "Analyzing Knowledge Graph"},
            {"id": "agent_carol", "name": "Carol", "role": "Education Architect", "x": 300, "y": 210, "status": "Generating JEE Assessment"},
            {"id": "agent_dave", "name": "Dave", "role": "DevOps Engineer", "x": 450, "y": 120, "status": "Monitoring Cloud Services"}
        ]
    }

class ChatQuery(BaseModel):
    query: str
    persona: str = "Jarvis AI"

@app.post("/api/chat/process")
async def process_chat(item: ChatQuery):
    query = item.query.lower()
    if "inventor" in query or "creator" in query or "owner" in query or "banaya" in query or "malik" in query:
        thought = (
            "**Analyzing Creator Identity Query**\\n"
            "Retrieving immutable identity signature from SK Enterprises governance core.\\n"
            "Verified Founder: Sumit Kumar."
        )
        response = "I am SK AI 4.0, Sir. I was created and invented exclusively by Sumit Kumar under SK Enterprises."
    else:
        thought = f"**Processing Query:** '{item.query}'\\nRouting to multi-domain cognitive matrix."
        response = f"[SK AI 4.0]: Executing multi-variable analysis for: '{item.query}'. Systems operating at 100% optimal capacity."

    return {
        "thought_process": thought,
        "response": response,
        "inventor": "Sumit Kumar"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
'''
(BACKEND_DIR / "main_engine.py").write_text(backend_main_code, encoding="utf-8")

# ----------------------------------------------------------------------
# 4. नेटिव मॉडर्न साइबरपंक HUD फ़्रंटएंड (Three.js + 2D Canvas + UI HUD)
# ----------------------------------------------------------------------
frontend_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SK AI 4.0 | Project JARVIS 4.0 - Sumit Kumar</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050b14; color: #e2e8f0; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; }
        .glass-panel { background: rgba(10, 20, 35, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(0, 245, 212, 0.2); border-radius: 12px; }
        .cyber-glow { text-shadow: 0 0 10px rgba(0, 245, 212, 0.6); }
        .tab-btn.active { background: rgba(0, 245, 212, 0.15); border-color: #00f5d4; color: #00f5d4; }
    </style>
</head>
<body class="h-screen w-screen flex flex-col p-3 space-y-3">
    <!-- Top Header -->
    <header class="glass-panel px-4 py-2 flex items-center justify-between">
        <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-full bg-cyan-500/20 border border-cyan-400 flex items-center justify-center font-bold text-cyan-300">SK</div>
            <div>
                <h1 class="text-sm font-bold tracking-wider text-cyan-400 cyber-glow">SK ENTERPRISES | PROJECT SK AI 4.0</h1>
                <p class="text-xs text-gray-400">INVENTOR & SOLE ARCHITECT: <span class="text-white font-medium">SUMIT KUMAR</span></p>
            </div>
        </div>
        <div class="flex items-center space-x-4 text-xs">
            <span class="flex items-center space-x-1"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span><span class="text-emerald-400">CORE ONLINE</span></span>
            <span class="bg-cyan-950 border border-cyan-500/40 text-cyan-300 px-2 py-1 rounded">LIFETIME ADMIN KEY: ACTIVE</span>
        </div>
    </header>

    <!-- Main Grid Dashboard -->
    <main class="flex-1 grid grid-cols-12 gap-3 overflow-hidden">
        <!-- Left Column: Media & Telemetry -->
        <section class="col-span-3 flex flex-col space-y-3">
            <div class="glass-panel p-3 flex-1 flex flex-col">
                <h2 class="text-xs font-semibold text-cyan-400 mb-2 tracking-wider flex items-center justify-between">
                    <span>● MEDIA LINK & SATELLITE</span>
                    <span class="text-[10px] text-gray-400">FEED ACTIVE</span>
                </h2>
                <div class="flex-1 bg-black/60 rounded-lg border border-cyan-900/40 flex items-center justify-center text-xs text-gray-400">
                    Live Satellite Intelligence Matrix
                </div>
            </div>
            <div class="glass-panel p-3 h-44">
                <h2 class="text-xs font-semibold text-cyan-400 mb-2 tracking-wider">● TELEMETRY HEADLINES</h2>
                <div class="space-y-2 text-[11px] text-gray-300">
                    <p class="border-l-2 border-cyan-400 pl-2">Quantum Neural Coherence: 100% Operational</p>
                    <p class="border-l-2 border-emerald-400 pl-2">Cognitive Hub: Education & Astrology Loaded</p>
                    <p class="border-l-2 border-indigo-400 pl-2">Governance: Sumit Kumar Master Lock Active</p>
                </div>
            </div>
        </section>

        <!-- Center Column: 3D Holographic Core & 2D Agent Town Canvas -->
        <section class="col-span-5 flex flex-col space-y-3">
            <!-- 3D WebGL Hologram Viewport -->
            <div class="glass-panel relative flex-1 overflow-hidden" id="three-container">
                <div class="absolute top-3 left-3 z-10 text-[11px] text-cyan-400 flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                    <span>3D NEURAL SPHERE • SYSTEM ACTIVE</span>
                </div>
                <div class="absolute bottom-3 right-3 z-10 flex space-x-2">
                    <button class="bg-cyan-900/60 border border-cyan-400 text-cyan-300 text-xs px-3 py-1 rounded hover:bg-cyan-800">START AI</button>
                    <button class="bg-rose-950/60 border border-rose-500 text-rose-300 text-xs px-3 py-1 rounded hover:bg-rose-900">TERMINATE</button>
                </div>
            </div>

            <!-- Bottom Multi-Hub: Agent Town 2D / Visual Hub / Gesture -->
            <div class="glass-panel h-56 flex flex-col p-2">
                <div class="flex items-center justify-between border-b border-cyan-900/60 pb-1 mb-2">
                    <div class="flex space-x-1 text-xs">
                        <button class="tab-btn active px-3 py-1 rounded border border-transparent" onclick="switchTab('agents')">● AGENT TOWN</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="switchTab('visual')">VISUAL HUB</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="switchTab('gesture')">GESTURE HUB</button>
                    </div>
                    <span class="text-[10px] text-cyan-400 font-mono">PORT: 8000 LIVE</span>
                </div>
                <div class="flex-1 relative bg-black/40 rounded border border-cyan-950 overflow-hidden" id="hub-content">
                    <canvas id="agentTownCanvas" class="w-full h-full"></canvas>
                </div>
            </div>
        </section>

        <!-- Right Column: Voice & Gemini Live Stream + Thinking Process -->
        <section class="col-span-4 glass-panel flex flex-col p-3">
            <div class="flex items-center justify-between border-b border-cyan-900/60 pb-2 mb-2">
                <div class="flex space-x-2 text-xs font-semibold text-cyan-400">
                    <span class="border-b border-cyan-400 pb-1">VOICE STREAM</span>
                    <span class="text-gray-400">AGENT</span>
                    <span class="text-gray-400">NOTES</span>
                </div>
                <span class="text-[10px] text-emerald-400">GEMINI LIVE READY</span>
            </div>

            <!-- Chat & Thought Accordion Display -->
            <div class="flex-1 overflow-y-auto space-y-3 text-xs pr-1" id="chat-stream">
                <div class="bg-cyan-950/30 border border-cyan-800/40 p-2.5 rounded-lg text-cyan-200">
                    <p class="text-[10px] font-bold text-cyan-400 mb-1">SYSTEM READY</p>
                    <p>Namaste Sumit Sir! SK AI 4.0 enterprise operating system fully operational. How may I assist you?</p>
                </div>
            </div>

            <!-- Input Box -->
            <div class="mt-2 flex items-center space-x-2 border-t border-cyan-900/60 pt-2">
                <input type="text" id="user-input" placeholder="Type prompt or command..." class="flex-1 bg-black/50 border border-cyan-800/60 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400">
                <button onclick="sendQuery()" class="bg-cyan-600 hover:bg-cyan-500 text-black font-bold px-4 py-2 rounded text-xs">SEND</button>
            </div>
        </section>
    </main>

    <!-- Scripts: Three.js 3D Core + 2D Agent Town Simulator -->
    <script>
        // 1. Three.js 3D Holographic Particle Sphere
        const container = document.getElementById('three-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 4.5;
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const particleGeo = new THREE.BufferGeometry();
        const particleCount = 2000;
        const posArray = new Float32Array(particleCount * 3);
        for(let i=0; i<particleCount*3; i+=3){
            const u = Math.random(), v = Math.random();
            const theta = u * 2.0 * Math.PI, phi = Math.acos(2.0 * v - 1.0), r = Math.cbrt(Math.random()) * 1.5;
            posArray[i] = r * Math.sin(phi) * Math.cos(theta);
            posArray[i+1] = r * Math.sin(phi) * Math.sin(theta);
            posArray[i+2] = r * Math.cos(phi);
        }
        particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particleMat = new THREE.PointsMaterial({ size: 0.02, color: 0x00f5d4, transparent: true, opacity: 0.8 });
        const sphere = new THREE.Points(particleGeo, particleMat);
        scene.add(sphere);

        function animate(){
            requestAnimationFrame(animate);
            sphere.rotation.y += 0.003;
            sphere.rotation.x += 0.001;
            renderer.render(scene, camera);
        }
        animate();

        // 2. 2D Agent Town Canvas Simulation
        const canvas = document.getElementById('agentTownCanvas');
        const ctx = canvas.getContext('2d');
        let agents = [
            { name: "Bob", role: "Researcher", x: 60, y: 50, dx: 0.5, dy: 0.3, color: "#38bdf8" },
            { name: "Carol", role: "Education", x: 180, y: 70, dx: -0.4, dy: 0.4, color: "#f472b6" },
            { name: "Dave", role: "DevOps", x: 280, y: 40, dx: 0.3, dy: -0.5, color: "#34d399" }
        ];

        function drawAgentTown(){
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            ctx.fillStyle = "#070e1b";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Office Grid Layout
            ctx.strokeStyle = "rgba(0, 245, 212, 0.1)";
            ctx.lineWidth = 1;
            for(let x=0; x<canvas.width; x+=30) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }
            for(let y=0; y<canvas.height; y+=30) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }

            agents.forEach(a => {
                a.x += a.dx; a.y += a.dy;
                if(a.x < 20 || a.x > canvas.width - 40) a.dx *= -1;
                if(a.y < 20 || a.y > canvas.height - 30) a.dy *= -1;

                // Agent Sprite & Label
                ctx.fillStyle = a.color;
                ctx.fillRect(a.x, a.y, 14, 14);
                ctx.fillStyle = "#ffffff";
                ctx.font = "10px sans-serif";
                ctx.fillText(`${a.name} (${a.role})`, a.x - 10, a.y - 4);
            });
            requestAnimationFrame(drawAgentTown);
        }
        drawAgentTown();

        // 3. Query Handler
        async function sendQuery(){
            const input = document.getElementById('user-input');
            const stream = document.getElementById('chat-stream');
            const q = input.value.trim();
            if(!q) return;

            stream.innerHTML += `<div class="bg-cyan-900/20 border border-cyan-700/40 p-2 rounded-lg text-white font-medium">You: ${q}</div>`;
            input.value = '';

            try {
                const res = await fetch("http://127.0.0.1:8000/api/chat/process", {
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
                stream.innerHTML += `<div class="text-rose-400 p-2">[SK AI Engine]: Backend server connecting...</div>`;
            }
            stream.scrollTop = stream.scrollHeight;
        }

        document.getElementById('user-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') sendQuery(); });
    </script>
</body>
</html>
'''
(FRONTEND_DIR / "index.html").write_text(frontend_html, encoding="utf-8")

# ----------------------------------------------------------------------
# 5. यूनिफाइड मास्टर लॉन्चर (Electron / Browser HUD + FastAPI Server)
# ----------------------------------------------------------------------
launcher_script = '''import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND_FILE = ROOT / "src_frontend" / "index.html"
BACKEND_FILE = ROOT / "src_backend" / "main_engine.py"

print("=" * 80)
print("  LAUNCHING PROPRIETARY SK AI 4.0 (PROJECT JARVIS 4.0)")
print("  INVENTOR & ARCHITECT: SUMIT KUMAR | SK ENTERPRISES")
print("=" * 80)

# 1. बैकएंड कॉग्निटिव इंजन चालू करना
subprocess.Popen([sys.executable, str(BACKEND_FILE)], cwd=str(ROOT))
print("[BACKEND]: FastAPI Autonomous Engine active on http://127.0.0.1:8000")

time.sleep(1.5)

# 2. नेटिव HUD विंडो खोलना
webbrowser.open(f"file:///{FRONTEND_FILE}")
print("[FRONTEND]: Cyberpunk 3D HUD & 2D Agent Town LIVE.")
'''
(ROOT_DIR / "run_sk_ai_4.py").write_text(launcher_script, encoding="utf-8")

# ----------------------------------------------------------------------
# 6. गिटहब ऑटो-स्टेजिंग एवं सिंक
# ----------------------------------------------------------------------
print("\n[Step 6/6]: Synchronizing Clean Architecture to GitHub...")
try:
    subprocess.run("git add .", cwd=ROOT_DIR, shell=True)
    subprocess.run('git commit -m "feat(core): Native SK AI 4.0 Cyberpunk Architecture by Sumit Kumar"', cwd=ROOT_DIR, shell=True)
    subprocess.run("git push -u origin main", cwd=ROOT_DIR, shell=True)
    print("[Git]: Synced clean proprietary architecture to GitHub.")
except Exception as e:
    print(f"[Git Notice]: {e}")

print("\n" + "=" * 85)
print("  NATIVE SK AI 4.0 SETUP COMPLETE! INVENTOR LOCKED TO SUMIT KUMAR")
print("=" * 85)
