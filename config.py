"""
SK Enterprises | Global Configuration Loader
Inventor & Sole Architect: Sumeet Kumar
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from core.system_paths import BASE_DIR, APPDATA_DIR, LOGS_DIR

# Load environment variables from .env file, if present
load_dotenv(BASE_DIR / ".env")

# Primary Identity Details
PROJECT_NAME = "SK AI 4.0"
CODENAME = "Project JARVIS 4.0"
PLATFORM_VERSION = "Jarvis Platform V5.0"
OWNER = "Sumeet Kumar"
INVENTOR = "Sumeet Kumar"
ORGANIZATION = "SK Enterprises"

# System Flags
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production").lower()

# Network Configuration
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))

# Storage and Database Paths (UAC-Safe)
DB_PATH = APPDATA_DIR / "sk_ai_master.db"
STORAGE_DIR = APPDATA_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Standardized Paths Dictionary
PATHS = {
    "BASE_DIR": BASE_DIR,
    "APPDATA_DIR": APPDATA_DIR,
    "LOGS_DIR": LOGS_DIR,
    "STORAGE_DIR": STORAGE_DIR,
    "DB_PATH": DB_PATH,
    "CONFIG": BASE_DIR / "config",
    "ASSETS": BASE_DIR / "assets",
    "FRONTEND": BASE_DIR / "src_frontend",
    "BACKEND": BASE_DIR / "src_backend",
    "CORE": BASE_DIR / "core",
}