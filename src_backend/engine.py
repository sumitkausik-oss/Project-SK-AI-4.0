"""
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
        thought = f"**[{persona_info['name']}]: Direct Interpersonal Sync**\nInterpreting conversational intent from Founder Sumit Kumar."
        resp = "प्रणाम सुमित सर! मैं बहुत बढ़िया हूँ। आप कैसे हैं, सर? SK AI 4.0 के सभी न्यूरल सिस्टम 100% ऑप्टिमल क्षमता पर तैयार हैं।"
        voice_text = "Pranam Sumit Sir! Main bahut badhiya hoon. Aap kaise hain Sir? Sabhi system taiyaar hain."
    elif any(k in q for k in ["inventor", "creator", "owner", "banaya", "malik", "kaun hai"]):
        thought = f"**[{persona_info['name']}]: Sovereign Identity Directive**\nValidated Sole Inventor & Supreme Master: Sumit Kumar."
        resp = f"प्रणाम सुमित सर! मैं {persona_info['name']} ({persona_info['role']}) हूँ। मेरा निर्माण एवं संपूर्ण स्वामित्व केवल आपके द्वारा 'SK Enterprises' के अंतर्गत किया गया है।"
        voice_text = f"Pranam Sumit Sir. Main {persona_info['name']} hoon. Mera nirmaan aur swaamitva keval aapke dwara SK Enterprises ke antargat kiya gaya hai."
    elif any(k in q for k in ["kundali", "astrology", "bhavishya", "jyotish"]):
        thought = f"**[{persona_info['name']}]: Activating Doctor Strange Ephemeris Matrix**"
        resp = "सुमित सर, वैदिक कुंडली इंजन सक्रिय है। जन्म विवरण दर्ज करते ही संपूर्ण जीवन का भविष्यफल व अचूक वैदिक उपाय 1 सेकंड में प्रस्तुत होंगे।"
        voice_text = "Vedic Jyotish engine sakriya hai Sir. Janma vivaran darj karein."
    else:
        thought = f"**[{persona_info['name']}]: Executing Autonomous Directive**\nAnalyzing: '{p.query}'"
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
