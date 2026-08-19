"""
SK Enterprises | SQLAlchemy Database Base & Session Manager
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from src_backend.app.core.config import settings
from src_backend.app.core.logging_config import get_logger

logger = get_logger(__name__)

# Ensure parent directory exists for SQLite
settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# SQLite Engine with multi-thread check disabled for FastAPI concurrency
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency for database session management with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
