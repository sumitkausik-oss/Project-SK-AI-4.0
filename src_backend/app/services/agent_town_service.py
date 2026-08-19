"""
SK Enterprises | 2D Agent Town Simulation Service
Inventor & Sole Architect: Sumeet Kumar
"""
import time
from typing import Dict, Any, List

AGENTS_STATE = [
    {
        "id": "agent_alpha",
        "name": "Bob",
        "role": "Lead Data & Research Analyst",
        "room": "Research Lab",
        "x": 60.0, "y": 70.0,
        "dx": 0.6, "dy": 0.4,
        "status": "Analyzing Knowledge Graph & Neural Weights",
        "color": "#38bdf8",
        "tier": "Master"
    },
    {
        "id": "agent_beta",
        "name": "Carol",
        "role": "Universal Education Architect",
        "room": "Education Matrix",
        "x": 200.0, "y": 90.0,
        "dx": -0.5, "dy": 0.5,
        "status": "Synthesizing JEE Advanced Physics Modules",
        "color": "#f472b6",
        "tier": "Master"
    },
    {
        "id": "agent_gamma",
        "name": "Dave",
        "role": "DevOps & Cloud Engineer",
        "room": "DevOps Center",
        "x": 340.0, "y": 60.0,
        "dx": 0.4, "dy": -0.6,
        "status": "Auditing Google Workspace & M365 Zero-Trust Policies",
        "color": "#34d399",
        "tier": "Master"
    },
    {
        "id": "agent_delta",
        "name": "Arya",
        "role": "Vedic Ephemeris Specialist",
        "room": "Ephemeris Observatory",
        "x": 460.0, "y": 110.0,
        "dx": -0.5, "dy": -0.3,
        "status": "Synchronizing Planetary Harmonic Ephemeris",
        "color": "#fbbf24",
        "tier": "Master"
    }
]

ROOMS_LAYOUT = [
    {"name": "Research Lab", "x": 10, "y": 10, "width": 140, "height": 130, "color": "rgba(56, 189, 248, 0.15)"},
    {"name": "Education Matrix", "x": 160, "y": 10, "width": 140, "height": 130, "color": "rgba(244, 114, 182, 0.15)"},
    {"name": "DevOps Center", "x": 310, "y": 10, "width": 140, "height": 130, "color": "rgba(52, 211, 153, 0.15)"},
    {"name": "Ephemeris Observatory", "x": 460, "y": 10, "width": 140, "height": 130, "color": "rgba(251, 191, 36, 0.15)"}
]

class AgentTownService:
    @staticmethod
    def get_state() -> Dict[str, Any]:
        return {
            "timestamp": time.time(),
            "agents": AGENTS_STATE,
            "rooms": ROOMS_LAYOUT
        }
