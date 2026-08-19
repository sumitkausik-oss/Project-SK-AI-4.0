"""
SK Enterprises | Health & Liveness Endpoints
Inventor & Sole Architect: Sumeet Kumar
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src_backend.app.database.base import get_db
from src_backend.app.schemas.health import HealthResponse, ReadinessResponse
from src_backend.app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])

@router.get("", response_model=HealthResponse, summary="Get Application Health Status")
@router.get("/live", response_model=HealthResponse, summary="Liveness Probe")
def get_liveness():
    """Liveness probe: verifies that the FastAPI process is running."""
    return HealthService.get_health()

@router.get("/ready", response_model=ReadinessResponse, summary="Readiness Probe")
def get_readiness(db: Session = Depends(get_db)):
    """Readiness probe: verifies backend and database connectivity."""
    return HealthService.get_readiness(db)
