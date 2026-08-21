"""
SK Enterprises | Structured Logging Configuration
Inventor & Sole Architect: Sumeet Kumar
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src_backend.app.core.config import settings

def setup_logging():
    """Configure structured logging with console and rotating file handlers."""
    log_dir = settings.LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    app_log_file = log_dir / "application.log"
    error_log_file = log_dir / "error.log"
    
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Format: [Timestamp] [Level] [Module:Line] - Message
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        
    # 1. Console Handler (Safe UTF-8 encoding on Windows)
    stream = sys.stdout
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    console_handler = logging.StreamHandler(stream)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 2. Rotating File Handler for all logs (10 MB per file, 5 backups)
    app_file_handler = RotatingFileHandler(
        filename=app_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    app_file_handler.setLevel(log_level)
    app_file_handler.setFormatter(formatter)
    root_logger.addHandler(app_file_handler)
    
    # 3. Rotating File Handler for ERROR+ logs only
    error_file_handler = RotatingFileHandler(
        filename=error_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    root_logger.addHandler(error_file_handler)
    
    # Suppress verbose 3rd party logs in production
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    
    logging.info(f"Structured logging initialized. Log files at: {log_dir}")

def get_logger(name: str) -> logging.Logger:
    """Helper to get a named logger."""
    return logging.getLogger(name)
