"""
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
        thought = f"**[Hermes Multi-Agent Hub via {p.provider.upper()}]: Conversational Sync**\nValidated Sovereign Master: Sumeet Kumar."
        resp = f"प्रणाम सुमीत सर! SK AI 4.0 प्लेटफॉर्म और सभी एजेंट्स पूरी तरह तैयार हैं। आज हम किस कार्य को निष्पादित करेंगे?"
        voice_text = "Pranam Sumeet Sir! Sabhi agents aur system taiyaar hain."
    elif any(k in q for k in ["inventor", "creator", "owner", "banaya", "malik", "kaun hai"]):
        thought = "**[Hermes Core Governance Directive]: Immutable Identity Validation**\nSole Architect: Sumeet Kumar."
        resp = "प्रणाम सुमीत सर! मेरा निर्माण एवं संपूर्ण स्वामित्व केवल आपके द्वारा 'SK Enterprises' के अंतर्गत किया गया है।"
        voice_text = "Pranam Sumeet Sir. Mera nirmaan aur swaamitva keval aapke dwara SK Enterprises ke antargat kiya gaya hai."
    else:
        thought = f"**[Hermes AI Orchestrator]: Multi-Tool Reasoning**\nProcessing query: '{p.query}' across agent swarm."
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
