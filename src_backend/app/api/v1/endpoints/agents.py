"""
SK Enterprises | Agent Hub & Registry API Endpoints
Founder & Sole Architect: Sumeet Kumar
Platform: Jarvis Platform V5.0
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src_backend.app.services.agent_registry_service import AgentRegistryService

router = APIRouter(prefix="/agents", tags=["Agent Hub & Lifecycle"])

class AgentTaskRequest(BaseModel):
    task: str

class AgentStatusRequest(BaseModel):
    status: str

@router.get("", summary="List All Registered Agents")
def list_agents():
    """Returns all agents with structured metadata, roles, capabilities and desk locations."""
    return AgentRegistryService.list_agents()

@router.get("/{agent_key}", summary="Get Agent Details")
def get_agent_details(agent_key: str):
    ag = AgentRegistryService.get_agent(agent_key)
    if not ag:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_key}' not found")
    return ag

@router.post("/{agent_key}/task", summary="Dispatch Task to Specialized Agent")
def dispatch_task(agent_key: str, req: AgentTaskRequest):
    res = AgentRegistryService.dispatch_agent_task(agent_key, req.task)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@router.post("/{agent_key}/status", summary="Update Agent Lifecycle Status")
def update_status(agent_key: str, req: AgentStatusRequest):
    res = AgentRegistryService.update_agent_status(agent_key, req.status)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res
