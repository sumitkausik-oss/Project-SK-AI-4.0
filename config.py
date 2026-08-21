"""
SK Enterprises | Global Configuration Loader
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI — Powered by SK Enterprises
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from core.system_paths import BASE_DIR, APPDATA_DIR, LOGS_DIR

# Load environment variables from .env file, if present
load_dotenv(BASE_DIR / ".env")

# Primary Identity Details
PROJECT_NAME = "SKAI"
TAGLINE = "SKAI — Powered by SK Enterprises"
CODENAME = "SKAI Desktop"
PLATFORM_VERSION = "5.0.0"
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
DB_PATH = APPDATA_DIR / "skai_master.db"
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
    "FRONTEND": BASE_DIR / "frontend",
    "BACKEND": BASE_DIR / "src_backend",
    "CORE": BASE_DIR / "core",
}