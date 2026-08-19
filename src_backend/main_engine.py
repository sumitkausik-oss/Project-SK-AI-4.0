"""
========================================================================================
                 SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)
           INVENTOR & SOLE ARCHITECT: Sumeet Kumar | NATIVE COGNITIVE OS
========================================================================================
Native High-Performance Autonomous Cognitive Backend Engine (FastAPI + WebSockets)
Platform: Jarvis Platform V5.0
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import consolidated, production-grade application factory
from src_backend.app.main import app, create_app
from src_backend.app.core.config import settings
from src_backend.app.services.agent_town_service import AGENTS_STATE

# Export components for backward compatibility
__all__ = ["app", "create_app", "settings", "AGENTS_STATE"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src_backend.main_engine:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
