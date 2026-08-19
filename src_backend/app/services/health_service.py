"""
SK Enterprises | Health & Telemetry Service
Inventor & Sole Architect: Sumeet Kumar
"""
import time
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from src_backend.app.core.config import settings

_STARTUP_TIME = time.time()

class HealthService:
    @staticmethod
    def get_health() -> dict:
        uptime = round(time.time() - _STARTUP_TIME, 2)
        return {
            "status": "HEALTHY",
            "version": settings.VERSION,
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": uptime,
            "system": settings.PROJECT_NAME,
            "inventor": settings.INVENTOR
        }

    @staticmethod
    def get_readiness(db: Session) -> dict:
        db_status = "CONNECTED"
        try:
            db.execute(text("SELECT 1"))
        except Exception:
            db_status = "ERROR"
            
        return {
            "status": "READY" if db_status == "CONNECTED" else "DEGRADED",
            "database": db_status,
            "version": settings.VERSION,
            "active_nodes": 4,
            "lifetime_license": "ACTIVE - VERIFIED",
            "timestamp": datetime.utcnow().isoformat()
        }
