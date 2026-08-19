"""
SK Enterprises | Agent Town & Astrology Endpoints
Inventor & Sole Architect: Sumeet Kumar
"""
from fastapi import APIRouter
from src_backend.app.schemas.astrology import KundaliPayload, AstrologyRequest
from src_backend.app.services.astrology_service import AstrologyService
from src_backend.app.services.agent_town_service import AgentTownService

router_agent_town = APIRouter(tags=["2D Agent Town"])

@router_agent_town.get("/agent_town/state", summary="Get 2D Agent Town State")
@router_agent_town.get("/agent_town/agents", summary="Get Agent Town State (Alias)")
def get_agent_town_state():
    return AgentTownService.get_state()

router_astrology = APIRouter(tags=["Vedic Astrology & Ephemeris"])

@router_astrology.post("/kundali/generate", summary="Generate 1-Second Lifelong Kundali Report")
def generate_kundali_report(p: KundaliPayload):
    return AstrologyService.calculate_kundali(p.name, p.dob, p.tob, p.pob)

@router_astrology.post("/astrology/kundali", summary="Calculate Astrological Harmonic Chart")
def calculate_kundali(req: AstrologyRequest):
    return AstrologyService.get_detailed_report(req.dob, req.tob, req.location, req.ayanamsa)
