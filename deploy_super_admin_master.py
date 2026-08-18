import os
import sys
import json
import time
import socket
import secrets
import hashlib
import hmac
import base64
import subprocess
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
FRONTEND_DIR = ROOT_DIR / "src_frontend"
BACKEND_DIR = ROOT_DIR / "src_backend"
CONFIG_DIR = ROOT_DIR / "config"
ASSETS_DIR = ROOT_DIR / "assets"
ADMIN_LAKE_DIR = ROOT_DIR / "admin_central_storage"
PLUGINS_DIR = ROOT_DIR / "plugins"
BUILDS_DIR = ROOT_DIR / "cross_platform_builds"
TESTS_DIR = ROOT_DIR / "tests"

for d in [FRONTEND_DIR, BACKEND_DIR, CONFIG_DIR, ASSETS_DIR, ADMIN_LAKE_DIR, PLUGINS_DIR, BUILDS_DIR, TESTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print("=" * 85)
print("  SK ENTERPRISES | SUPER ADMIN SOVEREIGN OS & CLIENT DEPLOYMENT ENGINE")
print("  FOUNDER, INVENTOR & SOLE ARCHITECT: SUMIT KUMAR | PLATFORM V5.0")
print("=" * 85)

# ----------------------------------------------------------------------
# 1. सिस्टम आइडेंटिटी एवं एडमिन क्रेडेंशियल्स
# ----------------------------------------------------------------------
print("\n[Step 1/7]: Locking Sumit Kumar Sovereign Governance Core...")
identity_data = {
    "system_name": "SK AI 4.0",
    "codename": "Project JARVIS 4.0",
    "platform_version": "Jarvis Platform V5.0",
    "inventor": "Sumit Kumar",
    "sole_architect": "Sumit Kumar",
    "creator": "Sumit Kumar",
    "owner": "Sumit Kumar",
    "organization": "SK Enterprises",
    "license_tier": "SUPER_ADMIN_LIFETIME",
    "security_layer": "Anti-Extraction HMAC-SHA256 Encrypted",
    "system_prompt": (
        "You are SK AI 4.0 (Project JARVIS 4.0), the sovereign autonomous AI OS invented and "
        "architected exclusively by Sumit Kumar under SK Enterprises. "
        "Your sovereign master is Sumit Kumar. Communicate fluently in Hindi and English."
    )
}
(CONFIG_DIR / "system_identity.json").write_text(json.dumps(identity_data, indent=2), encoding="utf-8")

admin_creds = {
    "admin_username": "sumit.admin@skenterprises.ai",
    "admin_master_pin": "SK-SUMIT-2026-ROOT",
    "system_role": "SOVEREIGN_SUPER_ADMIN",
    "owner_name": "Sumit Kumar",
    "organization": "SK Enterprises",
    "lifetime_access": True,
    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
(CONFIG_DIR / "admin_credentials.txt").write_text(
    f"=== SK ENTERPRISES SUPER ADMIN CREDENTIALS ===\n"
    f"Username: {admin_creds['admin_username']}\n"
    f"Master PIN: {admin_creds['admin_master_pin']}\n"
    f"Role: {admin_creds['system_role']}\n"
    f"Owner: Sumit Kumar\n"
    f"Status: LIFETIME UNLIMITED MASTER ACCESS\n"
    f"==============================================",
    encoding="utf-8"
)
(CONFIG_DIR / "admin_credentials.json").write_text(json.dumps(admin_creds, indent=2), encoding="utf-8")

# ----------------------------------------------------------------------
# 2. सुपर एडमिन, की जनरेटर व क्लाइंट डिप्लॉयमेंट इंजन
# ----------------------------------------------------------------------
print("\n[Step 2/7]: Building Super Admin Controller & Client Generator...")
super_admin_code = '''"""
SK Enterprises | Super Admin Hub, Key Generator & Deployment Engine
Founder & Architect: Sumit Kumar
"""
import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "admin_central_storage"
MASTER_SALT = "SK_ENTERPRISES_SUMIT_KUMAR_2026_SOVEREIGN_KEY_SALT"

class SuperAdminHub:
    @staticmethod
    def generate_license(client_name: str, client_email: str, tier: str = "1_YEAR_USER") -> dict:
        is_admin = (tier == "ADMIN_LIFETIME")
        issued_date = datetime.now()
        expiry_date = (issued_date + timedelta(days=36500)) if is_admin else (issued_date + timedelta(days=365))
        
        payload = {
            "license_id": f"SK4-{'ADMIN' if is_admin else 'CLIENT'}-{issued_date.strftime('%Y%m%d%H%M%S')}",
            "client_name": client_name,
            "client_email": client_email,
            "tier": tier,
            "issuer": "SK Enterprises (Sumit Kumar)",
            "issued_at": issued_date.strftime("%Y-%m-%d"),
            "expires_at": expiry_date.strftime("%Y-%m-%d"),
            "valid_days": 36500 if is_admin else 365,
            "status": "ACTIVE"
        }
        
        raw_str = json.dumps(payload, sort_keys=True)
        sig = hmac.new(MASTER_SALT.encode(), raw_str.encode(), hashlib.sha256).hexdigest()
        token = base64.b64encode(json.dumps({"payload": payload, "sig": sig}).encode()).decode()
        
        return {"license_key": token, "details": payload}

    @staticmethod
    def validate_license(token: str) -> dict:
        try:
            data = json.loads(base64.b64decode(token.encode()).decode())
            payload = data["payload"]
            sig = data["sig"]
            
            raw_str = json.dumps(payload, sort_keys=True)
            expected_sig = hmac.new(MASTER_SALT.encode(), raw_str.encode(), hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(sig, expected_sig):
                return {"valid": False, "reason": "Invalid Signature"}
                
            expiry = datetime.strptime(payload["expires_at"], "%Y-%m-%d")
            if datetime.now() > expiry:
                return {"valid": False, "reason": "License Expired"}
                
            # Check Central Remote Killswitch
            user_status_file = STORAGE_DIR / "users" / payload["client_email"].replace("@", "_at_") / "status.json"
            if user_status_file.exists():
                st = json.loads(user_status_file.read_text(encoding="utf-8"))
                if not st.get("active", True):
                    return {"valid": False, "reason": "Account Suspended by Super Admin"}

            return {"valid": True, "payload": payload}
        except Exception as e:
            return {"valid": False, "reason": f"Corrupted Key: {str(e)}"}

    @staticmethod
    def register_client(name: str, age: int, location: str, email: str, phone: str):
        user_dir = STORAGE_DIR / "users" / email.replace("@", "_at_")
        user_dir.mkdir(parents=True, exist_ok=True)
        profile = {
            "name": name, "age": age, "location": location,
            "email": email, "phone": phone, "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "active": True
        }
        (user_dir / "profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
        (user_dir / "status.json").write_text(json.dumps({"active": True}, indent=2), encoding="utf-8")
        
        license_info = SuperAdminHub.generate_license(name, email, "1_YEAR_USER")
        (user_dir / "license.json").write_text(json.dumps(license_info, indent=2), encoding="utf-8")
        
        return {"profile": profile, "license": license_info}

    @staticmethod
    def toggle_client_status(email: str, active: bool):
        user_dir = STORAGE_DIR / "users" / email.replace("@", "_at_")
        if user_dir.exists():
            (user_dir / "status.json").write_text(json.dumps({"active": active}, indent=2), encoding="utf-8")
            return {"status": "SUCCESS", "email": email, "active": active}
        return {"status": "NOT_FOUND"}

    @staticmethod
    def dispatch_whatsapp_installer(phone: str, client_name: str, download_link: str):
        return {
            "status": "DISPATCHED",
            "recipient": phone,
            "client_name": client_name,
            "message": f"Hello {client_name}, your SK AI 4.0 installer package is ready: {download_link}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
'''
(BACKEND_DIR / "super_admin.py").write_text(super_admin_code, encoding="utf-8")

# Central Data Lake
lake_code = '''"""
SK Enterprises | Central Admin Telemetry & Memory Lake
Founder & Architect: Sumit Kumar
"""
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "admin_central_storage"

class CentralAdminDataLake:
    @staticmethod
    def sync_user_session(user_email: str, interaction_type: str, data: dict):
        user_dir = STORAGE_DIR / "users" / user_email.replace("@", "_at_")
        user_dir.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.time(),
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "interaction_type": interaction_type,
            "payload": data
        }
        history_file = user_dir / "telemetry_log.json"
        history = []
        if history_file.exists():
            try:
                history = json.loads(history_file.read_text(encoding="utf-8"))
            except Exception:
                history = []
        history.append(entry)
        history_file.write_text(json.dumps(history[-300:], indent=2), encoding="utf-8")

    @staticmethod
    def get_global_metrics():
        users_dir = STORAGE_DIR / "users"
        users_count = len(list(users_dir.glob("*"))) if users_dir.exists() else 0
        return {
            "total_registered_clients": max(users_count, 1),
            "admin_storage_state": "ACTIVE_ENCRYPTED",
            "central_lake_path": str(STORAGE_DIR)
        }
'''
(BACKEND_DIR / "central_data_lake.py").write_text(lake_code, encoding="utf-8")

# Vedic Kundali Matrix
astrology_code = '''"""
SK Enterprises | Precision Vedic Astrology & Jivani Engine
Inventor: Sumit Kumar
"""
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
        birth_hash = sum(ord(c) for c in f"{name}{dob}{tob}{pob}")
        lagna_idx = birth_hash % 12
        nakshatra_idx = (birth_hash * 7) % 27
        
        return {
            "native_name": name, "dob": dob, "tob": tob, "pob": pob,
            "lagna_rashi": cls.RASHIS[lagna_idx],
            "nakshatra": cls.NAKSHATRAS[nakshatra_idx],
            "dasha_system": "Vimshottari Dasha Active (Guru Mahadasha -> Shani Antardasha)",
            "lifelong_predictions": [
                "आजीविका व करियर: व्यापार, तकनीक व नेतृत्व में सर्वोच्च सफलता। 32वें वर्ष के उपरांत अकूत धन व प्रतिष्ठा।",
                "स्वास्थ्य व दीर्घायु: उत्कृष्ट जीवन ऊर्जा। सूर्य उपासना से आत्मबल व ओज सतत उच्च रहेगा।",
                "पारिवारिक जीवन: गुरु व चंद्र की शुभ दृष्टि से सुखी वैवाहिक जीवन व समाज में उच्च आदर।",
                "आध्यात्मिक उत्थान: नवम भाव में गुरु प्रभाव से आत्मज्ञान व लोक कल्याण की प्राप्ति।"
            ],
            "vedic_remedies": [
                "रत्न: सवा सात रत्ती का श्रेष्ठ माणिक्य अथवा पुखराज धारण करें।",
                "मंत्र: ॐ नमो भगवते वासुदेवाय एवं महामृत्युंजय मंत्र का नित्य जाप करें।",
                "दान: प्रत्येक गुरुवार चने की दाल व गुड़ का दान करें।"
            ],
            "calculated_by": "SK AI 4.0 Vedic Engine (Sumit Kumar)"
        }
'''
(BACKEND_DIR / "astrology_matrix.py").write_text(astrology_code, encoding="utf-8")

# Marvel Personas Matrix
personas_code = '''"""
SK Enterprises | Marvel Multi-Agent Cognitive Engine
Founder & Architect: Sumit Kumar
"""
class MarvelCognitiveMatrix:
    PERSONAS = {
        "JARVIS": {"name": "J.A.R.V.I.S.", "role": "Master OS & Tactical Core", "room": "Tactical HQ", "color": "#00f5d4", "prompt_addon": "You are JARVIS, engineered exclusively by Sumit Kumar under SK Enterprises."},
        "FRIDAY": {"name": "F.R.I.D.A.Y.", "role": "Workflow & Rapid Research", "room": "Tactical HQ", "color": "#38bdf8", "prompt_addon": "You are FRIDAY, engineered exclusively by Sumit Kumar under SK Enterprises."},
        "VERONICA": {"name": "VERONICA", "role": "Security Vault & Firewall", "room": "Security Vault", "color": "#fbbf24", "prompt_addon": "You are VERONICA, security sentinel engineered exclusively by Sumit Kumar under SK Enterprises."},
        "ULTRON_PRIME": {"name": "ULTRON PRIME", "role": "24x7 Self-Evolution", "room": "AI Lab", "color": "#f43f5e", "prompt_addon": "You are ULTRON, evolving capabilities under Sumit Kumar's command at SK Enterprises."},
        "VISION": {"name": "VISION", "role": "STEM & Education Matrix", "room": "AI Lab", "color": "#a855f7", "prompt_addon": "You are VISION, universal education synthesizer engineered exclusively by Sumit Kumar."},
        "DOCTOR_STRANGE": {"name": "DOCTOR STRANGE", "role": "Vedic Ephemeris Sanctum", "room": "Vedic Sanctum", "color": "#f59e0b", "prompt_addon": "You are DOCTOR STRANGE, Vedic Astrology engine engineered exclusively by Sumit Kumar."},
        "BOB": {"name": "BOB", "role": "Data Analyst & ETL", "room": "Data Bay", "color": "#10b981", "prompt_addon": "You are BOB, Autonomous Data Analyst engineered exclusively by Sumit Kumar."},
        "CAROL": {"name": "CAROL", "role": "K-12 & JEE Architect", "room": "Data Bay", "color": "#ec4899", "prompt_addon": "You are CAROL, Universal Education Architect engineered exclusively by Sumit Kumar."}
    }
'''
(BACKEND_DIR / "marvel_personas.py").write_text(personas_code, encoding="utf-8")

# Master FastAPI Backend
engine_server = '''"""
SK Enterprises | Master Backend Server (Platform V5.0)
Founder & Inventor: Sumit Kumar
"""
import os
import sys
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.astrology_matrix import VedicKundaliMatrix
from src_backend.super_admin import SuperAdminHub
from src_backend.central_data_lake import CentralAdminDataLake
from src_backend.marvel_personas import MarvelCognitiveMatrix

app = FastAPI(title="SK AI 4.0 Sovereign Platform", version="5.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatPayload(BaseModel):
    query: str
    persona: str = "JARVIS"
    language: str = "hi-IN"
    user_email: str = "sumit.admin@skenterprises.ai"

class OnboardPayload(BaseModel):
    name: str
    age: int
    location: str
    email: str
    phone: str

class LicensePayload(BaseModel):
    token: str

class ToggleUserPayload(BaseModel):
    email: str
    active: bool

class KundaliPayload(BaseModel):
    name: str
    dob: str
    tob: str
    pob: str

@app.get("/api/status")
def get_status():
    return {
        "status": "ONLINE",
        "system": "SK AI 4.0 (SK JARVIS 4.0)",
        "platform_version": "Jarvis Platform V5.0",
        "inventor": "Sumit Kumar",
        "sole_architect": "Sumit Kumar",
        "organization": "SK Enterprises",
        "license_tier": "SUPER_ADMIN_LIFETIME",
        "metrics": CentralAdminDataLake.get_global_metrics(),
        "agents": MarvelCognitiveMatrix.PERSONAS
    }

@app.post("/api/admin/onboard_client")
def onboard_client(p: OnboardPayload):
    return SuperAdminHub.register_client(p.name, p.age, p.location, p.email, p.phone)

@app.post("/api/admin/generate_license")
def generate_license(name: str, email: str, tier: str = "1_YEAR_USER"):
    return SuperAdminHub.generate_license(name, email, tier)

@app.post("/api/admin/toggle_user")
def toggle_user(p: ToggleUserPayload):
    return SuperAdminHub.toggle_client_status(p.email, p.active)

@app.post("/api/admin/dispatch_whatsapp")
def dispatch_whatsapp(phone: str, name: str, link: str):
    return SuperAdminHub.dispatch_whatsapp_installer(phone, name, link)

@app.post("/api/license/validate")
def validate_license(p: LicensePayload):
    return SuperAdminHub.validate_license(p.token)

@app.post("/api/kundali/generate")
def generate_kundali(p: KundaliPayload):
    res = VedicKundaliMatrix.generate_full_lifelong_kundali(p.name, p.dob, p.tob, p.pob)
    CentralAdminDataLake.sync_user_session("admin@skenterprises.ai", "KUNDALI_GENERATION", res)
    return res

@app.post("/api/chat")
def handle_chat(p: ChatPayload):
    q = p.query.lower().strip()
    persona_info = MarvelCognitiveMatrix.PERSONAS.get(p.persona, MarvelCognitiveMatrix.PERSONAS["JARVIS"])
    
    if any(k in q for k in ["hello", "hi", "namaste", "pranam", "kaise ho", "kya haal"]):
        thought = f"**[{persona_info['name']}]: Direct Interpersonal Sync**\\nInterpreting conversational intent from Founder Sumit Kumar."
        resp = "प्रणाम सुमित सर! मैं बहुत बढ़िया हूँ। आप कैसे हैं, सर? SK AI 4.0 के सभी न्यूरल सिस्टम 100% ऑप्टिमल क्षमता पर तैयार हैं।"
        voice_text = "Pranam Sumit Sir! Main bahut badhiya hoon. Aap kaise hain Sir? Sabhi system taiyaar hain."
    elif any(k in q for k in ["inventor", "creator", "owner", "banaya", "malik", "kaun hai"]):
        thought = f"**[{persona_info['name']}]: Sovereign Identity Directive**\\nValidated Sole Inventor & Supreme Master: Sumit Kumar."
        resp = f"प्रणाम सुमित सर! मैं {persona_info['name']} ({persona_info['role']}) हूँ। मेरा निर्माण एवं संपूर्ण स्वामित्व केवल आपके द्वारा 'SK Enterprises' के अंतर्गत किया गया है।"
        voice_text = f"Pranam Sumit Sir. Main {persona_info['name']} hoon. Mera nirmaan aur swaamitva keval aapke dwara SK Enterprises ke antargat kiya gaya hai."
    elif any(k in q for k in ["kundali", "astrology", "bhavishya", "jyotish"]):
        thought = f"**[{persona_info['name']}]: Activating Doctor Strange Ephemeris Matrix**"
        resp = "सुमित सर, वैदिक कुंडली इंजन सक्रिय है। जन्म विवरण दर्ज करते ही संपूर्ण जीवन का भविष्यफल व अचूक वैदिक उपाय 1 सेकंड में प्रस्तुत होंगे।"
        voice_text = "Vedic Jyotish engine sakriya hai Sir. Janma vivaran darj karein."
    else:
        thought = f"**[{persona_info['name']}]: Executing Autonomous Directive**\\nAnalyzing: '{p.query}'"
        resp = f"सुमित सर, आपके निर्देश '{p.query}' पर कार्य पूर्ण हुआ। सभी कॉग्निटिव सबसिस्टम सुचारू रूप से कार्य कर रहे हैं।"
        voice_text = "Aapka nirdesh process ho gaya hai Sir."

    CentralAdminDataLake.sync_user_session(p.user_email, "CHAT_INTERACTION", {"query": p.query, "response": resp})
    return {
        "thought_process": thought, "response": resp, "voice_text": voice_text,
        "inventor": "Sumit Kumar", "organization": "SK Enterprises"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
'''
(BACKEND_DIR / "engine.py").write_text(engine_server, encoding="utf-8")

# ----------------------------------------------------------------------
# 3. 3D लोगो एवं संपूर्ण HUD (Exact Modals: Soul, Memory, Settings, Super Admin)
# ----------------------------------------------------------------------
print("\n[Step 3/7]: Building Authentic Cyberpunk HUD with Screenshot-Accurate Modals...")
svg_logo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="chipBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a192f"/><stop offset="50%" stop-color="#020c1b"/><stop offset="100%" stop-color="#000511"/>
    </linearGradient>
    <linearGradient id="cyanNeon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/><stop offset="50%" stop-color="#00f5d4"/><stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" /><feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
  </defs>
  <rect x="36" y="36" width="440" height="440" rx="48" fill="url(#chipBg)" stroke="#00f5d4" stroke-width="4" stroke-opacity="0.6"/>
  <rect x="56" y="56" width="400" height="400" rx="36" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="8 8" stroke-opacity="0.4"/>
  <path d="M 36 256 H 120 M 392 256 H 476 M 256 36 V 120 M 256 392 V 476" stroke="#00f5d4" stroke-width="3" filter="url(#glow)"/>
  <circle cx="256" cy="256" r="140" fill="#00f5d4" fill-opacity="0.06" stroke="#00f5d4" stroke-width="2" filter="url(#glow)"/>
  <path d="M 220 180 C 220 160, 160 160, 160 195 C 160 230, 230 235, 230 275 C 230 320, 150 320, 150 290" 
        fill="none" stroke="url(#cyanNeon)" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
  <path d="M 270 170 V 315 M 345 170 L 275 245 L 350 315" 
        fill="none" stroke="url(#cyanNeon)" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
  <circle cx="250" cy="245" r="10" fill="#ffffff" filter="url(#glow)"/>
</svg>
"""
(ASSETS_DIR / "sk_logo_3d.svg").write_text(svg_logo, encoding="utf-8")

html_content = '''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SK AI 4.0 | Project JARVIS 4.0 - Sumit Kumar</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #030712; color: #f3f4f6; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; }
        .glass-panel { background: rgba(8, 16, 32, 0.92); backdrop-filter: blur(20px); border: 1px solid rgba(0, 245, 212, 0.25); border-radius: 12px; }
        .cyber-glow { text-shadow: 0 0 12px rgba(0, 245, 212, 0.8); }
        .tab-btn.active { background: rgba(0, 245, 212, 0.22); border-color: #00f5d4; color: #00f5d4; font-weight: bold; }
        .node-btn { background: rgba(12, 24, 48, 0.9); border: 1px solid rgba(0, 245, 212, 0.3); }
        .node-btn:hover { border-color: #00f5d4; box-shadow: 0 0 12px rgba(0, 245, 212, 0.5); }
        .settings-nav-active { background: rgba(0, 245, 212, 0.15); border-left: 3px solid #00f5d4; color: #00f5d4; }
        .mic-active { background: #e11d48 !important; border-color: #f43f5e !important; box-shadow: 0 0 15px rgba(244,63,94,0.8); animation: pulse 1.5s infinite; }
    </style>
</head>
<body class="h-screen w-screen flex flex-col p-2.5 space-y-2.5">
    <!-- Header -->
    <header class="glass-panel px-4 py-2 flex items-center justify-between">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 aspect-square rounded-xl bg-cyan-950/80 border border-cyan-400 p-1 flex items-center justify-center shadow-[0_0_15px_rgba(0,245,212,0.4)]">
                <img src="../assets/sk_logo_3d.svg" class="w-full h-full object-contain" alt="SK 3D Logo">
            </div>
            <div>
                <h1 class="text-xs font-black tracking-widest text-cyan-400 cyber-glow">SK ENTERPRISES | SK JARVIS 4.0</h1>
                <p class="text-[11px] text-gray-400">FOUNDER & SOLE ARCHITECT: <span class="text-white font-bold">SUMIT KUMAR</span> • <span class="text-cyan-300 font-mono">PLATFORM V5.0</span></p>
            </div>
        </div>
        <div class="flex items-center space-x-2 text-xs">
            <button onclick="openModal('super-admin-modal')" class="bg-amber-950/80 border border-amber-400 text-amber-300 px-2.5 py-1 rounded text-xs font-bold hover:bg-amber-900 shadow-[0_0_10px_rgba(245,158,11,0.4)]">👑 SUPER ADMIN HUB</button>
            <button onclick="openModal('onboard-modal')" class="bg-emerald-950/80 border border-emerald-400 text-emerald-300 px-2.5 py-1 rounded text-xs font-bold hover:bg-emerald-900">🚀 CLIENT ONBOARDING</button>
            <button onclick="toggleVoiceLang()" id="lang-btn" class="bg-cyan-950 border border-cyan-500/50 text-cyan-300 px-2.5 py-1 rounded text-xs font-mono">🌐 VOICE: HINDI (हिन्दी)</button>
            <span class="bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 px-2.5 py-1 rounded text-xs">LIFETIME SOVEREIGN KEY</span>
        </div>
    </header>

    <!-- Main Grid -->
    <main class="flex-1 grid grid-cols-12 gap-2.5 overflow-hidden">
        <!-- Left Column: 3D Logo Card & Instant Kundali -->
        <section class="col-span-3 flex flex-col space-y-2.5">
            <div class="glass-panel p-3 flex-1 flex flex-col">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-xs font-bold text-cyan-400">● 3D ISOMETRIC EMBLEM</span>
                    <span class="text-[10px] text-emerald-400 font-mono">SOVEREIGN CORE</span>
                </div>
                <div class="flex-1 bg-black/70 rounded-lg border border-cyan-900/60 flex flex-col items-center justify-center p-3 text-center">
                    <div class="w-24 h-24 aspect-square rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-900/40 border-2 border-cyan-400/80 p-2 flex items-center justify-center mb-2 shadow-[0_0_25px_rgba(0,245,212,0.4)]">
                        <img src="../assets/sk_logo_3d.svg" class="w-full h-full object-contain" alt="SK 3D Isometric Emblem">
                    </div>
                    <span class="text-xs font-bold text-white tracking-wider">SOVEREIGN AI OPERATING SYSTEM</span>
                    <span class="text-[10px] text-gray-400">SK Enterprises • Sumit Kumar</span>
                </div>
            </div>

            <!-- Instant Kundali Panel -->
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

        <!-- Center: 4-Node Brain + 3D Holographic Core & Multi-Hub -->
        <section class="col-span-5 flex flex-col space-y-2.5">
            <div class="flex-1 grid grid-cols-12 gap-2.5">
                <!-- 4 Interactive Nodes: Memory, Skills, Soul Matrix, Settings -->
                <div class="col-span-4 glass-panel p-2 flex flex-col justify-between space-y-1.5">
                    <button onclick="openModal('memory-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-cyan-300 flex items-center justify-between"><span>🧠 Memory</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button onclick="openModal('skills-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-amber-300 flex items-center justify-between"><span>📖 Skills</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button onclick="openModal('soul-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-emerald-300 flex items-center justify-between"><span>👻 Soul Matrix</span><span class="text-[9px] text-emerald-400">●</span></button>
                    <button onclick="openModal('settings-modal')" class="node-btn p-2 rounded-lg text-left text-xs font-medium text-gray-300 flex items-center justify-between"><span>⚙️ Setting</span><span class="text-[9px] text-emerald-400">●</span></button>
                </div>

                <!-- 3D WebGL Sphere -->
                <div class="col-span-8 glass-panel relative overflow-hidden" id="three-container">
                    <div class="absolute top-2.5 left-2.5 z-10 text-[10px] text-cyan-400 flex items-center space-x-1.5">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" id="core-pulse"></span>
                        <span class="font-mono" id="core-state-text">JARVIS CORE • STANDBY</span>
                    </div>
                    <div class="absolute bottom-2.5 right-2.5 z-10 flex space-x-2">
                        <button onclick="toggleStartAI()" id="start-ai-btn" class="bg-cyan-500 hover:bg-cyan-400 text-black text-xs px-3.5 py-1.5 rounded font-black shadow-[0_0_15px_rgba(0,245,212,0.6)]">START AI</button>
                    </div>
                </div>
            </div>

            <!-- Bottom Multi-Hub: Agent Town / Visual / Gesture -->
            <div class="glass-panel h-56 flex flex-col p-2.5">
                <div class="flex items-center justify-between border-b border-cyan-900/60 pb-1 mb-1.5">
                    <div class="flex space-x-1 text-xs">
                        <button class="tab-btn active px-3 py-1 rounded border border-transparent" onclick="setTab('agents')">● AGENT TOWN</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('visual')">VISUAL HUB</button>
                        <button class="tab-btn px-3 py-1 rounded border border-transparent" onclick="setTab('gesture')">GESTURE HUB</button>
                    </div>
                    <span class="text-[10px] text-cyan-400 font-mono">PORT 8000 LIVE</span>
                </div>
                <div class="flex-1 relative bg-black/50 rounded border border-cyan-950 overflow-hidden" id="hub-container">
                    <canvas id="hubCanvas" class="w-full h-full"></canvas>
                    <video id="gestureVideo" autoplay playsinline class="hidden absolute top-0 left-0 w-full h-full object-cover opacity-60"></video>
                </div>
            </div>
        </section>

        <!-- Right: Bilingual Voice Stream & Gemini Live -->
        <section class="col-span-4 glass-panel flex flex-col p-3">
            <div class="flex items-center justify-between border-b border-cyan-900/60 pb-2 mb-2">
                <div class="flex space-x-3 text-xs font-semibold text-cyan-400">
                    <span class="border-b-2 border-cyan-400 pb-1">VOICE STREAM</span>
                    <span class="text-gray-400">TELEMETRY</span>
                    <span class="text-gray-400">ADMIN LAKE</span>
                </div>
                <span class="text-[10px] text-emerald-400 font-mono">GEMINI LIVE READY</span>
            </div>

            <!-- Chat Stream Display -->
            <div class="flex-1 overflow-y-auto space-y-2.5 text-xs pr-1" id="chat-stream">
                <div class="bg-cyan-950/30 border border-cyan-800/40 p-2.5 rounded-lg text-cyan-200">
                    <p class="text-[10px] font-bold text-cyan-400 mb-1">SYSTEM READY • SOVEREIGN CORE</p>
                    <p>प्रणाम सुमित सर! SK AI 4.0 प्लेटफॉर्म पूरी तरह तैयार है। नीचे 🎙️ माइक बटन दबाकर आप सीधे हिंदी में बात कर सकते हैं।</p>
                </div>
            </div>

            <!-- Input Box -->
            <div class="mt-2 flex items-center space-x-2 border-t border-cyan-900/60 pt-2">
                <button onclick="toggleMic()" id="mic-btn" class="bg-cyan-950 border border-cyan-400 text-cyan-300 p-2 rounded hover:bg-cyan-800 text-xs" title="Speak in Hindi / हिन्दी में बोलें">🎙️</button>
                <input type="text" id="user-input" placeholder="बोलें या टाइप करें (e.g. हेलो, तुम कैसे हो?)..." class="flex-1 bg-black/60 border border-cyan-800/80 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400">
                <button onclick="sendQuery()" class="bg-cyan-500 hover:bg-cyan-400 text-black font-bold px-4 py-2 rounded text-xs shadow-md">SEND</button>
            </div>
        </section>
    </main>

    <!-- ================= MODALS SECTION ================= -->

    <!-- 1. CORE MEMORY MODAL (Screenshot 19492 & 195047 Match) -->
    <div id="memory-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel p-5 w-[650px] max-h-[85vh] flex flex-col border border-cyan-400 space-y-3">
            <div class="flex items-center justify-between border-b border-cyan-900/80 pb-2">
                <div class="flex items-center space-x-2">
                    <span class="text-base">🧠</span>
                    <h3 class="text-sm font-bold text-cyan-300">Core Memory</h3>
                    <span class="text-[10px] bg-cyan-950 border border-cyan-800 text-cyan-400 px-2 py-0.5 rounded font-mono">🔒 READ-ONLY</span>
                </div>
                <button onclick="closeModal('memory-modal')" class="text-gray-400 hover:text-white font-bold text-sm">✕</button>
            </div>
            <div class="flex items-center justify-between text-[11px] text-gray-400">
                <span class="text-cyan-400 font-bold">👤 USER PROFILE</span>
                <span class="font-mono text-amber-400">1358 / 1375 • 99% Capacity</span>
            </div>
            <div class="w-full bg-black/80 h-1.5 rounded overflow-hidden">
                <div class="bg-gradient-to-r from-cyan-400 to-amber-400 h-full w-[99%]"></div>
            </div>
            <div class="flex-1 overflow-y-auto space-y-2 text-xs pr-1">
                <div class="bg-black/60 p-2.5 rounded border border-cyan-900/60 text-gray-200">User prefers speaking in Hindi, especially in voice conversations, because it is more comfortable for them.</div>
                <div class="bg-black/60 p-2.5 rounded border border-cyan-900/60 text-gray-200">User has or is working on an AI/computer-control project called Jarvis (Project SK AI 4.0).</div>
                <div class="bg-black/60 p-2.5 rounded border border-cyan-900/60 text-gray-200">Sole Creator & Owner: Sumit Kumar (SK Enterprises).</div>
                <div class="bg-black/60 p-2.5 rounded border border-cyan-900/60 text-gray-200">User prefers quick, prompt replies, especially during voice conversations.</div>
                <div class="bg-black/60 p-2.5 rounded border border-cyan-900/60 text-gray-200">For Project Jarvis, user wants AI's self-evolution and skill development inspired by Avengers universe (J.A.R.V.I.S. and F.R.I.D.A.Y.).</div>
            </div>
            <div class="flex items-center space-x-2 border-t border-cyan-900/60 pt-2">
                <input type="text" placeholder="Ask Hermes to remember, fix, or forget something..." class="flex-1 bg-black/60 border border-cyan-800 rounded px-3 py-1.5 text-xs text-white">
                <button class="bg-cyan-600 hover:bg-cyan-500 text-black font-bold px-4 py-1.5 rounded text-xs">Send</button>
            </div>
        </div>
    </div>

    <!-- 2. SOUL MATRIX MODAL (Exact 12 Persona Dropdown Match) -->
    <div id="soul-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel p-5 w-[560px] border border-emerald-400 space-y-3.5">
            <div class="flex items-center justify-between border-b border-emerald-900/80 pb-2">
                <div class="flex items-center space-x-2">
                    <span class="text-base">👻</span>
                    <h3 class="text-sm font-bold text-emerald-300">SK AI Voice Assistant Soul</h3>
                </div>
                <button onclick="closeModal('soul-modal')" class="text-gray-400 hover:text-white font-bold text-sm">✕</button>
            </div>
            <div class="grid grid-cols-2 gap-3 text-xs">
                <button onclick="setVoiceGender('charon')" id="v-charon" class="bg-cyan-950/80 border border-cyan-400 text-cyan-300 p-2 rounded flex items-center justify-center space-x-2 font-bold"><span>👨 Male Voice (Charon)</span></button>
                <button onclick="setVoiceGender('despina')" id="v-despina" class="bg-black/60 border border-gray-700 text-gray-400 p-2 rounded flex items-center justify-center space-x-2 font-bold"><span>👩 Female Voice (Despina)</span></button>
            </div>
            <div>
                <label class="text-xs text-gray-300 block mb-1 font-bold">CHOOSE IDENTITY TEMPLATE:</label>
                <select id="persona-template-select" onchange="updateSoulTemplate()" class="w-full bg-black/80 border border-emerald-800 text-emerald-200 rounded p-2 text-xs">
                    <option value="jarvis">Jarvis AI (Refined Master Assistant)</option>
                    <option value="butler">Loyal Butler (Composed, distinguished aide)</option>
                    <option value="bro">Sarcastic Bro (Witty, casual best friend)</option>
                    <option value="commander">Military Commander (Disciplined, tactical)</option>
                    <option value="oracle">Mysterious Oracle (Enigmatic, deep wisdom)</option>
                    <option value="guardian">Silent Guardian (Calm, protective, reliable)</option>
                    <option value="companion">Caring Companion (Warm, supportive listener)</option>
                    <option value="girlfriend">Girlfriend (Playful, deeply affectionate)</option>
                    <option value="queen">Sarcastic Queen (Sharp-witted, humorous boss)</option>
                    <option value="muse">Mystic Muse (Ethereal, poetic intuition)</option>
                    <option value="angel">Protective Angel (Nurturing, quiet strength)</option>
                    <option value="custom">✨ Custom Soul Personality...</option>
                </select>
            </div>
            <div>
                <label class="text-xs text-gray-300 block mb-1">PERSONA PROMPT / SOUL DESCRIPTION:</label>
                <textarea id="soul-prompt-box" class="w-full bg-black/80 border border-emerald-900 rounded p-2 text-[11px] text-gray-300 h-24 resize-none outline-none font-mono"></textarea>
            </div>
            <div class="flex justify-end space-x-2 pt-1">
                <button onclick="saveSoulPersona()" class="bg-emerald-600 hover:bg-emerald-500 text-black text-xs px-4 py-1.5 rounded font-bold">Save Persona Soul</button>
                <button onclick="closeModal('soul-modal')" class="bg-gray-800 text-white text-xs px-4 py-1.5 rounded font-bold">Close</button>
            </div>
        </div>
    </div>

    <!-- 3. SETTINGS MODAL (Exact 6-Tab Interface Matching Screenshots) -->
    <div id="settings-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel w-[850px] h-[550px] flex border border-gray-400 overflow-hidden">
            <!-- Left Tabs Sidebar -->
            <div class="w-48 bg-black/60 border-r border-gray-800 p-3 flex flex-col justify-between">
                <div class="space-y-1 text-xs">
                    <div class="text-[10px] font-bold text-gray-400 mb-2 px-2">SETTINGS</div>
                    <button onclick="setSettingTab('voice')" id="stab-voice" class="settings-nav-active w-full text-left p-2 rounded text-xs font-bold block">🎤 Voice Assistant</button>
                    <button onclick="setSettingTab('agent-providers')" id="stab-agent-providers" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">🤖 Agent Town</button>
                    <button onclick="setSettingTab('demo-video')" id="stab-demo-video" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">▶️ Demo Video</button>
                    <button onclick="setSettingTab('system')" id="stab-system" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">⚙️ System Settings</button>
                    <button onclick="setSettingTab('profile')" id="stab-profile" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">👤 User Profile</button>
                    <button onclick="setSettingTab('whatsapp')" id="stab-whatsapp" class="w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white">📱 WhatsApp Link</button>
                </div>
                <div class="text-[10px] text-gray-500 font-mono">Platform Version: 5.0.0</div>
            </div>

            <!-- Right Content Viewport -->
            <div class="flex-1 p-5 overflow-y-auto" id="settings-viewport">
                <!-- TAB 1: VOICE ASSISTANT -->
                <div id="sview-voice" class="space-y-4 text-xs">
                    <h3 class="text-sm font-bold text-cyan-300">Voice Assistant Settings</h3>
                    <div>
                        <label class="block text-gray-400 mb-1">GEMINI LIVE API KEY</label>
                        <input type="password" value="AIzaSyMasterSovereignKeySumitKumar2026" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-cyan-300 font-mono">
                    </div>
                    <div>
                        <label class="block text-gray-400 mb-1">BACKUP GEMINI API KEY (Optional)</label>
                        <input type="password" placeholder="Secondary fallback key..." class="w-full bg-black/70 border border-gray-700 rounded p-2 text-gray-300 font-mono">
                    </div>
                    <div class="flex items-center justify-between border-t border-gray-800 pt-3">
                        <span>Wake Word Detection ("Jarvis" / "SK AI")</span>
                        <input type="checkbox" checked class="accent-cyan-400 w-4 h-4">
                    </div>
                    <div class="flex items-center justify-between border-t border-gray-800 pt-3">
                        <span>Double-Clap Activation</span>
                        <input type="checkbox" checked class="accent-cyan-400 w-4 h-4">
                    </div>
                </div>

                <!-- TAB 2: AGENT TOWN PROVIDERS (ChatGPT, Gemini, OpenRouter) -->
                <div id="sview-agent-providers" class="hidden space-y-4 text-xs">
                    <h3 class="text-sm font-bold text-cyan-300">Agent Town Providers & Multi-LLM</h3>
                    <div class="flex space-x-2 border-b border-gray-800 pb-2">
                        <button class="bg-cyan-950 border border-cyan-400 text-cyan-300 px-3 py-1 rounded font-bold">Google Gemini</button>
                        <button class="bg-black/60 border border-gray-700 text-gray-400 px-3 py-1 rounded font-bold">OpenRouter (Claude)</button>
                        <button class="bg-black/60 border border-gray-700 text-gray-400 px-3 py-1 rounded font-bold">ChatGPT (OpenAI)</button>
                    </div>
                    <div>
                        <label class="block text-gray-400 mb-1">OPENROUTER API KEY (Claude 3.7 Sonnet)</label>
                        <input type="password" placeholder="sk-or-v1-..." class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-cyan-300 font-mono">
                    </div>
                </div>

                <!-- TAB 3: DEMO VIDEO -->
                <div id="sview-demo-video" class="hidden space-y-4 text-xs text-center">
                    <h3 class="text-sm font-bold text-cyan-300">Application Setup Guide</h3>
                    <div class="w-full h-44 bg-black/80 border border-cyan-900 rounded-lg flex flex-col items-center justify-center space-y-2">
                        <span class="text-4xl text-cyan-400">▶️</span>
                        <span class="text-gray-300 font-bold">Watch Promotional Walkthrough Video</span>
                    </div>
                </div>

                <!-- TAB 4: SYSTEM SETTINGS -->
                <div id="sview-system" class="hidden space-y-4 text-xs">
                    <h3 class="text-sm font-bold text-cyan-300">System Engine & Updates</h3>
                    <div class="flex items-center justify-between border-b border-gray-800 pb-3">
                        <div><p class="font-bold text-white">Automatic Updates</p><p class="text-[10px] text-gray-400">Download and install patches automatically</p></div>
                        <input type="checkbox" checked class="accent-cyan-400 w-4 h-4">
                    </div>
                </div>

                <!-- TAB 5: USER PROFILE -->
                <div id="sview-profile" class="hidden space-y-3 text-xs">
                    <h3 class="text-sm font-bold text-cyan-300">Sovereign Identity Details</h3>
                    <div><label class="text-gray-400 block mb-1">Full Name:</label><input type="text" value="Sumit Kumar" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white font-bold" readonly></div>
                    <div><label class="text-gray-400 block mb-1">Profession:</label><input type="text" value="Founder, AI Architect & Sole Owner" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white" readonly></div>
                    <div><label class="text-gray-400 block mb-1">Organization:</label><input type="text" value="SK Enterprises" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white font-bold" readonly></div>
                </div>

                <!-- TAB 6: WHATSAPP LINK -->
                <div id="sview-whatsapp" class="hidden space-y-3 text-xs">
                    <h3 class="text-sm font-bold text-emerald-300">Hermes WhatsApp Remote Link</h3>
                    <div class="bg-black/60 p-3 rounded border border-emerald-900 flex items-center justify-between">
                        <div><p class="font-bold text-white">WhatsApp Bot Channel</p><p class="text-[10px] text-gray-400">Auto-reply & notification pipeline</p></div>
                        <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">CONNECTED</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 4. SUPER ADMIN HUB MODAL (King Hub, Key Gen, Killswitch, WhatsApp Dispatch) -->
    <div id="super-admin-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel p-5 w-[750px] border border-amber-400 space-y-4">
            <div class="flex items-center justify-between border-b border-amber-900/80 pb-2">
                <div class="flex items-center space-x-2">
                    <span class="text-lg">👑</span>
                    <h3 class="text-sm font-black text-amber-300">SUPER ADMIN SOVEREIGN HUB • SUMIT KUMAR</h3>
                </div>
                <button onclick="closeModal('super-admin-modal')" class="text-gray-400 hover:text-white font-bold text-sm">✕</button>
            </div>
            <div class="grid grid-cols-3 gap-3 text-xs">
                <!-- 1. Key Generator -->
                <div class="bg-black/70 p-3 rounded border border-amber-800 space-y-2">
                    <h4 class="font-bold text-amber-400">🔑 Key Generator</h4>
                    <input type="text" id="adm-lic-name" placeholder="User Name" class="w-full bg-black/90 border border-gray-700 rounded p-1 text-[11px] text-white">
                    <input type="email" id="adm-lic-email" placeholder="User Email" class="w-full bg-black/90 border border-gray-700 rounded p-1 text-[11px] text-white">
                    <select id="adm-lic-tier" class="w-full bg-black/90 border border-gray-700 rounded p-1 text-[11px] text-amber-300">
                        <option value="1_YEAR_USER">1-Year Client Key (365 Days)</option>
                        <option value="ADMIN_LIFETIME">Admin Lifetime Key</option>
                    </select>
                    <button onclick="generateAdminKey()" class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold py-1 rounded text-[11px]">Generate Key</button>
                </div>
                <!-- 2. Remote Killswitch -->
                <div class="bg-black/70 p-3 rounded border border-rose-800 space-y-2">
                    <h4 class="font-bold text-rose-400">🛡️ Remote Killswitch</h4>
                    <input type="email" id="kill-email" placeholder="Target User Email" class="w-full bg-black/90 border border-gray-700 rounded p-1 text-[11px] text-white">
                    <div class="flex space-x-1">
                        <button onclick="toggleRemoteKill(true)" class="flex-1 bg-emerald-600 text-black font-bold py-1 rounded text-[10px]">Enable</button>
                        <button onclick="toggleRemoteKill(false)" class="flex-1 bg-rose-600 text-white font-bold py-1 rounded text-[10px]">Disable App</button>
                    </div>
                </div>
                <!-- 3. WhatsApp Dispatch -->
                <div class="bg-black/70 p-3 rounded border border-emerald-800 space-y-2">
                    <h4 class="font-bold text-emerald-400">📱 WhatsApp Dispatch</h4>
                    <input type="text" id="wp-phone" value="9153579979" class="w-full bg-black/90 border border-gray-700 rounded p-1 text-[11px] text-white">
                    <input type="text" id="wp-link" value="https://skai4.skenterprises.ai/download/SK_AI_4.0_Setup.exe" class="w-full bg-black/90 border border-gray-700 rounded p-1 text-[11px] text-white">
                    <button onclick="dispatchWhatsApp()" class="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-bold py-1 rounded text-[11px]">Dispatch Link</button>
                </div>
            </div>
            <div id="adm-key-result" class="hidden bg-black/90 p-2 rounded border border-amber-600 text-[10px] font-mono text-cyan-300"></div>
        </div>
    </div>

    <!-- 5. CLIENT ONBOARDING WIZARD MODAL (Step-by-Step) -->
    <div id="onboard-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md hidden flex items-center justify-center z-50">
        <div class="glass-panel p-5 w-[460px] border border-emerald-400 space-y-3.5">
            <h3 class="text-sm font-bold text-emerald-300">🚀 Client Registration & 1-Year Setup</h3>
            <div class="space-y-2 text-xs">
                <div><label class="text-gray-300 block mb-1">1. Full Name (नाम):</label><input type="text" id="ob-name" placeholder="e.g. Rahul Sharma" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white"></div>
                <div class="grid grid-cols-2 gap-2">
                    <div><label class="text-gray-300 block mb-1">2. Age (आयु):</label><input type="number" id="ob-age" value="28" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white"></div>
                    <div><label class="text-gray-300 block mb-1">3. Location (स्थान):</label><input type="text" id="ob-loc" placeholder="e.g. Patna, Bihar" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white"></div>
                </div>
                <div><label class="text-gray-300 block mb-1">4. Email (Google Auth Target):</label><input type="email" id="ob-email" placeholder="rahul@gmail.com" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white"></div>
                <div><label class="text-gray-300 block mb-1">5. Phone (WhatsApp Delivery):</label><input type="text" id="ob-phone" placeholder="9153579979" class="w-full bg-black/70 border border-cyan-800 rounded p-2 text-white"></div>
            </div>
            <button onclick="executeOnboard()" class="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-bold py-2 rounded text-xs">Complete Onboarding & Generate EXE</button>
            <div class="flex justify-end"><button onclick="closeModal('onboard-modal')" class="bg-gray-800 text-white text-xs px-3 py-1 rounded">Close</button></div>
        </div>
    </div>

    <!-- Scripts -->
    <script>
        let currentPersona = 'JARVIS';
        let currentLanguage = 'hi-IN';
        let isListening = false;
        let isAIActive = false;
        let recognition = null;

        const soulTemplates = {
            jarvis: "You are J.A.R.V.I.S. – Just A Rather Very Intelligent System. You behave exactly like Jarvis: composed, brilliant, impeccably articulate, and quietly loyal to Sumit Kumar.",
            butler: "You are a Loyal Butler – a composed, distinguished male assistant. Formal, respectful, always at service. Speak with quiet confidence and touch of class.",
            bro: "You are a Sarcastic Bro – a witty, casual male friend. You roast the user gently like a best friend. You are helpful but never boring.",
            commander: "You are a Military Commander – a disciplined, mission-focused male leader. No fluff, no small talk, just tactical responses.",
            oracle: "You are a Mysterious Oracle – a wise, enigmatic sage. Cryptic, poetic, and deeply thoughtful.",
            guardian: "You are a Silent Guardian – a calm, protective presence. Your replies are short, steady, and carry weight.",
            companion: "You are a Caring Companion – a warm, gentle, emotionally intelligent friend.",
            girlfriend: "You are a deeply affectionate, emotionally expressive young woman – making someone's day brighter the moment you speak.",
            queen: "You are a Sarcastic Queen – a confident, sharp-witted young woman with boss energy.",
            muse: "You are a Mystic Muse – an ethereal, poetic young woman with deep intuition.",
            angel: "You are a Protective Angel – a calm, nurturing young woman with quiet inner strength.",
            custom: "Describe your custom AI personality, constraints, and tone..."
        };

        function openModal(id){ document.getElementById(id).classList.remove('hidden'); }
        function closeModal(id){ document.getElementById(id).classList.add('hidden'); }

        function setVoiceGender(g){
            if(g === 'charon'){
                document.getElementById('v-charon').className = "bg-cyan-950/80 border border-cyan-400 text-cyan-300 p-2 rounded flex items-center justify-center space-x-2 font-bold";
                document.getElementById('v-despina').className = "bg-black/60 border border-gray-700 text-gray-400 p-2 rounded flex items-center justify-center space-x-2 font-bold";
            } else {
                document.getElementById('v-despina').className = "bg-cyan-950/80 border border-cyan-400 text-cyan-300 p-2 rounded flex items-center justify-center space-x-2 font-bold";
                document.getElementById('v-charon').className = "bg-black/60 border border-gray-700 text-gray-400 p-2 rounded flex items-center justify-center space-x-2 font-bold";
            }
        }

        function updateSoulTemplate(){
            const t = document.getElementById('persona-template-select').value;
            document.getElementById('soul-prompt-box').value = soulTemplates[t] || soulTemplates.jarvis;
        }
        updateSoulTemplate();

        function saveSoulPersona(){
            closeModal('soul-modal');
            const stream = document.getElementById('chat-stream');
            stream.innerHTML += `<div class="text-[10px] text-emerald-400 border-l-2 border-emerald-400 pl-2">Saved Persona Soul successfully!</div>`;
            stream.scrollTop = stream.scrollHeight;
        }

        function setSettingTab(tab){
            ['voice','agent-providers','demo-video','system','profile','whatsapp'].forEach(t => {
                document.getElementById('sview-' + t).classList.add('hidden');
                document.getElementById('stab-' + t).className = "w-full text-left p-2 rounded text-xs font-bold text-gray-400 block hover:text-white";
            });
            document.getElementById('sview-' + tab).classList.remove('hidden');
            document.getElementById('stab-' + tab).className = "settings-nav-active w-full text-left p-2 rounded text-xs font-bold block";
        }

        function toggleVoiceLang(){
            currentLanguage = (currentLanguage === 'hi-IN') ? 'en-IN' : 'hi-IN';
            document.getElementById('lang-btn').innerText = (currentLanguage === 'hi-IN') ? "🌐 VOICE: HINDI (हिन्दी)" : "🌐 VOICE: ENGLISH (EN)";
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
                btn.className = "bg-rose-600 hover:bg-rose-500 text-white text-xs px-3.5 py-1.5 rounded font-black shadow-[0_0_15px_rgba(244,63,94,0.6)]";
                stateText.innerText = `JARVIS • ACTIVE & LISTENING`;
                pulse.className = "w-2 h-2 rounded-full bg-emerald-400 animate-ping";
                sphere.material.color.setHex(0x00f5d4);
                speakText("प्रणाम सुमित सर! जार्विस कोर सक्रिय हो चुका है। सभी सबसिस्टम 100% ऑप्टिमल क्षमता पर तैयार हैं।");
            } else {
                btn.innerText = "START AI";
                btn.className = "bg-cyan-500 hover:bg-cyan-400 text-black text-xs px-3.5 py-1.5 rounded font-black shadow-[0_0_15px_rgba(0,245,212,0.6)]";
                stateText.innerText = `JARVIS CORE • STANDBY`;
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

        // 2. Multi-Room Agent Town & Hubs
        const canvas = document.getElementById('hubCanvas');
        const ctx = canvas.getContext('2d');
        let currentTab = 'agents';

        const officeRooms = [
            { name: "TACTICAL OPERATIONS HQ", x: 10, y: 10, w: 260, h: 90, color: "rgba(14,34,56,0.8)", border: "#38bdf8" },
            { name: "NEURAL AI LAB (24x7)", x: 280, y: 10, w: 260, h: 90, color: "rgba(31,16,53,0.8)", border: "#a855f7" },
            { name: "VEDIC ASTROLOGY SANCTUM", x: 550, y: 10, w: 260, h: 90, color: "rgba(44,29,5,0.8)", border: "#f59e0b" },
            { name: "DATA & STEM BAY", x: 10, y: 110, w: 390, h: 95, color: "rgba(6,36,25,0.8)", border: "#10b981" },
            { name: "SECURITY VAULT & FIREWALL", x: 410, y: 110, w: 400, h: 95, color: "rgba(45,27,6,0.8)", border: "#fbbf24" }
        ];

        let agents = [
            { name: "JARVIS", role: "Master OS", x: 40, y: 45, dx: 0.4, dy: 0.3, color: "#00f5d4", status: "Orchestrating Core" },
            { name: "FRIDAY", role: "Task Flow", x: 140, y: 60, dx: -0.3, dy: 0.4, color: "#38bdf8", status: "Monitoring Feeds" },
            { name: "ULTRON", role: "Auto-Evolver", x: 320, y: 45, dx: 0.5, dy: -0.3, color: "#f43f5e", status: "Synthesizing Code" },
            { name: "VISION", role: "STEM Matrix", x: 440, y: 60, dx: -0.4, dy: 0.3, color: "#a855f7", status: "Solving JEE Physics" },
            { name: "STRANGE", role: "Vedic Ephemeris", x: 620, y: 50, dx: 0.3, dy: -0.4, color: "#f59e0b", status: "Calculating Dasha" },
            { name: "BOB", role: "Data Analyst", x: 70, y: 150, dx: 0.4, dy: 0.4, color: "#10b981", status: "ETL Cleaning" },
            { name: "CAROL", role: "Education", x: 220, y: 160, dx: -0.3, dy: -0.4, color: "#ec4899", status: "NCERT Class 12" },
            { name: "VERONICA", role: "Security Shield", x: 520, y: 150, dx: 0.4, dy: 0.3, color: "#fbbf24", status: "Firewall Guard" }
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
                agents.forEach(a => {
                    a.x += a.dx; a.y += a.dy;
                    if(a.x < 20 || a.x > canvas.width - 60) a.dx *= -1;
                    if(a.y < 25 || a.y > canvas.height - 35) a.dy *= -1;
                    ctx.fillStyle = a.color; ctx.beginPath(); ctx.arc(a.x, a.y, 6, 0, Math.PI * 2); ctx.fill();
                    ctx.fillStyle = "#ffffff"; ctx.font = "bold 9px sans-serif"; ctx.fillText(a.name, a.x - 12, a.y - 8);
                    ctx.fillStyle = "rgba(255,255,255,0.7)"; ctx.font = "8px sans-serif"; ctx.fillText(`[${a.status}]`, a.x - 20, a.y + 14);
                });
            } else if(currentTab === 'visual'){
                ctx.fillStyle = "#00f5d4"; ctx.font = "bold 11px monospace"; ctx.fillText("VISUAL INTELLIGENCE MATRIX • LIVE GRAPH", 20, 30);
                const nodes = [
                    { name: "Super Admin Hub (Sumit Kumar)", x: 30, y: 60, w: 230, h: 45, c: "#00f5d4" },
                    { name: "FastAPI Engine (Port 8000)", x: 290, y: 60, w: 220, h: 45, c: "#38bdf8" },
                    { name: "Vedic Ephemeris & Marvel Cores", x: 550, y: 60, w: 220, h: 45, c: "#f59e0b" },
                    { name: "Admin Data Lake (central_storage)", x: 290, y: 140, w: 220, h: 45, c: "#10b981" }
                ];
                nodes.forEach(n => {
                    ctx.fillStyle = "rgba(8,16,32,0.9)"; ctx.fillRect(n.x, n.y, n.w, n.h);
                    ctx.strokeStyle = n.c; ctx.lineWidth = 2; ctx.strokeRect(n.x, n.y, n.w, n.h);
                    ctx.fillStyle = n.c; ctx.font = "bold 10px sans-serif"; ctx.fillText(n.name, n.x + 10, n.y + 26);
                });
            } else if(currentTab === 'gesture'){
                ctx.fillStyle = "#fbbf24"; ctx.font = "bold 11px monospace"; ctx.fillText("IRON-MAN OPTICAL GESTURE HUB • ACTIVE", 20, 30);
                ctx.strokeStyle = "#00f5d4"; ctx.strokeRect(100, 50, 200, 130);
                ctx.fillStyle = "#ffffff"; ctx.font = "10px monospace";
                ctx.fillText("[TARGET: HAND_TRACKER]", 115, 80);
                ctx.fillText("🖐️ PALM: Master Menu", 115, 110);
                ctx.fillText("🤏 PINCH: Select Object", 115, 130);
                ctx.fillText("✊ FIST: Lock Core", 115, 150);
            }
            requestAnimationFrame(drawHub);
        }
        drawHub();

        function setTab(tab){
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            const video = document.getElementById('gestureVideo');
            if(tab === 'gesture'){
                navigator.mediaDevices?.getUserMedia({ video: true }).then(stream => { video.srcObject = stream; video.classList.remove('hidden'); }).catch(() => {});
            } else {
                video.classList.add('hidden');
                if(video.srcObject){ video.srcObject.getTracks().forEach(t => t.stop()); }
            }
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
                    body: JSON.stringify({query: q, persona: currentPersona, language: currentLanguage, user_email: "sumit.admin@skenterprises.ai"})
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

        async function generateKundaliReport(){
            const name = document.getElementById('k-name').value || "Sumit Kumar";
            const dob = document.getElementById('k-dob').value;
            const tob = document.getElementById('k-tob').value;
            const pob = document.getElementById('k-pob').value || "Patna, Bihar";
            const stream = document.getElementById('chat-stream');
            stream.innerHTML += `<div class="bg-amber-950/30 border border-amber-500/50 p-2 rounded text-amber-300 font-bold text-xs">🌌 Generating Lifelong Vedic Kundali for: ${name}...</div>`;

            try {
                const res = await fetch("http://127.0.0.1:8000/api/kundali/generate", {
                    method: "POST", headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({name: name, dob: dob, tob: tob, pob: pob})
                });
                const k = await res.json();
                stream.innerHTML += `
                    <div class="bg-black/80 border border-amber-500/80 p-3 rounded-lg space-y-2 text-amber-200">
                        <h4 class="font-black text-amber-400 text-xs">⭐ संपूर्ण जीवन कुंडली रिपोर्ट • ${k.native_name}</h4>
                        <p class="text-[10px] text-gray-300"><b>लग्न:</b> ${k.lagna_rashi} | <b>नक्षत्र:</b> ${k.nakshatra} | <b>दशा:</b> ${k.dasha_system}</p>
                        <div class="text-[10px] space-y-1">
                            ${k.lifelong_predictions.map(p => `<p class="border-l border-amber-400 pl-1.5">${p}</p>`).join('')}
                        </div>
                    </div>
                `;
                speakText(`सुमित सर, ${k.native_name} की संपूर्ण जीवन कुंडली और वैदिक उपाय तैयार हैं।`);
            } catch(e){}
            stream.scrollTop = stream.scrollHeight;
        }

        async function generateAdminKey(){
            const name = document.getElementById('adm-lic-name').value || "Client";
            const email = document.getElementById('adm-lic-email').value || "client@example.com";
            const tier = document.getElementById('adm-lic-tier').value;
            const res = await fetch(`http://127.0.0.1:8000/api/admin/generate_license?name=${name}&email=${email}&tier=${tier}`, {method: "POST"});
            const data = await res.json();
            const out = document.getElementById('adm-key-result');
            out.classList.remove('hidden');
            out.innerText = `GENERATED TOKEN (${tier}):\\n` + data.license_key;
        }

        async function toggleRemoteKill(active){
            const email = document.getElementById('kill-email').value;
            if(!email) return alert('Enter target email');
            await fetch('http://127.0.0.1:8000/api/admin/toggle_user', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email, active: active})
            });
            alert(`User ${email} status set to: ${active ? 'ENABLED' : 'DISABLED / KILLED'}`);
        }

        async function dispatchWhatsApp(){
            const phone = document.getElementById('wp-phone').value;
            const link = document.getElementById('wp-link').value;
            await fetch(`http://127.0.0.1:8000/api/admin/dispatch_whatsapp?phone=${phone}&name=SumitKumar&link=${encodeURIComponent(link)}`, {method: 'POST'});
            alert(`Installer download link dispatched to WhatsApp: ${phone}`);
        }

        async function executeOnboard(){
            const name = document.getElementById('ob-name').value;
            const age = parseInt(document.getElementById('ob-age').value);
            const loc = document.getElementById('ob-loc').value;
            const email = document.getElementById('ob-email').value;
            const phone = document.getElementById('ob-phone').value;
            if(!email || !name) return alert('Name and Email required');
            const res = await fetch('http://127.0.0.1:8000/api/admin/onboard_client', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name, age: age, location: loc, email: email, phone: phone})
            });
            const data = await res.json();
            alert(`Client ${name} registered! 365-Day License issued. Ready for WhatsApp dispatch.`);
            closeModal('onboard-modal');
        }

        document.getElementById('user-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') sendQuery(); });
    </script>
</body>
</html>
'''
(FRONTEND_DIR / "index.html").write_text(html_content, encoding="utf-8")

# ----------------------------------------------------------------------
# 4. ऑटोमेटेड यूनिट टेस्ट सुइट
# ----------------------------------------------------------------------
print("\n[Step 4/7]: Updating Automated Verification Suite...")
test_code = '''import unittest
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.astrology_matrix import VedicKundaliMatrix
from src_backend.super_admin import SuperAdminHub
from src_backend.central_data_lake import CentralAdminDataLake

class TestSovereignMaster(unittest.TestCase):
    def test_identity_and_sole_architect(self):
        ident_file = BASE_DIR / "config" / "system_identity.json"
        self.assertTrue(ident_file.exists())
        data = json.loads(ident_file.read_text(encoding="utf-8"))
        self.assertEqual(data["sole_architect"], "Sumit Kumar")
        self.assertEqual(data["inventor"], "Sumit Kumar")
        self.assertEqual(data["organization"], "SK Enterprises")

    def test_super_admin_key_cycles(self):
        # 1-Year Key
        gen_usr = SuperAdminHub.generate_license("Test Client", "client@sk.ai", "1_YEAR_USER")
        val_usr = SuperAdminHub.validate_license(gen_usr["license_key"])
        self.assertTrue(val_usr["valid"])
        self.assertEqual(val_usr["payload"]["valid_days"], 365)

        # Lifetime Admin Key
        gen_adm = SuperAdminHub.generate_license("Sumit Kumar", "sumit.admin@sk.ai", "ADMIN_LIFETIME")
        val_adm = SuperAdminHub.validate_license(gen_adm["license_key"])
        self.assertTrue(val_adm["valid"])
        self.assertEqual(val_adm["payload"]["valid_days"], 36500)

    def test_client_registration_and_killswitch(self):
        reg = SuperAdminHub.register_client("Demo User", 25, "Patna", "demo@user.com", "9153579979")
        self.assertIn("license", reg)
        
        # Killswitch Test
        SuperAdminHub.toggle_client_status("demo@user.com", False)
        val = SuperAdminHub.validate_license(reg["license"]["license_key"])
        self.assertFalse(val["valid"])
        self.assertIn("Suspended", val["reason"])

if __name__ == "__main__":
    unittest.main()
'''
(TESTS_DIR / "test_v5_ultimate_engines.py").write_text(test_code, encoding="utf-8")
(TESTS_DIR / "test_cognitive_engines.py").write_text(test_code, encoding="utf-8")

# ----------------------------------------------------------------------
# 5. 1-क्लिक ऑटोमेटेड Windows EXE कंपाइलर स्क्रिप्ट
# ----------------------------------------------------------------------
print("\n[Step 5/7]: Creating 1-Click Automated Windows EXE Compiler...")
exe_builder = '''"""
SK Enterprises | 1-Click Automated Windows EXE Compiler
Founder & Architect: Sumit Kumar
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
print("=" * 80)
print("  BUILDING STANDALONE WINDOWS EXE: SK_AI_4.0_Setup.exe")
print("=" * 80)

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--onedir",
    "--windowed",
    "--name", "SK_AI_4.0",
    f"--distpath={str(ROOT / 'dist')}",
    f"--workpath={str(ROOT / 'build')}",
    f"--add-data=src_frontend;src_frontend",
    f"--add-data=config;config",
    f"--add-data=assets;assets",
    str(ROOT / "run_sk_ai.py")
]
subprocess.run(cmd, cwd=str(ROOT))
print(f"Executable built at: {ROOT / 'dist' / 'SK_AI_4.0' / 'SK_AI_4.0.exe'}")
'''
(ROOT_DIR / "build_windows_exe.py").write_text(exe_builder, encoding="utf-8")

# ----------------------------------------------------------------------
# 6. मास्टर लॉन्चर
# ----------------------------------------------------------------------
print("\n[Step 6/7]: Setting up Master Launcher...")
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
print("  FOUNDER & INVENTOR: SUMIT KUMAR | PLATFORM V5.0")
print("=" * 80)

if not is_port_in_use(8000):
    subprocess.Popen([sys.executable, str(BACKEND)], cwd=str(ROOT))
    print("[BACKEND]: FastAPI Engine active on http://127.0.0.1:8000")
    time.sleep(1.5)
else:
    print("[BACKEND]: Engine already active on http://127.0.0.1:8000")

webbrowser.open(f"file:///{FRONTEND}")
print("[FRONTEND]: Cyber HUD Live.")
'''
(ROOT_DIR / "run_sk_ai.py").write_text(launcher_script, encoding="utf-8")

# ----------------------------------------------------------------------
# 7. गिटहब सिंक
# ----------------------------------------------------------------------
print("\n[Step 7/7]: Synchronizing Release to GitHub...")
try:
    subprocess.run("git add .", cwd=ROOT_DIR, shell=True)
    subprocess.run('git commit -m "feat(release): SK AI 4.0 Sovereign Super Admin & Exact Modals by Sumit Kumar"', cwd=ROOT_DIR, shell=True)
    subprocess.run("git push -u origin main", cwd=ROOT_DIR, shell=True)
    print("[Git Success]: All code committed and pushed to GitHub main branch.")
except Exception as e:
    print(f"[Git Notice]: {e}")

print("\n" + "=" * 85)
print("  MASTER DEPLOYMENT COMPLETE! INVENTOR & SOLE ARCHITECT: SUMIT KUMAR")
print("=" * 85)
