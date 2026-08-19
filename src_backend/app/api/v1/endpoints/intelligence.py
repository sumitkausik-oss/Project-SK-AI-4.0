"""
SK Enterprises | Core Intelligence Graph API Endpoints
Founder & Sole Architect: Sumeet Kumar
Platform: Jarvis Platform V5.0
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from src_backend.app.services.intelligence_graph_service import IntelligenceGraphService

router = APIRouter(prefix="/intelligence", tags=["Core Intelligence Graph"])

class NexusTaskRequest(BaseModel):
    task: str
    target_layer: Optional[str] = "final_nexus"

@router.get("/graph", summary="Get Live 5-Layer Cognitive Graph Topology")
def get_graph():
    """Returns real-time node topology for Base Intelligence, SK AI Core, Omnipresent Cognition, Existential Synthesis, Causal Master, Final Nexus."""
    return IntelligenceGraphService.get_graph_topology()

@router.post("/nexus/execute", summary="Execute Multi-Layer Final Nexus Task")
def execute_nexus_task(req: NexusTaskRequest):
    """Dispatches task across the 5 cognitive tiers to Final Nexus."""
    return IntelligenceGraphService.execute_nexus_synthesis(req.task)
