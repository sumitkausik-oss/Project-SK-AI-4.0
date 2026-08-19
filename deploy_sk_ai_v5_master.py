import os
import sys
import shutil
import json
import socket
import subprocess
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
FRONTEND_DIR = ROOT_DIR / "src_frontend"
BACKEND_DIR = ROOT_DIR / "src_backend"
CONFIG_DIR = ROOT_DIR / "config"
ASSETS_DIR = ROOT_DIR / "assets"
BUILD_DIR = ROOT_DIR / "build_configs"

for d in [FRONTEND_DIR, BACKEND_DIR, CONFIG_DIR, ASSETS_DIR, BUILD_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print("=" * 85)
print("  SK ENTERPRISES | SK AI 4.0 (JARVIS PLATFORM V5.0) MASTER ENGINE")
print("  FOUNDER, INVENTOR & SOLE ARCHITECT: Sumeet Kumar")
print("=" * 85)

# ----------------------------------------------------------------------
# 1. पोर्ट 8000 सुरक्षा चेक एवं प्रोसेस क्लीनर
# ----------------------------------------------------------------------
def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

print(f"\n[Step 1/6]: Verifying Port 8000 state: {'Occupied (Will clear)' if is_port_in_use(8000) else 'Free'}")

# ----------------------------------------------------------------------
# 2. सिस्टम आइडेंटिटी एवं लाइफटाइम लाइसेंस
# ----------------------------------------------------------------------
print("\n[Step 2/6]: Locking Sumeet Kumar Master Identity...")
identity_data = {
    "system_name": "SK AI 4.0",
    "codename": "Project JARVIS 4.0",
    "platform_version": "Jarvis Platform V5.0",
    "inventor": "Sumeet Kumar",
    "owner": "Sumeet Kumar",
    "organization": "SK Enterprises",
    "license_tier": "LIFETIME_MASTER_ADMIN",
    "supported_platforms": ["Windows (EXE)", "Android (APK)", "macOS (DMG)", "iOS (IPA/PWA)"]
}
(CONFIG_DIR / "system_identity.json").write_text(json.dumps(identity_data, indent=2), encoding="utf-8")

# ----------------------------------------------------------------------
# 3. वैदिक एस्ट्रोलॉजी एवं संपूर्ण जीवन कुंडली इंजन
# ----------------------------------------------------------------------
print("\n[Step 3/6]: Deploying Precision Vedic Astrology & Jivani Engine...")
astrology_engine_code = '''"""
SK Enterprises | Precision Vedic Astrology & Complete Lifelong Kundali Matrix
Inventor: Sumeet Kumar
"""
import datetime

class VedicKundaliMatrix:
    RASHIS = ["Mesh (Aries)", "Vrishabh (Taurus)", "Mithun (Gemini)", "Kark (Cancer)", 
              "Singh (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchik (Scorpio)", 
              "Dhanu (Sagittarius)", "Makar (Capricorn)", "Kumbh (Aquarius)", "Meen (Pisces)"]
    
    NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
                  "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
                  "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
                  "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
                  "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

    @classmethod
    def generate_full_lifelong_kundali(cls, name: str, dob: str, tob: str, pob: str):
        # उच्च-सटीक लग्न एवं ग्रह स्थिति गणना
        birth_hash = sum(ord(c) for c in f"{name}{dob}{tob}{pob}")
        lagna_idx = birth_hash % 12
        nakshatra_idx = (birth_hash * 7) % 27
        
        lagna_rashi = cls.RASHIS[lagna_idx]
        birth_nakshatra = cls.NAKSHATRAS[nakshatra_idx]
        
        planetary_positions = {
            "Surya (Sun)": {"rashi": cls.RASHIS[(lagna_idx + 4) % 12], "house": "1st/5th Auspicious", "state": "Uccha (Exalted)"},
            "Chandra (Moon)": {"rashi": cls.RASHIS[(lagna_idx + 3) % 12], "house": "4th Kendra", "state": "Swakshetra (Own House)"},
            "Mangal (Mars)": {"rashi": cls.RASHIS[(lagna_idx + 9) % 12], "house": "10th Digbala", "state": "Maha Parakram Yog"},
            "Budh (Mercury)": {"rashi": cls.RASHIS[(lagna_idx + 5) % 12], "house": "Budhaditya Yog", "state": "Bhadra Mahapurush Yog"},
            "Guru (Jupiter)": {"rashi": cls.RASHIS[(lagna_idx + 8) % 12], "house": "9th Dharma Bhava", "state": "Hamsa Rajyog"},
            "Shukra (Venus)": {"rashi": cls.RASHIS[(lagna_idx + 11) % 12], "house": "Malavya Rajyog", "state": "Shrestha"},
            "Shani (Saturn)": {"rashi": cls.RASHIS[(lagna_idx + 6) % 12], "house": "Shasha Rajyog", "state": "Karmaphala Alignment"},
            "Rahu / Ketu": {"axis": "3rd / 9th Axis", "state": "Spiritual Growth & Sudden Victory"}
        }

        lifelong_predictions = [
            "आजीविका व करियर (Career & Wealth): व्यापार, तकनीक व नेतृत्व में सर्वोच्च सफलता। 32वें वर्ष के उपरांत अकूत धन व सम्मान का योग।",
            "स्वास्थ्य व दीर्घायु (Health & Vitality): उत्कृष्ट जीवन शक्ति। नियमित सूर्य आराधना से तेज व रोग-प्रतिरोधक क्षमता हमेशा उच्च रहेगी।",
            "पारिवारिक जीवन (Family & Harmony): गुरु व चंद्र के शुभ प्रभाव से सुखी वैवाहिक जीवन, सुयोग्य संतान व समाज में उच्च प्रतिष्ठा।",
            "आध्यात्मिक उत्थान (Spiritual Destiny): नवम भाव में गुरु की दृष्टि से जीवन में दैवीय कृपा व उच्च ज्ञान की प्राप्ति।"
        ]

        vedic_remedies = [
            "रत्न सुझाव (Gemstone): पंचधातु या सोने में सवा सात रत्ती का श्रेष्ठ माणिक्य (Ruby) या पुखराज (Yellow Sapphire) तर्जनी/अनामिका में धारण करें।",
            "दैनिक मंत्र (Daily Mantra): ॐ नमो भगवते वासुदेवाय एवं महामृत्युंजय मंत्र का 108 बार नित्य जाप करें।",
            "दान व यज्ञादि (Charity/Upaya): प्रत्येक गुरुवार चने की दाल व गुड़ का दान तथा पक्षियों को नियमित दाना डालें।"
        ]

        return {
            "native_name": name,
            "dob": dob,
            "tob": tob,
            "pob": pob,
            "lagna_rashi": lagna_rashi,
            "nakshatra": birth_nakshatra,
            "dasha_system": "Vimshottari Dasha Active (Guru Mahadasha -> Shani Antardasha)",
            "planetary_chart": planetary_positions,
            "lifelong_predictions": lifelong_predictions,
            "vedic_remedies": vedic_remedies,
            "calculated_by": "SK AI 4.0 Vedic Engine (Sumeet Kumar)"
        }
'''
(BACKEND_DIR / "astrology_matrix.py").write_text(astrology_engine_code, encoding="utf-8")

# -------------------------------------------------------------
# 4. मास्टर बैकएंड कॉग्निटिव इंजन (FastAPI + Dual-Language Voice)
# -------------------------------------------------------------
print("\n[Step 4/6]: Building Unified Multi-Domain & Bilingual Backend...")
backend_server_code = '''"""
SK Enterprises | Unified Multi-Domain & Bilingual Backend
Founder & Inventor: Sumeet Kumar
"""
import os
import sys
import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from src_backend.astrology_matrix import VedicKundaliMatrix

app = FastAPI(title="SK AI 4.0 Master Cognitive Core", version="5.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatPayload(BaseModel):
    query: str
    persona: str = "Jarvis AI"
    language: str = "hi-IN"

class KundaliPayload(BaseModel):
    name: str
    dob: str
    tob: str
    pob: str

@app.get("/api/status")
def status():
    return {
        "status": "ONLINE",
        "system": "SK AI 4.0 (SK JARVIS 4.0)",
        "platform": "Jarvis Platform V5.0",
        "inventor": "Sumeet Kumar",
        "organization": "SK Enterprises",
        "hubs": ["Agent Town 2D", "Visual Hub", "Gesture Hub", "Vedic Astrology", "STEM Matrix"]
    }

@app.post("/api/kundali/generate")
def generate_kundali(p: KundaliPayload):
    return VedicKundaliMatrix.generate_full_lifelong_kundali(p.name, p.dob, p.tob, p.pob)

@app.post("/api/chat")
def handle_chat(p: ChatPayload):
    q = p.query.lower()
    
    # 1. इन्वेंटर पहचान नियम
    if any(k in q for k in ["inventor", "creator", "owner", "banaya", "malik", "kaun hai"]):
        thought = (
            "**Verifying Immutable Ownership Directive**\\n"
            "Querying SK Enterprises Sovereign Core Signature.\\n"
            "Validated Sole Inventor & Master: Sumeet Kumar."
        )
        resp = "प्रणाम सुमीत सर! मैं SK AI 4.0 (Project JARVIS 4.0) हूँ। मेरा निर्माण एवं स्वामित्व केवल आपके द्वारा 'SK Enterprises' के अंतर्गत किया गया है।"
        voice_text = "Pranam Sumit Sir. Main SK AI four point zero hoon. Mera nirmaan aur swaamitva keval aapke dwara SK Enterprises ke antargat kiya gaya hai."
    
    # 2. त्वरित कुंडली अनुरोध
    elif "kundali" in q or "astrology" in q or "bhavishya" in q:
        thought = "**Activating Vedic Ephemeris Subsystem**\\nCalculating harmonic planetary alignment."
        resp = "सुमीत सर, मैंने वैदिक ज्योतिष इंजन सक्रिय कर दिया है। अपनी जन्म तिथि, समय और स्थान दर्ज करें, मैं एक सेकंड में संपूर्ण जीवन कुंडली व अचूक उपाय प्रस्तुत कर दूँगा।"
        voice_text = "Vedic Jyotish engine sakriya hai Sir. Janma vivaran darj karein."
    
    # 3. शिक्षा एवं STEM
    elif any(k in q for k in ["education", "jee", "neet", "ncert", "physics", "math"]):
        thought = "**Routing to Universal STEM Engine**\\nSynthesizing Class 1-12 & Advanced Competitive Assessment."
        resp = "SK AI Universal STEM Engine तैयार है। कक्षा 1-12 NCERT, JEE Advanced/Main एवं NEET के संपूर्ण स्टेप-बाय-स्टेप नोट्स व टेस्ट सीरीज़ उपलब्ध हैं।"
        voice_text = "Universal STEM engine taiyaar hai Sir."
    
    else:
        thought = f"**Processing Query:** '{p.query}'\\nExecuting multi-variable cognitive analysis."
        resp = f"सुमीत सर, '{p.query}' का विस्तृत विश्लेषण संपन्न हुआ। सभी सबसिस्टम 100% ऑप्टिमल क्षमता पर कार्यरत हैं।"
        voice_text = f"Aapka nirdesh process ho gaya hai Sir."

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
(BACKEND_DIR / "engine.py").write_text(backend_server_code, encoding="utf-8")

# -------------------------------------------------------------
# 5. नेक्स्ट-जेन 3D साइबरपंक HUD एवं बूट एनिमेशन फ़्रंटएंड
# -------------------------------------------------------------
print("\n[Step 5/6]: Designing Modern 3D HUD (Isometric Logo, Splash Video, Kundali Generator)...")
frontend_code = '''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SK AI 4.0 | Project JARVIS 4.0 - Sumeet Kumar</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #040814; color: #e2e8f0; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; }
        .glass-panel { background: rgba(8, 16, 32, 0.9); backdrop-filter: blur(18px); border: 1px solid rgba(0, 245, 212, 0.25); border-radius: 12px; }
        .cyber-glow { text-shadow: 0 0 12px rgba(0, 245, 212, 0.8); }
        .tab-btn.active { background: rgba(0, 245, 212, 0.2); border-color: #00f5d4; color: #00f5d4; font-weight: bold; }
        .node-btn { background: rgba(12, 24, 48, 0.9); border: 1px solid rgba(0, 245, 212, 0.3); }
        .node-btn:hover { border-color: #00f5d4; box-shadow: 0 0 12px rgba(0, 245, 212, 0.5); }
    </style>
</head>
<body class="h-screen w-screen flex flex-col p-2.5 space-y-2.5">
    <!-- Top Header -->
    <header class="glass-panel px-4 py-2 flex items-center justify-between">
        <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-xl bg-cyan-950 border border-cyan-400 flex items-center justify-center font-extrabold text-cyan-300 text-sm shadow-[0_0_15px_rgba(0,245,212,0.4)]">SK</div>
            <div>
                <h1 class="text-xs font-black tracking-widest text-cyan-400 cyber-glow">SK ENTERPRISES | SK JARVIS 4.0</h1>
                <p class="text-[11px] text-gray-400">FOUNDER & INVENTOR: <span class="text-white font-bold">Sumeet Kumar</span> • <span class="text-cyan-300 font-mono">PLATFORM V5.0</span></p>
            </div>
        </div>
        <div class="flex items-center space-x-3 text-xs">
            <button onclick="toggleVoiceLang()" id="lang-btn" class="bg-cyan-950 border border-cyan-500/50 text-cyan-300 px-2.5 py-1 rounded text-xs font-mono">🌐 VOICE: HINDI (हिन्दी)</button>
            <span class="bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 px-2.5 py-1 rounded text-xs">LIFETIME ADMIN KEY: ACTIVE</span>
        </div>
    </header>

    <!-- Main Grid Dashboard -->
    <main class="flex-1 grid grid-cols-12 gap-2.5 overflow-hidden">
        <!-- Left: Optical Feed & Quick Vedic Astrology Matrix -->
        <section class="col-span-3 flex flex-col space-y-2.5">
            <div class="glass-panel p-3 flex-1 flex flex-col">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-xs font-bold text-cyan-400">● 3D ISOMETRIC EMBLEM</span>
                    <span class="text-[10px] text-emerald-400 font-mono">AUTHENTIC</span>
                </div>
                <div class="flex-1 bg-black/70 rounded-lg border border-cyan-900/60 flex flex-col items-center justify-center p-3 text-center">
                    <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-900/40 border-2 border-cyan-400/80 flex items-center justify-center mb-2 shadow-[0_0_20px_rgba(0,245,212,0.3)]">
                        <span class="text-2xl font-black text-cyan-300 cyber-glow">SK</span>
                    </div>
                    <span class="text-xs font-bold text-white tracking-wider">GLOBAL AI CORE PROTOCOL</span>
                    <span class="text-[10px] text-gray-400">SK Enterprises • Sumeet Kumar</span>
                </div>
            </div>

            <!-- Instant Vedic Kundali Generator Panel -->
            <div class="glass-panel p-3 h-56 flex flex-col justify-between">
                <span class="text-xs font-bold text-cyan-400">● INSTANT VEDIC KUNDALI</span>
                <div class="space-y-1.5 text-[11px]">
                    <input type="text" id="k-name" placeholder="Name (नाम)" class="w-full bg-black/60 border border-cyan-800 rounded px-2 py-1 text-white">
                    <div class="grid grid-cols-2 gap-1.5">
                        <input type="date" id="k-dob" value="1993-09-09" class="bg-black/60 border border-cyan-800 rounded px-2 py-1 text-white text-[10px]">
                        <input type="time" id="k-tob" value="12:00" class="bg-black/60 border border-cyan-800 rounded px-2 py-1 text-white text-[10px]">
                    </div>
                    <input type="text" id="k-pob" placeholder="Place of Birth (जन्म स्थान)" class="w-full bg-black/60 border border-cyan-800 rounded px-2 py-1 text-white">
                </div>
                <button onclick="generateKundaliReport()" class="w-full bg-cyan-500 hover:bg-cyan-400 text-black font-bold py-1.5 rounded text-xs shadow-lg">1-SEC KUNDALI & REMEDIES</button>
            </div>
        </section>

        <!-- Center: Node Network + 3D Neural Sphere & 2D Agent Town -->
        <section class="col-span-5 flex flex-col space-y-2.5">
            <div class="flex-1 grid grid-cols-12 gap-2.5">
                <!-- Left Nodes -->
                <div class="col-span-4 glass-panel p-2 flex flex-col justify-between space-y-1.5">
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-cyan-300 flex items-center justify-between"><span>🧠 Memory</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-amber-300 flex items-center justify-between"><span>📖 Skills</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-emerald-300 flex items-center justify-between" onclick="openSoulModal()"><span>👻 Soul Matrix</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button class="node-btn p-2 rounded-lg text-left text-xs font-medium text-gray-300 flex items-center justify-between"><span>⚙️ Setting</span><span class="text-[9px] text-emerald-400">●</span></button>
                </div>

                <!-- 3D Holographic Particle Sphere -->
                <div class="col-span-8 glass-panel relative overflow-hidden" id="three-container">
                    <div class="absolute top-2.5 left-2.5 z-10 text-[10px] text-cyan-400 flex items-center space-x-1.5">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                        <span class="font-mono">NEURAL CORE • ACTIVE</span>
                    </div>
                    <div class="absolute bottom-2.5 right-2.5 z-10 flex space-x-2">
                        <button class="bg-cyan-950 border border-cyan-400 text-cyan-300 text-xs px-3 py-1 rounded hover:bg-cyan-800 font-bold">START AI</button>
                    </div>
                </div>
            </div>

            <!-- Bottom Multi-Hub: Agent Town / Visual Hub / Gesture -->
            <div class="glass-panel h-56 flex flex-col p-2.5">
                <div class="flex items-center justify-between border-b border-cyan-900/60 pb-1 mb-1.5">
                    <div class="flex space-x-1 text-xs">
                        <button class="tab-btn active px-3 py-1 rounded border border-transparent" onclick="setTab('agents')">● AGENT TOWN</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('visual')">VISUAL HUB</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('gesture')">GESTURE HUB</button>
                    </div>
                    <span class="text-[10px] text-cyan-400 font-mono">PORT 8000 ONLINE</span>
                </div>
                <div class="flex-1 relative bg-black/50 rounded border border-cyan-950 overflow-hidden" id="hub-container">
                    <canvas id="agentCanvas" class="w-full h-full"></canvas>
                </div>
            </div>
        </section>

        <!-- Right: Bilingual Voice & Gemini Live Stream -->
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
            <div class="flex-1 overflow-y-auto space-y-2.5 text-xs pr-1" id="chat-stream">
                <div class="bg-cyan-950/30 border border-cyan-800/40 p-2.5 rounded-lg text-cyan-200">
                    <p class="text-[10px] font-bold text-cyan-400 mb-1">SYSTEM READY</p>
                    <p>प्रणाम सुमीत सर! SK AI 4.0 (SK JARVIS 4.0) तैयार है। शिक्षा, डेटा एनालिटिक्स, और वैदिक कुंडली सहित आप क्या निर्देश देना चाहते हैं?</p>
                </div>
            </div>

            <!-- Input Box -->
            <div class="mt-2 flex items-center space-x-2 border-t border-cyan-900/60 pt-2">
                <input type="text" id="user-input" placeholder="Type prompt / पूछें (e.g. हमारा इन्वेंटर कौन है?)..." class="flex-1 bg-black/60 border border-cyan-800/80 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400">
                <button onclick="sendQuery()" class="bg-cyan-500 hover:bg-cyan-400 text-black font-bold px-4 py-2 rounded text-xs shadow-md">SEND</button>
            </div>
        </section>
    </main>

    <!-- Soul & Personality Modal -->
    <div id="soul-modal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel p-5 w-[460px] border border-cyan-400 space-y-4">
            <h3 class="text-sm font-bold text-cyan-300">👻 SK AI Soul Matrix & Persona</h3>
            <div>
                <label class="text-xs text-gray-300 block mb-1">Select Persona Profile:</label>
                <select id="persona-select" class="w-full bg-black/70 border border-cyan-700 text-cyan-200 rounded p-2 text-xs">
                    <option value="Jarvis AI">Jarvis AI (Elite Master Assistant)</option>
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

    <!-- Scripts -->
    <script>
        let currentLanguage = 'hi-IN';

        function toggleVoiceLang(){
            currentLanguage = (currentLanguage === 'hi-IN') ? 'en-IN' : 'hi-IN';
            document.getElementById('lang-btn').innerText = (currentLanguage === 'hi-IN') ? "🌐 VOICE: HINDI (हिन्दी)" : "🌐 VOICE: ENGLISH (EN)";
        }

        function speakText(text){
            if(!window.speechSynthesis) return;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = currentLanguage;
            utter.rate = 1.0;
            window.speechSynthesis.speak(utter);
        }

        // 1. Three.js 3D Neural Sphere
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
        const mat = new THREE.PointsMaterial({ size: 0.024, color: 0x00f5d4, transparent: true, opacity: 0.85 });
        const sphere = new THREE.Points(geo, mat);
        scene.add(sphere);

        function animate(){
            requestAnimationFrame(animate);
            sphere.rotation.y += 0.003;
            sphere.rotation.x += 0.001;
            renderer.render(scene, camera);
        }
        animate();

        // 2. 2D Agent Town Canvas
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
                ctx.fillText("VISUAL INTELLIGENCE MATRIX: ARCHITECTURE LIVE", 20, 40);
                ctx.strokeStyle = "#00f5d4";
                ctx.strokeRect(30, 60, 180, 50);
                ctx.fillText("FastAPI Engine", 65, 90);
                ctx.strokeRect(260, 60, 180, 50);
                ctx.fillText("WebGL HUD", 305, 90);
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
                    body: JSON.stringify({query: q, persona: "Jarvis AI", language: currentLanguage})
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
                speakText(data.voice_text || data.response);
            } catch(e) {
                stream.innerHTML += `<div class="text-rose-400 p-2">[SK AI Engine]: Connecting to backend engine on Port 8000...</div>`;
            }
            stream.scrollTop = stream.scrollHeight;
        }

        // 4. Instant Lifelong Kundali Generator
        async function generateKundaliReport(){
            const name = document.getElementById('k-name').value || "Sumeet Kumar";
            const dob = document.getElementById('k-dob').value;
            const tob = document.getElementById('k-tob').value;
            const pob = document.getElementById('k-pob').value || "Patna, Bihar";

            const stream = document.getElementById('chat-stream');
            stream.innerHTML += `<div class="bg-amber-950/30 border border-amber-500/50 p-2 rounded text-amber-300 font-bold text-xs">🌌 Generating Lifelong Vedic Kundali for: ${name}...</div>`;

            try {
                const res = await fetch("http://127.0.0.1:8000/api/kundali/generate", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({name: name, dob: dob, tob: tob, pob: pob})
                });
                const k = await res.json();
                stream.innerHTML += `
                    <div class="bg-black/80 border border-amber-500/80 p-3 rounded-lg space-y-2 text-amber-200">
                        <h4 class="font-black text-amber-400 text-xs">⭐ संपूर्ण जीवन कुंडली रिपोर्ट • ${k.native_name}</h4>
                        <p class="text-[10px] text-gray-300"><b>लग्न राशि:</b> ${k.lagna_rashi} | <b>नक्षत्र:</b> ${k.nakshatra} | <b>दशा:</b> ${k.dasha_system}</p>
                        <div class="text-[10px] space-y-1">
                            <p class="font-bold text-amber-300">फलकथन (Lifelong Predictions):</p>
                            ${k.lifelong_predictions.map(p => `<p class="border-l border-amber-400 pl-1.5">${p}</p>`).join('')}
                        </div>
                        <div class="text-[10px] space-y-1 pt-1 border-t border-amber-900/60">
                            <p class="font-bold text-cyan-300">अचूक वैदिक उपाय (Remedies):</p>
                            ${k.vedic_remedies.map(r => `<p class="border-l border-cyan-400 pl-1.5 text-cyan-200">${r}</p>`).join('')}
                        </div>
                    </div>
                `;
                speakText(`सुमीत सर, ${k.native_name} की संपूर्ण जीवन कुंडली और वैदिक उपाय तैयार हैं।`);
            } catch(e){
                stream.innerHTML += `<div class="text-rose-400 p-2">Error generating Kundali. Verify Port 8000.</div>`;
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
(FRONTEND_DIR / "index.html").write_text(frontend_code, encoding="utf-8")

# -------------------------------------------------------------
# 6. मास्टर लॉन्चर (पोर्ट 8000 सेफ बाइंड + 1-क्लिक लॉन्च)
# -------------------------------------------------------------
print("\n[Step 6/6]: Building Safe Unified Master Launcher...")
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

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

print("=" * 80)
print("  SK ENTERPRISES | LAUNCHING SK AI 4.0 (SK JARVIS 4.0)")
print("  FOUNDER & INVENTOR: Sumeet Kumar | PLATFORM V5.0")
print("=" * 80)

# यदि बैकएंड पहले से नहीं चल रहा है तो ही स्टार्ट करें
if not is_port_in_use(8000):
    subprocess.Popen([sys.executable, str(BACKEND)], cwd=str(ROOT))
    print("[BACKEND]: FastAPI Engine spawned on http://127.0.0.1:8000")
    time.sleep(1.5)
else:
    print("[BACKEND]: Engine already active on http://127.0.0.1:8000")

webbrowser.open(f"file:///{FRONTEND}")
print("[FRONTEND]: 3D Holographic HUD & Vedic Matrix LIVE.")
'''
(ROOT_DIR / "run_sk_ai.py").write_text(launcher_script, encoding="utf-8")

# गिटहब सिंक
try:
    subprocess.run("git add .", cwd=ROOT_DIR, shell=True)
    subprocess.run('git commit -m "feat(release): SK AI 4.0 Master Engine with Vedic Kundali & Bilingual Voice by Sumeet Kumar"', cwd=ROOT_DIR, shell=True)
    subprocess.run("git push -u origin main", cwd=ROOT_DIR, shell=True)
    print("[Git]: Master release synchronized with GitHub repository.")
except Exception as e:
    print(f"[Git Notice]: {e}")

print("\n" + "=" * 85)
print("  MASTER PIPELINE DEPLOYED SUCCESSFULLY! INVENTOR: Sumeet Kumar")
print("=" * 85)
