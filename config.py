import os
from dotenv import load_dotenv
from core.system_paths import BASE_DIR, APPDATA_DIR, LOGS_DIR

# Load environment variables from .env file, if present
load_dotenv(BASE_DIR / ".env")

# Basic Details
PROJECT_NAME = "SK AI 4.0"
OWNER = "Inventor Usman"

# Flags
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Paths available for other modules
PATHS = {
    "BASE_DIR": BASE_DIR,
    "APPDATA_DIR": APPDATA_DIR,
    "LOGS_DIR": LOGS_DIR,
    "VISUAL_HUB": os.path.join(BASE_DIR, "VisualHub"),
    "CORE": os.path.join(BASE_DIR, "core"),
    "NOTES_DB": os.path.join(BASE_DIR, "admin_central_storage", "notes"),
    "MEMORY_DB": os.path.join(BASE_DIR, "admin_central_storage", "memory"),
}