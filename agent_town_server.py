import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SK AI 4.0 Cognitive Engine", version="4.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
@app.get("/health")
def health():
    return {
        "status": "ONLINE",
        "system": "SK AI 4.0 (Project JARVIS 4.0)",
        "inventor": "Sumit Kumar",
        "organization": "SK Enterprises",
        "tier": "Lifetime Admin",
        "domains": ["Universal Education", "Data Analyst Suite", "Cloud DevOps", "Vedic Astrology"]
    }

@app.get("/api/v1/agents")
def get_agents():
    return {
        "agents": [
            {"id": "stem_engine", "name": "Universal STEM & K-12 Matrix", "status": "ONLINE"},
            {"id": "data_engine", "name": "Autonomous Data Analyst", "status": "ONLINE"},
            {"id": "cloud_devops", "name": "Google Workspace & M365 DevOps", "status": "ONLINE"},
            {"id": "astro_engine", "name": "Vedic Ephemeris Calculator", "status": "ONLINE"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
