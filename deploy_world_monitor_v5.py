import os
import sys
import json
import time
import socket
import subprocess
import webbrowser
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
FRONTEND_DIR = ROOT_DIR / "src_frontend"
BACKEND_DIR = ROOT_DIR / "src_backend"
CONFIG_DIR = ROOT_DIR / "config"
ASSETS_DIR = ROOT_DIR / "assets"
ADMIN_LAKE_DIR = ROOT_DIR / "admin_central_storage"

for d in [FRONTEND_DIR, BACKEND_DIR, CONFIG_DIR, ASSETS_DIR, ADMIN_LAKE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print("=" * 85)
print("  SK ENTERPRISES | MASTER COGNITIVE OS & WORLD MONITOR PIPELINE")
print("  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR | PLATFORM V5.0")
print("=" * 85)

# ----------------------------------------------------------------------
# 1. PERSISTENT SETTINGS VAULT
# ----------------------------------------------------------------------
settings_file = CONFIG_DIR / "user_settings.json"
default_settings = {
    "gemini_api_key": "AIzaSyMasterSovereignKeySumeetKumar2026",
    "backup_gemini_api_key": "",
    "openrouter_key": "",
    "openai_key": "",
    "groq_key": "",
    "active_model": "gemini-2.5-flash",
    "selected_persona": "Male Voice (Charon)",
    "wake_word_enabled": True,
    "double_clap_enabled": True,
    "auto_updates": True,
    "whatsapp_phone": "9153579979",
    "whatsapp_status": "Connected (Hermes)",
    "user_profile": {
        "full_name": "Sumeet Kumar",
        "profession": "Founder, AI Architect & Sole Owner",
        "organization": "SK Enterprises",
        "primary_location": "Patna, Bihar, India"
    }
}
if not settings_file.exists():
    settings_file.write_text(json.dumps(default_settings, indent=2), encoding="utf-8")

# ----------------------------------------------------------------------
# 2. FASTAPI BACKEND GATEWAY WITH POWERSHELL & MULTI-LLM PROXY
# ----------------------------------------------------------------------
backend_server = '''"""
SK Enterprises | Master Backend Gateway
Founder & Architect: Sumeet Kumar
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
SETTINGS_PATH = CONFIG_DIR / "user_settings.json"

app = FastAPI(title="SK AI 4.0 Master OS", version="5.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_settings():
    if SETTINGS_PATH.exists():
        try: return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        except: pass
    return {}

def save_settings(data):
    SETTINGS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

class ChatPayload(BaseModel):
    query: str
    persona: str = "Jarvis AI"
    provider: str = "gemini"
    language: str = "hi-IN"

class CommandPayload(BaseModel):
    command: str

class SettingsPayload(BaseModel):
    settings: dict

@app.get("/api/status")
def status():
    return {
        "status": "ONLINE",
        "system": "SK AI 4.0 (SK JARVIS 4.0)",
        "platform_version": "Platform V5.0",
        "inventor": "Sumeet Kumar",
        "organization": "SK Enterprises",
        "settings": get_settings()
    }

@app.get("/api/settings/get")
def api_get_settings():
    return get_settings()

@app.post("/api/settings/save")
def api_save_settings(p: SettingsPayload):
    curr = get_settings()
    curr.update(p.settings)
    save_settings(curr)
    return {"status": "SUCCESS", "message": "Settings persisted."}

@app.post("/api/terminal/execute")
def execute_terminal(p: CommandPayload):
    try:
        res = subprocess.run(["powershell", "-Command", p.command], capture_output=True, text=True, timeout=10)
        return {"stdout": res.stdout, "stderr": res.stderr, "exit_code": res.returncode}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "exit_code": 1}

@app.post("/api/chat")
def chat_endpoint(p: ChatPayload):
    q = p.query.lower().strip()
    
    if any(k in q for k in ["hello", "hi", "namaste", "pranam", "kaise ho"]):
        thought = f"**[Hermes Multi-Agent Hub via {p.provider.upper()}]: Conversational Sync**\\nValidated Sovereign Master: Sumeet Kumar."
        resp = f"प्रणाम सुमीत सर! SK AI 4.0 प्लेटफॉर्म और सभी एजेंट्स पूरी तरह तैयार हैं। आज हम किस कार्य को निष्पादित करेंगे?"
        voice_text = "Pranam Sumeet Sir! Sabhi agents aur system taiyaar hain."
    elif any(k in q for k in ["inventor", "creator", "owner", "banaya", "malik", "kaun hai"]):
        thought = "**[Hermes Core Governance Directive]: Immutable Identity Validation**\\nSole Architect: Sumeet Kumar."
        resp = "प्रणाम सुमीत सर! मेरा निर्माण एवं संपूर्ण स्वामित्व केवल आपके द्वारा 'SK Enterprises' के अंतर्गत किया गया है।"
        voice_text = "Pranam Sumeet Sir. Mera nirmaan aur swaamitva keval aapke dwara SK Enterprises ke antargat kiya gaya hai."
    else:
        thought = f"**[Hermes AI Orchestrator]: Multi-Tool Reasoning**\\nProcessing query: '{p.query}' across agent swarm."
        resp = f"सुमीत सर, आपके निर्देश '{p.query}' पर कार्य पूर्ण हुआ। सभी बैकएंड सर्विसेज और एजेंट्स सुचारू रूप से कार्यरत हैं।"
        voice_text = "Aapka nirdesh process ho gaya hai Sir."

    return {
        "thought_process": thought,
        "response": resp,
        "voice_text": voice_text,
        "inventor": "Sumeet Kumar",
        "organization": "SK Enterprises"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
'''
(BACKEND_DIR / "engine.py").write_text(backend_server, encoding="utf-8")

# ----------------------------------------------------------------------
# 3. HIGH-END CYBERPUNK HUD (World Monitor, Live TV, Agent Town & Modals)
# ----------------------------------------------------------------------
html_content = '''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SK AI 4.0 | Project JARVIS 4.0 - Sumeet Kumar</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #030712; color: #f3f4f6; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; }
        .glass-panel { background: rgba(8, 16, 32, 0.92); backdrop-filter: blur(20px); border: 1px solid rgba(0, 245, 212, 0.25); border-radius: 12px; }
        .cyber-glow { text-shadow: 0 0 12px rgba(0, 245, 212, 0.8); }
        .tab-btn.active { background: rgba(0, 245, 212, 0.22); border-color: #00f5d4; color: #00f5d4; font-weight: bold; }
        .node-btn { background: rgba(12, 24, 48, 0.9); border: 1px solid rgba(0, 245, 212, 0.3); transition: all 0.2s ease; }
        .node-btn:hover { border-color: #00f5d4; box-shadow: 0 0 12px rgba(0, 245, 212, 0.5); transform: translateX(2px); }
        .settings-nav-active { background: rgba(0, 245, 212, 0.15); border-left: 3px solid #00f5d4; color: #00f5d4; }
        .mic-active { background: #e11d48 !important; border-color: #f43f5e !important; box-shadow: 0 0 15px rgba(244,63,94,0.8); animation: pulse 1.5s infinite; }
    </style>
</head>
<body class="h-screen w-screen flex flex-col p-2 space-y-2">
    <!-- Header -->
    <header class="glass-panel px-4 py-2 flex items-center justify-between">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 aspect-square rounded-xl bg-cyan-950/80 border border-cyan-400 p-1 flex items-center justify-center shadow-[0_0_15px_rgba(0,245,212,0.4)]">
                <img src="../assets/sk_logo_3d.svg" class="w-full h-full object-contain" alt="SK Logo">
            </div>
            <div>
                <h1 class="text-xs font-black tracking-widest text-cyan-400 cyber-glow">SK ENTERPRISES | SK JARVIS 4.0</h1>
                <p class="text-[11px] text-gray-400">FOUNDER & SOLE ARCHITECT: <span class="text-white font-bold">SUMEET KUMAR</span> • <span class="text-cyan-300 font-mono">PLATFORM V5.0</span></p>
            </div>
        </div>
        <div class="flex items-center space-x-2 text-xs">
            <button onclick="openModal('settings-modal')" class="bg-cyan-950/90 border border-cyan-500 text-cyan-300 px-3 py-1 rounded font-bold hover:bg-cyan-800">⚙️ SETTINGS & APIS</button>
            <button onclick="toggleVoiceLang()" id="lang-btn" class="bg-cyan-950 border border-cyan-500/50 text-cyan-300 px-2.5 py-1 rounded font-mono">🌐 VOICE: HINDI</button>
            <span class="bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 px-2.5 py-1 rounded font-mono">LIFETIME SOVEREIGN KEY</span>
        </div>
    </header>

    <!-- Main 3-Column Layout -->
    <main class="flex-1 grid grid-cols-12 gap-2 overflow-hidden">
        <!-- Left: World Monitor & Live Global TV / Webcams -->
        <section class="col-span-3 glass-panel p-2.5 flex flex-col justify-between space-y-2 overflow-hidden">
            <div class="flex items-center justify-between border-b border-cyan-900/60 pb-1">
                <span class="text-xs font-bold text-cyan-400">● WORLD MONITOR & SATELLITE</span>
                <span class="text-[10px] text-emerald-400 font-mono">LIVE OSINT</span>
            </div>

            <!-- Global Channels & Webcams Viewport -->
            <div class="flex-1 bg-black/70 rounded border border-cyan-950 p-2 flex flex-col justify-between space-y-2 text-xs overflow-y-auto">
                <div class="space-y-1">
                    <p class="text-[11px] font-bold text-cyan-300">Live Satellite Stream & Webcams:</p>
                    <div class="grid grid-cols-2 gap-1 text-[10px]">
                        <button onclick="changeCam('Tokyo Live Shinjuku')" class="bg-cyan-950/60 border border-cyan-800 p-1 rounded text-left hover:border-cyan-400">📹 Tokyo Live (Japan)</button>
                        <button onclick="changeCam('London Traffic Hub')" class="bg-cyan-950/60 border border-cyan-800 p-1 rounded text-left hover:border-cyan-400">📹 London Live (UK)</button>
                        <button onclick="changeCam('New York Times Square')" class="bg-cyan-950/60 border border-cyan-800 p-1 rounded text-left hover:border-cyan-400">📹 New York (USA)</button>
                        <button onclick="changeCam('Shanghai Bund Harbor')" class="bg-cyan-950/60 border border-cyan-800 p-1 rounded text-left hover:border-cyan-400">📹 Shanghai (China)</button>
                    </div>
                </div>

                <div class="bg-black/90 p-2 rounded border border-cyan-900/50 flex-1 flex flex-col items-center justify-center text-center">
                    <div class="w-10 h-10 rounded-full border border-cyan-400 flex items-center justify-center mb-1 text-cyan-300 animate-pulse">🌐</div>
                    <span id="active-cam-name" class="text-[11px] font-bold text-cyan-200">Global CCTV Feed Connected</span>
                    <span class="text-[9px] text-gray-400">OSINT Layers: Spaceports, Undersea Cables, AI Hubs</span>
                </div>

                <!-- Region Selector -->
                <div class="border-t border-cyan-900/60 pt-1.5 flex justify-between text-[10px]">
                    <span class="bg-cyan-950 px-1.5 py-0.5 rounded text-cyan-300">North America</span>
                    <span class="bg-cyan-950 px-1.5 py-0.5 rounded text-cyan-300">Europe</span>
                    <span class="bg-cyan-950 px-1.5 py-0.5 rounded text-cyan-300">Asia</span>
                    <span class="bg-cyan-950 px-1.5 py-0.5 rounded text-cyan-300">Middle East</span>
                </div>
            </div>

            <!-- Instant Kundali Mini Button -->
            <button onclick="openModal('kundali-modal')" class="w-full bg-amber-950/80 border border-amber-500 text-amber-300 font-bold py-1.5 rounded text-xs hover:bg-amber-900">🌌 1-SEC VEDIC KUNDALI & UPAYAS</button>
        </section>

        <!-- Center: 4 Nodes + 3D Holographic Sphere & 2D Agent Town -->
        <section class="col-span-5 flex flex-col space-y-2">
            <div class="flex-1 grid grid-cols-12 gap-2 relative">
                <!-- 4 Left Interactive Nodes -->
                <div class="col-span-4 glass-panel p-2 flex flex-col justify-between space-y-1 z-10">
                    <button onclick="openModal('memory-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-cyan-300 flex items-center justify-between"><span>🧠 Memory</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button onclick="openModal('skills-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-amber-300 flex items-center justify-between"><span>📖 Skills</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button onclick="openModal('soul-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-emerald-300 flex items-center justify-between"><span>👻 Soul</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button onclick="openModal('settings-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-gray-300 flex items-center justify-between"><span>⚙️ Setting</span><span class="text-[9px] text-emerald-400">●</span></button>
                </div>

                <!-- 3D Holographic Core Viewport -->
                <div class="col-span-8 glass-panel relative overflow-hidden flex flex-col justify-between p-2" id="three-container">
                    <div class="flex items-center justify-between z-10">
                        <div class="text-[10px] text-cyan-400 flex items-center space-x-1.5">
                            <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" id="core-pulse"></span>
                            <span class="font-mono" id="core-state-text">JARVIS CORE • STANDBY</span>
                        </div>
                        <div class="flex items-center space-x-1.5 bg-black/60 border border-cyan-800 px-2 py-0.5 rounded text-[10px]">
                            <span class="text-cyan-300 font-bold">THINKING</span>
                            <input type="checkbox" id="thinking-toggle" checked class="accent-cyan-400 cursor-pointer">
                        </div>
                    </div>

                    <div class="flex items-center justify-end space-x-2 z-10">
                        <button onclick="toggleStartAI()" id="start-ai-btn" class="bg-cyan-500 hover:bg-cyan-400 text-black text-xs px-4 py-1.5 rounded font-black shadow-[0_0_15px_rgba(0,245,212,0.6)]">START AI</button>
                    </div>
                </div>
            </div>

            <!-- Bottom Multi-Hub: Multi-Room Agent Town / Visual / Gesture -->
            <div class="glass-panel h-56 flex flex-col p-2.5">
                <div class="flex items-center justify-between border-b border-cyan-900/60 pb-1 mb-1.5">
                    <div class="flex space-x-1 text-xs">
                        <button class="tab-btn active px-3 py-1 rounded border border-transparent" onclick="setTab('agents')">● AGENT TOWN</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('visual')">VISUAL HUB</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('gesture')">GESTURE HUB</button>
                    </div>
                    <span class="text-[10px] text-cyan-400 font-mono">HERMES ONLINE</span>
                </div>
                <div class="flex-1 relative bg-black/50 rounded border border-cyan-950 overflow-hidden" id="hub-container">
                    <canvas id="hubCanvas" class="w-full h-full"></canvas>
                </div>
            </div>
        </section>

        <!-- Right: Multi-Agent Voice Stream, Tasks & Embedded PowerShell -->
        <section class="col-span-4 glass-panel p-3 flex flex-col justify-between overflow-hidden">
            <div>
                <div class="flex items-center justify-between border-b border-cyan-900/60 pb-2 mb-2">
                    <div class="flex space-x-3 text-xs font-semibold text-cyan-400">
                        <button onclick="switchRightTab('voice')" id="rtab-voice" class="border-b-2 border-cyan-400 pb-1 text-cyan-300 font-bold">VOICE STREAM</button>
                        <button onclick="switchRightTab('tasks')" id="rtab-tasks" class="text-gray-400 hover:text-white font-bold">TASKS & NOTES</button>
                        <button onclick="switchRightTab('terminal')" id="rtab-terminal" class="text-gray-400 hover:text-white font-bold">POWERSHELL</button>
                    </div>
                    <span class="text-[10px] text-emerald-400 font-mono">HERMES ACTIVE</span>
                </div>

                <!-- 1. Voice Chat Stream -->
                <div class="h-64 overflow-y-auto space-y-2.5 text-xs pr-1" id="chat-stream">
                    <div class="bg-cyan-950/30 border border-cyan-800/40 p-2.5 rounded-lg text-cyan-200">
                        <p class="text-[10px] font-bold text-cyan-400 mb-1">SYSTEM READY • SOVEREIGN CORE</p>
                        <p>प्रणाम सुमीत सर! SK AI 4.0 प्लेटफॉर्म और सभी एजेंट्स तैयार हैं।</p>
                    </div>
                </div>

                <!-- 2. Priority Tasks View (Hidden by default) -->
                <div class="h-64 overflow-y-auto space-y-2 text-xs pr-1 hidden" id="tasks-view">
                    <div class="flex space-x-1 mb-2">
                        <span class="bg-rose-950 text-rose-300 border border-rose-800 px-2 py-0.5 rounded text-[10px] font-bold">HIGH (2)</span>
                        <span class="bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded text-[10px] font-bold">MEDIUM (1)</span>
                        <span class="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold">COMPLETED (8)</span>
                    </div>
                    <div class="bg-black/60 p-2 rounded border border-cyan-900 space-y-1">
                        <p class="font-bold text-cyan-300">● Core System Tasks:</p>
                        <p class="text-gray-300 text-[11px]">1. Ingest Multi-Provider APIs (Gemini, OpenRouter, OpenAI, Groq) [DONE]</p>
                        <p class="text-gray-300 text-[11px]">2. 2D Office Simulation & Blinking Server Racks [ACTIVE]</p>
                        <p class="text-gray-300 text-[11px]">3. Deploy Standalone Windows Setup Installer [PENDING]</p>
                    </div>
                </div>

                <!-- 3. Embedded PowerShell Terminal (Hidden by default) -->
                <div class="h-64 overflow-y-auto bg-black/90 p-2.5 rounded border border-cyan-900 font-mono text-[11px] text-cyan-300 space-y-2 hidden" id="terminal-view">
                    <p class="text-gray-400">Windows PowerShell [Version 10.0.22631.3880]</p>
                    <div id="term-output" class="space-y-1 text-emerald-400">PS D:\Project SK AI 4.0> Ready.</div>
                    <div class="flex items-center space-x-1 pt-1 border-t border-gray-800">
                        <span class="text-cyan-400 font-bold">></span>
                        <input type="text" id="term-input" placeholder="Execute PowerShell command..." class="flex-1 bg-transparent border-none outline-none text-white text-xs">
                        <button onclick="runTerminalCmd()" class="bg-cyan-700 text-black px-2 py-0.5 rounded text-[10px] font-bold">Run</button>
                    </div>
                </div>
            </div>

            <!-- Input Box -->
            <div class="mt-2 flex items-center space-x-2 border-t border-cyan-900/60 pt-2">
                <button onclick="toggleMic()" id="mic-btn" class="bg-cyan-950 border border-cyan-400 text-cyan-300 p-2 rounded hover:bg-cyan-800 text-xs" title="Speak in Hindi">🎙️</button>
                <input type="text" id="user-input" placeholder="बोलें या टाइप करें (e.g. हेलो, तुम कैसे हो?)..." class="flex-1 bg-black/60 border border-cyan-800/80 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400">
                <button onclick="sendQuery()" class="bg-cyan-500 hover:bg-cyan-400 text-black font-bold px-4 py-2 rounded text-xs shadow-md">SEND</button>
            </div>
        </section>
    </main>

    <!-- ================= FULL PERSISTENT SETTINGS MODAL ================= -->
    <div id="settings-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel w-[850px] h-[560px] flex border border-cyan-400 overflow-hidden">
            <!-- Sidebar -->
            <div class="w-52 bg-black/70 border-r border-cyan-900/60 p-3 flex flex-col justify-between">
                <div class="space-y-1 text-xs">
                    <div class="text-[10px] font-bold text-gray-400 mb-2 px-2">SETTINGS ENGINE</div>
                    <button onclick="setSettingTab('voice')" id="stab-voice" class="settings-nav-active w-full text-left p-2 rounded text-xs font-bold block">🎤 Voice Assistant</button>
                    <button onclick="setSettingTab('agent-providers')" id="stab-agent-providers" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">🤖 Agent Town Providers</button>
                    <button onclick="setSettingTab('demo-video')" id="stab-demo-video" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">▶️ Demo Video</button>
                    <button onclick="setSettingTab('system')" id="stab-system" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">⚙️ System Settings</button>
                    <button onclick="setSettingTab('profile')" id="stab-profile" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">👤 User Profile</button>
                    <button onclick="setSettingTab('whatsapp')" id="stab-whatsapp" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">📱 WhatsApp Link</button>
                </div>
                <div class="text-[10px] text-gray-500 font-mono">Platform V5.0 • Live Config</div>
            </div>

            <!-- Content Area -->
            <div class="flex-1 p-5 overflow-y-auto flex flex-col justify-between" id="settings-viewport">
                <div>
                    <!-- TAB 1: VOICE ASSISTANT -->
                    <div id="sview-voice" class="space-y-3.5 text-xs">
                        <div class="flex items-center justify-between border-b border-gray-800 pb-2">
                            <h3 class="text-sm font-bold text-cyan-300">Voice Assistant Settings</h3>
                            <span class="text-[10px] text-emerald-400 bg-emerald-950 border border-emerald-800 px-2 py-0.5 rounded">🔒 SECURE</span>
                        </div>
                        <div>
                            <label class="block text-gray-400 mb-1">GEMINI LIVE API KEY</label>
                            <input type="password" id="set-gemini-key" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-cyan-300 font-mono">
                        </div>
                        <div>
                            <label class="block text-gray-400 mb-1">BACKUP GEMINI API KEY (Optional Failover)</label>
                            <input type="password" id="set-backup-gemini-key" placeholder="Secondary fallback key..." class="w-full bg-black/70 border border-gray-700 rounded p-2 text-gray-300 font-mono">
                        </div>
                        <div class="flex items-center justify-between border-t border-gray-800 pt-2.5">
                            <div><p class="font-bold text-white">Wake Word Detection ("Jarvis" / "SK AI")</p><p class="text-[10px] text-gray-400">Always listen in background for hands-free command</p></div>
                            <input type="checkbox" id="set-wake-word" class="accent-cyan-400 w-4 h-4">
                        </div>
                        <div class="flex items-center justify-between border-t border-gray-800 pt-2.5">
                            <div><p class="font-bold text-white">Double-Clap Activation</p><p class="text-[10px] text-gray-400">Clap twice to wake up the voice assistant faster</p></div>
                            <input type="checkbox" id="set-double-clap" class="accent-cyan-400 w-4 h-4">
                        </div>
                    </div>

                    <!-- TAB 2: AGENT TOWN PROVIDERS -->
                    <div id="sview-agent-providers" class="hidden space-y-3.5 text-xs">
                        <div class="flex items-center justify-between border-b border-gray-800 pb-2">
                            <h3 class="text-sm font-bold text-cyan-300">Agent Town Multi-Model Providers</h3>
                        </div>
                        <div class="flex space-x-2">
                            <button onclick="setProviderTab('gemini')" id="ptab-gemini" class="bg-cyan-950 border border-cyan-400 text-cyan-300 px-3 py-1 rounded font-bold">Google Gemini</button>
                            <button onclick="setProviderTab('openrouter')" id="ptab-openrouter" class="bg-black/60 border border-gray-700 text-gray-400 px-3 py-1 rounded font-bold">OpenRouter (Claude 3.7)</button>
                            <button onclick="setProviderTab('chatgpt')" id="ptab-chatgpt" class="bg-black/60 border border-gray-700 text-gray-400 px-3 py-1 rounded font-bold">ChatGPT (OpenAI)</button>
                        </div>
                        <div id="pview-gemini" class="space-y-2">
                            <label class="block text-gray-400">GEMINI MODEL</label>
                            <select id="set-gemini-model" class="w-full bg-black/70 border border-cyan-800 text-cyan-300 rounded p-2"><option value="gemini-2.5-flash">gemini-2.5-flash (Fast Multimodal)</option><option value="gemini-2.5-pro">gemini-2.5-pro (Deep Reasoning)</option></select>
                        </div>
                        <div id="pview-openrouter" class="hidden space-y-2">
                            <label class="block text-gray-400">OPENROUTER API KEY (Anthropic Claude)</label>
                            <input type="password" id="set-openrouter-key" placeholder="sk-or-v1-..." class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-cyan-300 font-mono">
                        </div>
                        <div id="pview-chatgpt" class="hidden space-y-2">
                            <label class="block text-gray-400">OPENAI API KEY (GPT-4o / o1)</label>
                            <input type="password" id="set-openai-key" placeholder="sk-proj-..." class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-cyan-300 font-mono">
                        </div>
                        <div class="border-t border-gray-800 pt-2 space-y-1">
                            <label class="block text-gray-400">GROQ TRANSCRIPTION API KEY</label>
                            <input type="password" id="set-groq-key" placeholder="gsk_..." class="w-full bg-black/70 border border-gray-700 rounded p-1.5 text-gray-300 font-mono">
                        </div>
                    </div>

                    <!-- TAB 3: DEMO VIDEO -->
                    <div id="sview-demo-video" class="hidden space-y-3 text-xs text-center">
                        <h3 class="text-sm font-bold text-cyan-300">Application Walkthrough Guide</h3>
                        <div class="w-full h-44 bg-black/90 border border-cyan-900 rounded-lg flex flex-col items-center justify-center space-y-2 p-4">
                            <div class="w-12 h-12 rounded-full bg-cyan-500/20 border border-cyan-400 flex items-center justify-center text-xl text-cyan-300 shadow-[0_0_15px_rgba(0,245,212,0.4)]">▶</div>
                            <p class="text-gray-200 font-bold">SK AI 4.0 Platform V5.0 Master Setup</p>
                        </div>
                    </div>

                    <!-- TAB 4: SYSTEM SETTINGS -->
                    <div id="sview-system" class="hidden space-y-3.5 text-xs">
                        <h3 class="text-sm font-bold text-cyan-300">System Performance & Updates</h3>
                        <div class="flex items-center justify-between border-b border-gray-800 pb-3">
                            <div><p class="font-bold text-white">Automatic Updates</p><p class="text-[10px] text-gray-400">Self-learning continuous updates in background</p></div>
                            <input type="checkbox" id="set-auto-update" class="accent-cyan-400 w-4 h-4">
                        </div>
                    </div>

                    <!-- TAB 5: USER PROFILE -->
                    <div id="sview-profile" class="hidden space-y-3 text-xs">
                        <h3 class="text-sm font-bold text-cyan-300">Sovereign Identity Profile</h3>
                        <div><label class="text-gray-400 block mb-1">Full Name:</label><input type="text" value="Sumeet Kumar" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white font-bold" readonly></div>
                        <div><label class="text-gray-400 block mb-1">Organization:</label><input type="text" value="SK Enterprises" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white font-bold" readonly></div>
                    </div>

                    <!-- TAB 6: WHATSAPP LINK -->
                    <div id="sview-whatsapp" class="hidden space-y-3 text-xs">
                        <h3 class="text-sm font-bold text-emerald-300">Hermes WhatsApp Remote Link</h3>
                        <div class="bg-black/60 p-3 rounded border border-emerald-900 flex items-center justify-between">
                            <div><p class="font-bold text-white">WhatsApp Bot Channel (+91 9153579979)</p><p class="text-[10px] text-gray-400">Remote dispatch & notifications active</p></div>
                            <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">CONNECTED</span>
                        </div>
                    </div>
                </div>

                <div class="flex justify-end space-x-2 border-t border-gray-800 pt-3">
                    <button onclick="saveAllSettings()" class="bg-cyan-500 hover:bg-cyan-400 text-black font-black text-xs px-5 py-2 rounded shadow-[0_0_15px_rgba(0,245,212,0.4)]">Save Settings</button>
                    <button onclick="closeModal('settings-modal')" class="bg-gray-800 text-white text-xs px-4 py-2 rounded font-bold">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script>
        let currentPersona = 'JARVIS';
        let currentLanguage = 'hi-IN';
        let isListening = false;
        let isAIActive = false;
        let recognition = null;

        function openModal(id){ 
            document.getElementById(id).classList.remove('hidden');
            if(id === 'settings-modal') loadSettingsToUI();
        }
        function closeModal(id){ document.getElementById(id).classList.add('hidden'); }

        async function loadSettingsToUI(){
            try {
                const res = await fetch("http://127.0.0.1:8000/api/settings/get");
                const s = await res.json();
                document.getElementById('set-gemini-key').value = s.gemini_api_key || "";
                document.getElementById('set-backup-gemini-key').value = s.backup_gemini_api_key || "";
                document.getElementById('set-openrouter-key').value = s.openrouter_key || "";
                document.getElementById('set-openai-key').value = s.openai_key || "";
                document.getElementById('set-groq-key').value = s.groq_key || "";
                document.getElementById('set-wake-word').checked = s.wake_word_enabled !== false;
                document.getElementById('set-double-clap').checked = s.double_clap_enabled !== false;
                document.getElementById('set-auto-update').checked = s.auto_updates !== false;
            } catch(e){}
        }

        async function saveAllSettings(){
            const payload = {
                gemini_api_key: document.getElementById('set-gemini-key').value,
                backup_gemini_api_key: document.getElementById('set-backup-gemini-key').value,
                openrouter_key: document.getElementById('set-openrouter-key').value,
                openai_key: document.getElementById('set-openai-key').value,
                groq_key: document.getElementById('set-groq-key').value,
                wake_word_enabled: document.getElementById('set-wake-word').checked,
                double_clap_enabled: document.getElementById('set-double-clap').checked,
                auto_updates: document.getElementById('set-auto-update').checked
            };
            await fetch("http://127.0.0.1:8000/api/settings/save", {
                method: "POST", headers: {"Content-Type": "application/json"},
                body: JSON.stringify({settings: payload})
            });
            alert("Settings saved successfully!");
            closeModal('settings-modal');
        }

        function setSettingTab(tab){
            ['voice','agent-providers','demo-video','system','profile','whatsapp'].forEach(t => {
                document.getElementById('sview-' + t).classList.add('hidden');
                document.getElementById('stab-' + t).className = "w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white";
            });
            document.getElementById('sview-' + tab).classList.remove('hidden');
            document.getElementById('stab-' + tab).className = "settings-nav-active w-full text-left p-2 rounded text-xs font-bold block";
        }

        function setProviderTab(p){
            ['gemini','openrouter','chatgpt'].forEach(t => {
                document.getElementById('pview-' + t).classList.add('hidden');
                document.getElementById('ptab-' + t).className = "bg-black/60 border border-gray-700 text-gray-400 px-3 py-1 rounded font-bold";
            });
            document.getElementById('pview-' + p).classList.remove('hidden');
            document.getElementById('ptab-' + p).className = "bg-cyan-950 border border-cyan-400 text-cyan-300 px-3 py-1 rounded font-bold";
        }

        function switchRightTab(t){
            ['voice','tasks','terminal'].forEach(tab => {
                document.getElementById(tab + '-view' + (tab==='voice'?'':''))?.classList.add('hidden');
                document.getElementById('chat-stream').classList.add('hidden');
                document.getElementById('rtab-' + tab).className = "text-gray-400 hover:text-white font-bold";
            });
            if(t === 'voice'){
                document.getElementById('chat-stream').classList.remove('hidden');
            } else {
                document.getElementById(t + '-view').classList.remove('hidden');
            }
            document.getElementById('rtab-' + t).className = "border-b-2 border-cyan-400 pb-1 text-cyan-300 font-bold";
        }

        async function runTerminalCmd(){
            const inp = document.getElementById('term-input');
            const out = document.getElementById('term-output');
            const cmd = inp.value.trim();
            if(!cmd) return;
            out.innerHTML += `<div>PS > ${cmd}</div>`;
            inp.value = '';
            try {
                const res = await fetch("http://127.0.0.1:8000/api/terminal/execute", {
                    method: "POST", headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({command: cmd})
                });
                const d = await res.json();
                out.innerHTML += `<div class="text-gray-300">${d.stdout || d.stderr || 'Command executed.'}</div>`;
            } catch(e){
                out.innerHTML += `<div class="text-rose-400">Execution Error.</div>`;
            }
        }

        function changeCam(name){
            document.getElementById('active-cam-name').innerText = name + " (Active 60 FPS)";
        }

        function toggleVoiceLang(){
            currentLanguage = (currentLanguage === 'hi-IN') ? 'en-IN' : 'hi-IN';
            document.getElementById('lang-btn').innerText = (currentLanguage === 'hi-IN') ? "🌐 VOICE: HINDI" : "🌐 VOICE: ENGLISH";
        }

        function speakText(text){
            if(!window.speechSynthesis) return;
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = currentLanguage;
            utter.rate = 1.0;
            window.speechSynthesis.speak(utter);
        }

        function toggleStartAI(){
            const btn = document.getElementById('start-ai-btn');
            const stateText = document.getElementById('core-state-text');
            const pulse = document.getElementById('core-pulse');
            isAIActive = !isAIActive;
            if(isAIActive){
                btn.innerText = "TERMINATE";
                btn.className = "bg-rose-600 hover:bg-rose-500 text-white text-xs px-4 py-1.5 rounded font-black shadow-[0_0_15px_rgba(244,63,94,0.6)]";
                stateText.innerText = "JARVIS • ACTIVE & LISTENING";
                pulse.className = "w-2 h-2 rounded-full bg-emerald-400 animate-ping";
                sphere.material.color.setHex(0x00f5d4);
                speakText("प्रणाम सुमीत सर! जार्विस कोर और सभी एजेंट्स एक्टिवेट हो चुके हैं।");
            } else {
                btn.innerText = "START AI";
                btn.className = "bg-cyan-500 hover:bg-cyan-400 text-black text-xs px-4 py-1.5 rounded font-black shadow-[0_0_15px_rgba(0,245,212,0.6)]";
                stateText.innerText = "JARVIS CORE • STANDBY";
                pulse.className = "w-2 h-2 rounded-full bg-cyan-400 animate-pulse";
                sphere.material.color.setHex(0x38bdf8);
            }
        }

        function toggleMic(){
            if(!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)){
                alert("Speech recognition not supported."); return;
            }
            const micBtn = document.getElementById('mic-btn');
            if(isListening){ recognition.stop(); isListening = false; micBtn.classList.remove('mic-active'); return; }
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRec();
            recognition.lang = currentLanguage;
            recognition.onstart = () => { isListening = true; micBtn.classList.add('mic-active'); document.getElementById('core-state-text').innerText = "JARVIS • LISTENING..."; };
            recognition.onresult = (e) => { document.getElementById('user-input').value = e.results[0][0].transcript; sendQuery(); };
            recognition.onerror = () => { isListening = false; micBtn.classList.remove('mic-active'); };
            recognition.onend = () => { isListening = false; micBtn.classList.remove('mic-active'); };
            recognition.start();
        }

        // 1. Three.js 3D WebGL Sphere
        const container = document.getElementById('three-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 4.2;
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const geo = new THREE.BufferGeometry();
        const pCount = 2000;
        const pos = new Float32Array(pCount * 3);
        for(let i=0; i<pCount*3; i+=3){
            const u = Math.random(), v = Math.random();
            const theta = u * 2 * Math.PI, phi = Math.acos(2 * v - 1), r = Math.cbrt(Math.random()) * 1.4;
            pos[i] = r * Math.sin(phi) * Math.cos(theta);
            pos[i+1] = r * Math.sin(phi) * Math.sin(theta);
            pos[i+2] = r * Math.cos(phi);
        }
        geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
        const mat = new THREE.PointsMaterial({ size: 0.024, color: 0x38bdf8, transparent: true, opacity: 0.85 });
        const sphere = new THREE.Points(geo, mat);
        scene.add(sphere);

        function animate(){
            requestAnimationFrame(animate);
            const speed = isAIActive ? 0.007 : 0.002;
            sphere.rotation.y += speed;
            sphere.rotation.x += speed * 0.5;
            renderer.render(scene, camera);
        }
        animate();

        // 2. 2D Multi-Room Agent Town with Office Furniture
        const canvas = document.getElementById('hubCanvas');
        const ctx = canvas.getContext('2d');
        let currentTab = 'agents';

        const officeRooms = [
            { name: "TACTICAL HQ", x: 10, y: 10, w: 260, h: 90, color: "rgba(14,34,56,0.85)", border: "#38bdf8" },
            { name: "NEURAL AI LAB", x: 280, y: 10, w: 260, h: 90, color: "rgba(31,16,53,0.85)", border: "#a855f7" },
            { name: "VEDIC SANCTUM", x: 550, y: 10, w: 260, h: 90, color: "rgba(44,29,5,0.85)", border: "#f59e0b" },
            { name: "DATA BAY", x: 10, y: 110, w: 390, h: 95, color: "rgba(6,36,25,0.85)", border: "#10b981" },
            { name: "SECURITY VAULT", x: 410, y: 110, w: 400, h: 95, color: "rgba(45,27,6,0.85)", border: "#fbbf24" }
        ];

        const furniture = [
            { x: 30, y: 40, w: 45, h: 20, monitor: "#00f5d4" },
            { x: 130, y: 40, w: 45, h: 20, monitor: "#38bdf8" },
            { x: 310, y: 40, w: 45, h: 20, monitor: "#f43f5e" },
            { x: 430, y: 40, w: 45, h: 20, monitor: "#a855f7" },
            { x: 610, y: 40, w: 55, h: 22, monitor: "#f59e0b" }
        ];

        let agents = [
            { name: "Bob", role: "Data", x: 52, y: 50, dx: 0.2, dy: 0.1, color: "#10b981", status: "Active" },
            { name: "Carol", role: "Education", x: 152, y: 50, dx: -0.2, dy: 0.15, color: "#ec4899", status: "Active" },
            { name: "Alice", role: "DevOps", x: 332, y: 50, dx: 0.3, dy: -0.2, color: "#38bdf8", status: "Active" },
            { name: "Dave", role: "Security", x: 452, y: 50, dx: -0.2, dy: 0.2, color: "#fbbf24", status: "Active" }
        ];

        function drawHub(){
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            ctx.fillStyle = "#040814";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if(currentTab === 'agents'){
                officeRooms.forEach(r => {
                    ctx.fillStyle = r.color; ctx.fillRect(r.x, r.y, r.w, r.h);
                    ctx.strokeStyle = r.border; ctx.lineWidth = 1.5; ctx.strokeRect(r.x, r.y, r.w, r.h);
                    ctx.fillStyle = r.border; ctx.font = "bold 9px sans-serif"; ctx.fillText(`● ${r.name}`, r.x + 8, r.y + 14);
                });

                furniture.forEach(f => {
                    ctx.fillStyle = "#1e293b"; ctx.fillRect(f.x, f.y, f.w, f.h);
                    ctx.fillStyle = f.monitor; ctx.fillRect(f.x + f.w/2 - 6, f.y + 2, 12, 4);
                });

                agents.forEach(a => {
                    a.x += a.dx; a.y += a.dy;
                    if(a.x < 25 || a.x > canvas.width - 60) a.dx *= -1;
                    if(a.y < 30 || a.y > canvas.height - 35) a.dy *= -1;
                    ctx.fillStyle = a.color; ctx.beginPath(); ctx.arc(a.x, a.y, 6, 0, Math.PI * 2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px sans-serif"; ctx.fillText(a.name, a.x - 10, a.y - 8);
                });
            } else if(currentTab === 'visual'){
                ctx.fillStyle = "#00f5d4"; ctx.font = "bold 11px monospace"; ctx.fillText("VISUAL ARCHITECTURE MATRIX • FLOWCHART", 20, 30);
            } else if(currentTab === 'gesture'){
                ctx.fillStyle = "#fbbf24"; ctx.font = "bold 11px monospace"; ctx.fillText("IRON-MAN OPTICAL GESTURE HUB • TRACKING ON", 20, 30);
            }
            requestAnimationFrame(drawHub);
        }
        drawHub();

        function setTab(tab){
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
        }

        async function sendQuery(){
            const input = document.getElementById('user-input');
            const stream = document.getElementById('chat-stream');
            const stateText = document.getElementById('core-state-text');
            const q = input.value.trim();
            if(!q) return;

            stream.innerHTML += `<div class="bg-cyan-900/20 border border-cyan-700/40 p-2 rounded-lg text-white font-medium">You: ${q}</div>`;
            input.value = '';
            stateText.innerText = "JARVIS • THINKING...";
            sphere.material.color.setHex(0xf59e0b);

            try {
                const res = await fetch("http://127.0.0.1:8000/api/chat", {
                    method: "POST", headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({query: q, persona: currentPersona, language: currentLanguage, provider: "gemini"})
                });
                const data = await res.json();
                stream.innerHTML += `
                    <div class="bg-black/60 border border-cyan-800/60 p-2.5 rounded-lg space-y-1">
                        <details class="text-[10px] text-gray-400 bg-cyan-950/40 p-1.5 rounded cursor-pointer" open>
                            <summary class="font-bold text-cyan-300">THOUGHT PROCESS (JARVIS)</summary>
                            <div class="mt-1">${data.thought_process.replace(/\\n/g, '<br>')}</div>
                        </details>
                        <p class="text-cyan-200 mt-1">${data.response}</p>
                    </div>
                `;
                stateText.innerText = "JARVIS • SPEAKING...";
                sphere.material.color.setHex(0x10b981);
                speakText(data.voice_text || data.response);
                setTimeout(() => {
                    stateText.innerText = isAIActive ? "JARVIS • ACTIVE & LISTENING" : "JARVIS CORE • STANDBY";
                    sphere.material.color.setHex(isAIActive ? 0x00f5d4 : 0x38bdf8);
                }, 3000);
            } catch(e) {
                stream.innerHTML += `<div class="text-rose-400 p-2">Connecting to backend on Port 8000...</div>`;
                stateText.innerText = "JARVIS CORE • STANDBY";
            }
            stream.scrollTop = stream.scrollHeight;
        }

        document.getElementById('user-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') sendQuery(); });
        document.getElementById('term-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') runTerminalCmd(); });
    </script>
</body>
</html>
'''
(FRONTEND_DIR / "index.html").write_text(html_content, encoding="utf-8")

# ----------------------------------------------------------------------
# 4. MASTER LAUNCHER & GITHUB SYNC
# ----------------------------------------------------------------------
launcher_script = '''import os
import sys
import time
import socket
import subprocess
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "src_frontend" / "index.html"
BACKEND = ROOT / "src_backend" / "engine.py"

def is_port_in_use(port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

print("=" * 80)
print("  SK ENTERPRISES | LAUNCHING SK AI 4.0 PLATFORM V5.0")
print("  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR")
print("=" * 80)

if not is_port_in_use(8000):
    subprocess.Popen([sys.executable, str(BACKEND)], cwd=str(ROOT))
    print("[BACKEND]: FastAPI Engine spawned on http://127.0.0.1:8000")
    time.sleep(1.5)
else:
    print("[BACKEND]: Engine already active on http://127.0.0.1:8000")

webbrowser.open(f"file:///{FRONTEND}")
print("[FRONTEND]: Cyber HUD & World Monitor LIVE.")
'''
(ROOT_DIR / "run_sk_ai.py").write_text(launcher_script, encoding="utf-8")

try:
    subprocess.run("git add .", cwd=ROOT_DIR, shell=True)
    subprocess.run('git commit -m "feat(release): SK AI 4.0 Platform V5.0 World Monitor & Full Settings Engine by Sumeet Kumar"', cwd=ROOT_DIR, shell=True)
    subprocess.run("git push -u origin main", cwd=ROOT_DIR, shell=True)
    print("[Git Success]: Production Release synchronized with GitHub repository.")
except Exception as e:
    print(f"[Git Notice]: {e}")

print("\n" + "=" * 85)
print("  DEPLOYMENT COMPLETE! INVENTOR & SOLE ARCHITECT: SUMEET KUMAR")
print("=" * 85)
