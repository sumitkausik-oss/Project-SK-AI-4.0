"""
Unit and Integration Tests for SKAI Local Memory Management
Founder & Sole Architect: Sumeet Kumar
"""
import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src_backend.app.database.base import Base
from src_backend.app.repositories.memory_repo import MemoryRepository

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_store_and_retrieve_memory(test_db):
    item = MemoryRepository.store_memory(
        db=test_db,
        key="UI Theme Preference",
        content="User Sumeet prefers futuristic dark mode with cyan accents.",
        tags=["theme", "preferences", "ui"]
    )
    assert item.id is not None
    assert item.key == "UI Theme Preference"

    fetched = MemoryRepository.get_memory(test_db, "UI Theme Preference")
    assert fetched is not None
    assert "cyan accents" in fetched.content

def test_associative_memory_recall(test_db):
    MemoryRepository.store_memory(test_db, "Favorite Editor", "VS Code with Python extensions", tags=["ide", "coding"])
    MemoryRepository.store_memory(test_db, "Working Location", "Patna, Bihar headquarters", tags=["geo", "office"])

    recalled = MemoryRepository.recall_associative(test_db, "What is my favorite coding IDE?", limit=2)
    assert len(recalled) >= 1
    assert recalled[0].key == "Favorite Editor"

def test_delete_memory(test_db):
    item = MemoryRepository.store_memory(test_db, "Temp Memory", "Temporary note to be deleted", tags=["temp"])
    assert MemoryRepository.get_memory(test_db, "Temp Memory") is not None

    deleted = MemoryRepository.delete_memory(test_db, item.id)
    assert deleted is True
    assert MemoryRepository.get_memory(test_db, "Temp Memory") is None
