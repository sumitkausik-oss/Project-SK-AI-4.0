"""
SK Enterprises | Request & Performance Logging Middleware
Inventor & Sole Architect: Sumeet Kumar
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src_backend.app.core.logging_config import get_logger

logger = get_logger("API_ACCESS")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            
            # Log successful requests
            if request.url.path not in ("/api/v1/health/live", "/health/live"):
                logger.info(f"{request.method} {request.url.path} - {response.status_code} ({duration_ms}ms)")
                
            return response
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(f"{request.method} {request.url.path} - FAILED ({duration_ms}ms): {e}", exc_info=True)
            raise e
