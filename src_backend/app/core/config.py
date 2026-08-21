"""
SK Enterprises | SKAI Core Settings Module
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System
"""
import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

from core.system_paths import BASE_DIR, APPDATA_DIR, LOGS_DIR

class Settings(BaseSettings):
    PROJECT_NAME: str = "SKAI"
    TAGLINE: str = "SKAI — Powered by SK Enterprises"
    CODENAME: str = "SKAI Desktop"
    VERSION: str = "5.0.0"
    API_V1_STR: str = "/api/v1"
    
    INVENTOR: str = "Sumeet Kumar"
    FOUNDER: str = "Sumeet Kumar"
    SOLE_ARCHITECT: str = "Sumeet Kumar"
    ORGANIZATION: str = "SK Enterprises"
    
    ENVIRONMENT: str = Field(default="production", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    HOST: str = Field(default="127.0.0.1", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # Database Configuration (SQLite)
    DATABASE_PATH: Path = APPDATA_DIR / "skai_master.db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite:///{self.DATABASE_PATH.as_posix()}"
    
    # CORS Origins (Restricted strictly to local addresses)
    CORS_ORIGINS: List[str] = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null",  # Allows file:/// browser protocol
    ]
    
    # Security Secrets
    SECRET_KEY: str = Field(default="SKAI_SOVEREIGN_KEY_SUMEET_KUMAR_2026_MASTER", env="SECRET_KEY")
    HMAC_SALT: str = Field(default="SK_ENTERPRISES_SUMEET_KUMAR_SKAI_CORE_5_0", env="HMAC_SALT")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOGS_DIR: Path = LOGS_DIR
    
    class Config:
        case_sensitive = True
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
