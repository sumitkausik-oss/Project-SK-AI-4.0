"""
SK AI 4.0 — Local Foundation (Phase 1)
========================================
A real, runnable FastAPI backend wiring together four nodes:
Memory, Skills, Soul, Settings.

Run with:
    python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

Then open http://127.0.0.1:8000/docs for interactive API docs.

Scope note: this is a genuine working foundation, not a finished
product. It runs locally on one machine, with no cloud sync, no
license-key gate, and no auto-executing arbitrary code — those pieces
from the original spec are commercial/legal or safety-sensitive
decisions that deserve to be made deliberately later, not defaulted
into existence.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from memory import store as memory_store
from skills import registry as skills_registry
from soul import persona as soul_persona
from settings import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    memory_store._connect().close()  # ensures tables exist on boot
    yield


app = FastAPI(title=config.APP_NAME, lifespan=lifespan)


# ---------- Schemas ----------

class RememberRequest(BaseModel):
    key: str
    value: str


class SkillRequest(BaseModel):
    name: str
    args: dict = {}


class ChatTurn(BaseModel):
    role: str
    content: str


# ---------- Root ----------

@app.get("/")
def root():
    return {
        "app": config.APP_NAME,
        "status": "running",
        "nodes": ["memory", "skills", "soul", "settings"],
        "persona": config.DEFAULT_PERSONA,
    }


# ---------- Memory Node ----------

@app.post("/memory/remember")
def remember(req: RememberRequest):
    memory_store.remember(req.key, req.value)
    return {"stored": req.key}


@app.get("/memory/recall/{key}")
def recall(key: str):
    value = memory_store.recall(key)
    if value is None:
        raise HTTPException(status_code=404, detail=f"No memory found for '{key}'")
    return {"key": key, "value": value}


@app.get("/memory/recent")
def recent(limit: int = 20):
    return {"turns": memory_store.recent_turns(limit)}


# ---------- Skills Node ----------

@app.get("/skills/list")
def list_skills():
    return {"skills": skills_registry.list_skills()}


@app.post("/skills/run")
def run_skill(req: SkillRequest):
    try:
        result = skills_registry.run_skill(req.name, **req.args)
        return {"skill": req.name, "result": result}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Bad arguments: {e}")


# ---------- Soul Node ----------

@app.get("/soul/personas")
def personas():
    return soul_persona.list_personas()


@app.get("/soul/current")
def current_persona():
    return soul_persona.get_persona(config.DEFAULT_PERSONA)


# ---------- Settings Node ----------

@app.get("/settings")
def settings_view():
    return {
        "host": config.HOST,
        "port": config.PORT,
        "default_persona": config.DEFAULT_PERSONA,
    }


# ---------- Chat log passthrough (wires memory into a conversation) ----------

@app.post("/chat/log")
def log_chat(turn: ChatTurn):
    memory_store.log_turn(turn.role, turn.content)
    return {"logged": True}
