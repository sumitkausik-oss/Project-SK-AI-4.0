"""
SK Enterprises | SKAI Master Cognitive Backend Engine
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI — Powered by SK Enterprises
"""
import sys
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src_backend.app.core.config import settings
from src_backend.app.core.logging_config import setup_logging, get_logger
from src_backend.app.database.init_db import init_database
from src_backend.app.middleware.logging_middleware import LoggingMiddleware
from src_backend.app.api.v1.router import api_v1_router
from src_backend.app.websocket.telemetry import websocket_telemetry_endpoint, telemetry_manager

# Ensure base directory in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle manager."""
    # 1. Startup
    setup_logging()
    logger.info("=" * 80)
    logger.info(f"[SKAI] SK ENTERPRISES | {settings.PROJECT_NAME} ({settings.TAGLINE})")
    logger.info(f"   FOUNDER & SOLE ARCHITECT: {settings.INVENTOR}")
    logger.info(f"   PLATFORM VERSION: {settings.VERSION} | LOCAL COGNITIVE ASSISTANT STARTUP")
    logger.info("=" * 80)
    
    # Initialize SQLite Database & Tables
    init_database()
    
    # Start WebSocket background broadcaster
    telemetry_task = asyncio.create_task(telemetry_manager.broadcast_telemetry())
    
    yield
    
    # 2. Shutdown
    logger.info("Shutting down SKAI Engine...")
    telemetry_task.cancel()
    try:
        await telemetry_task
    except asyncio.CancelledError:
        pass
    logger.info("All background tasks gracefully terminated.")

def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title=f"{settings.PROJECT_NAME} — Powered by {settings.ORGANIZATION}",
        description=f"Local-First Desktop AI Assistant engineered by {settings.INVENTOR} ({settings.ORGANIZATION})",
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # 1. Security & CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Custom Logging Middleware
    app.add_middleware(LoggingMiddleware)

    # 3. Global Exception Handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception on {request.method} {request.url.path}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Cognitive Core Exception",
                "message": str(exc) if settings.DEBUG else "An unexpected error occurred. Please consult the system logs.",
                "system": settings.PROJECT_NAME,
                "architect": settings.INVENTOR
            }
        )

    # 4. Mount Versioned API Routes (/api/v1/...)
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    # 5. Backward Compatibility Route Aliases (mount /api/... without /v1/ for legacy frontends)
    app.include_router(api_v1_router, prefix="/api")

    # 6. WebSocket Endpoints
    app.add_api_websocket_route("/ws/telemetry", websocket_telemetry_endpoint)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src_backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
