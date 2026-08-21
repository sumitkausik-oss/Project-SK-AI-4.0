"""
SK Enterprises | API v1 Master Router
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System
"""
from fastapi import APIRouter
from src_backend.app.api.v1.endpoints.health import router as health_router
from src_backend.app.api.v1.endpoints.system import router as system_router
from src_backend.app.api.v1.endpoints.chat import router as chat_router
from src_backend.app.api.v1.endpoints.os_control import router as os_control_router
from src_backend.app.api.v1.endpoints.permissions import router as permissions_router
from src_backend.app.api.v1.endpoints.memory import router as memory_router
from src_backend.app.api.v1.endpoints.astrology import router_agent_town, router_astrology
from src_backend.app.api.v1.endpoints.education_data_cloud import (
    router_education, router_data, router_cloud
)
from src_backend.app.api.v1.endpoints.admin import router as admin_router
from src_backend.app.api.v1.endpoints.intelligence import router as intelligence_router
from src_backend.app.api.v1.endpoints.agents import router as agents_router
from src_backend.app.api.v1.endpoints.providers import router as providers_router
from src_backend.app.api.v1.endpoints.diagnostics import router as diagnostics_router

api_v1_router = APIRouter()

# Register core OS Control, Safety & Memory sub-routers
api_v1_router.include_router(health_router)
api_v1_router.include_router(system_router)
api_v1_router.include_router(chat_router)
api_v1_router.include_router(os_control_router)
api_v1_router.include_router(permissions_router)
api_v1_router.include_router(memory_router)

# Register specialized modular capabilities
api_v1_router.include_router(router_agent_town)
api_v1_router.include_router(router_astrology)
api_v1_router.include_router(router_education)
api_v1_router.include_router(router_data)
api_v1_router.include_router(router_cloud)
api_v1_router.include_router(admin_router)
api_v1_router.include_router(intelligence_router)
api_v1_router.include_router(agents_router)
api_v1_router.include_router(providers_router)
api_v1_router.include_router(diagnostics_router)
