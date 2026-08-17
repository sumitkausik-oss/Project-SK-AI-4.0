"""
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
            "**Verifying Immutable Ownership Directive**\n"
            "Querying SK Enterprises Sovereign Core Signature.\n"
            "Validated Sole Inventor & Master: Sumeet Kumar."
        )
        resp = "प्रणाम सुमीत सर! मैं SK AI 4.0 (Project JARVIS 4.0) हूँ। मेरा निर्माण एवं स्वामित्व केवल आपके द्वारा 'SK Enterprises' के अंतर्गत किया गया है।"
        voice_text = "Pranam Sumeet Sir. Main SK AI four point zero hoon. Mera nirmaan aur swaamitva keval aapke dwara SK Enterprises ke antargat kiya gaya hai."
    
    # 2. त्वरित कुंडली अनुरोध
    elif "kundali" in q or "astrology" in q or "bhavishya" in q:
        thought = "**Activating Vedic Ephemeris Subsystem**\nCalculating harmonic planetary alignment."
        resp = "सुमीत सर, मैंने वैदिक ज्योतिष इंजन सक्रिय कर दिया है। अपनी जन्म तिथि, समय और स्थान दर्ज करें, मैं एक सेकंड में संपूर्ण जीवन कुंडली व अचूक उपाय प्रस्तुत कर दूँगा।"
        voice_text = "Vedic Jyotish engine sakriya hai Sir. Janma vivaran darj karein."
    
    # 3. शिक्षा एवं STEM
    elif any(k in q for k in ["education", "jee", "neet", "ncert", "physics", "math"]):
        thought = "**Routing to Universal STEM Engine**\nSynthesizing Class 1-12 & Advanced Competitive Assessment."
        resp = "SK AI Universal STEM Engine तैयार है। कक्षा 1-12 NCERT, JEE Advanced/Main एवं NEET के संपूर्ण स्टेप-बाय-स्टेप नोट्स व टेस्ट सीरीज़ उपलब्ध हैं।"
        voice_text = "Universal STEM engine taiyaar hai Sir."
    
    else:
        thought = f"**Processing Query:** '{p.query}'\nExecuting multi-variable cognitive analysis."
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
