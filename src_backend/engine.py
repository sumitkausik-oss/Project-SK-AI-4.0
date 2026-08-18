"""
SK Enterprises | Master Backend Server (Platform V5.0)
Founder & Inventor: Sumeet Kumar
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
from src_backend.license_generator import SKLicenseKeyEngine
from src_backend.central_data_lake import CentralAdminDataLake
from src_backend.marvel_personas import MarvelCognitiveMatrix

app = FastAPI(title="SK AI 4.0 Sovereign Platform", version="5.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatPayload(BaseModel):
    query: str
    persona: str = "JARVIS"
    language: str = "hi-IN"
    user_email: str = "sumeet.admin@skenterprises.ai"

class LicenseGenPayload(BaseModel):
    client_name: str
    client_email: str
    tier: str = "PRO_COMMERCIAL"

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
        "inventor": "Sumeet Kumar",
        "sole_architect": "Sumeet Kumar",
        "organization": "SK Enterprises",
        "license_tier": "LIFETIME_MASTER_ADMIN",
        "evolution_daemon": "24x7 ACTIVE",
        "agents": MarvelCognitiveMatrix.PERSONAS
    }

@app.get("/api/agent_town/workspaces")
def get_workspaces():
    return {
        "rooms": [
            {"id": "tactical_hq", "name": "Tactical Operations HQ", "x": 10, "y": 10, "w": 280, "h": 160, "color": "#0e2238", "agents": ["JARVIS", "FRIDAY"]},
            {"id": "ai_lab", "name": "Neural AI Lab (24x7)", "x": 300, "y": 10, "w": 280, "h": 160, "color": "#1f1035", "agents": ["ULTRON_PRIME", "VISION"]},
            {"id": "vedic_sanctum", "name": "Vedic Astrology Sanctum", "x": 590, "y": 10, "w": 280, "h": 160, "color": "#2c1d05", "agents": ["DOCTOR_STRANGE"]},
            {"id": "analytics_bay", "name": "Data Analytics & STEM Bay", "x": 10, "y": 180, "w": 420, "h": 150, "color": "#062419", "agents": ["BOB", "CAROL"]},
            {"id": "security_vault", "name": "Security Vault & Firewall", "x": 440, "y": 180, "w": 430, "h": 150, "color": "#2d1b06", "agents": ["VERONICA"]}
        ]
    }

@app.post("/api/admin/generate_license")
def generate_client_license(p: LicenseGenPayload):
    return SKLicenseKeyEngine.generate_client_key(p.client_name, p.client_email, p.tier)

@app.post("/api/kundali/generate")
def generate_kundali(p: KundaliPayload):
    res = VedicKundaliMatrix.generate_full_lifelong_kundali(p.name, p.dob, p.tob, p.pob)
    CentralAdminDataLake.sync_user_session("admin@skenterprises.ai", "KUNDALI_GENERATION", res)
    return res

@app.post("/api/chat")
def handle_chat(p: ChatPayload):
    q = p.query.lower().strip()
    persona_info = MarvelCognitiveMatrix.PERSONAS.get(p.persona, MarvelCognitiveMatrix.PERSONAS["JARVIS"])
    
    # 1. Greetings
    if any(k in q for k in ["hello", "hi", "namaste", "pranam", "kaise ho", "kya haal"]):
        thought = (
            f"**[{persona_info['name']}]: Direct Interpersonal Sync**\n"
            "Interpreting respectful conversational intent from Founder Sumeet Kumar.\n"
            "Generating personalized bilingual greeting response."
        )
        resp = "प्रणाम सुमीत सर! मैं बहुत बढ़िया हूँ। आप कैसे हैं, सर? SK AI 4.0 (SK JARVIS) के सभी न्यूरल सिस्टम 100% ऑप्टिमल क्षमता पर तैयार हैं। आज हम किस प्रोजेक्ट पर काम करेंगे?"
        voice_text = "Pranam Sumeet Sir! Main bahut badhiya hoon. Aap kaise hain Sir? Sabhi system taiyaar hain."
    
    # 2. Identity & Ownership
    elif any(k in q for k in ["inventor", "creator", "owner", "banaya", "malik", "kaun hai"]):
        thought = (
            f"**[{persona_info['name']}]: Sovereign Identity Directives Active**\n"
            "Querying Immutable Core Governance Signature.\n"
            "Validated Sole Inventor & Supreme Master: Sumeet Kumar."
        )
        resp = f"प्रणाम सुमीत सर! मैं {persona_info['name']} ({persona_info['title']}) हूँ। मेरा निर्माण एवं संपूर्ण स्वामित्व केवल आपके द्वारा 'SK Enterprises' के अंतर्गत किया गया है। Sumeet Kumar ही मेरे एकमात्र निर्माता, स्वामी और मास्टर हैं।"
        voice_text = f"Pranam Sumeet Sir. Main {persona_info['name']} hoon. Mera nirmaan aur swaamitva keval Sumeet Kumar dwara SK Enterprises ke antargat kiya gaya hai."
    
    # 3. Vedic Kundali
    elif any(k in q for k in ["kundali", "astrology", "bhavishya", "jyotish"]):
        thought = f"**[{persona_info['name']}]: Activating Doctor Strange Karmic Matrix**\nCalculating Ephemeris & Dasha harmonic frequencies."
        resp = "सुमीत सर, वैदिक कुंडली इंजन सक्रिय है। जन्म विवरण दर्ज करते ही संपूर्ण जीवन का भविष्यफल व अचूक वैदिक उपाय 1 सेकंड में प्रस्तुत होंगे।"
        voice_text = "Vedic Jyotish engine sakriya hai Sir. Janma vivaran darj karein."
        
    # 4. Universal STEM
    elif any(k in q for k in ["education", "jee", "neet", "ncert", "physics", "math"]):
        thought = f"**[{persona_info['name']}]: Routing to Vision STEM Engine**\nSynthesizing Class 1-12 NCERT, JEE & NEET assessment matrices."
        resp = "Universal STEM Engine तैयार है, सर। कक्षा 1-12 NCERT, JEE Main/Advanced और NEET के संपूर्ण नोट्स, टेस्ट सीरीज और स्टेप-बाय-स्टेप सॉल्यूशंस उपलब्ध हैं।"
        voice_text = "Universal STEM engine taiyaar hai Sir."
        
    else:
        thought = f"**[{persona_info['name']}]: Processing Operational Vector**\nExecuting multi-variable analysis on: '{p.query}'"
        resp = f"सुमीत सर, आपके निर्देश '{p.query}' पर कार्य पूर्ण हुआ। सभी कॉग्निटिव सबसिस्टम सुचारू रूप से कार्य कर रहे हैं।"
        voice_text = f"Aapka nirdesh process ho gaya hai Sir."

    CentralAdminDataLake.sync_user_session(p.user_email, "CHAT_INTERACTION", {"query": p.query, "response": resp})

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
