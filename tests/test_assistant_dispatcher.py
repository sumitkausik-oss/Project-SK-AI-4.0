"""
Unit and Integration Tests for SKAI Master Assistant & Natural Language Dispatcher
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
from src_backend.app.services.assistant_service import AssistantService

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

def test_assistant_creator_query(test_db):
    res = AssistantService.process_command(test_db, "Who made you?")
    assert res["status"] == "COMPLETED"
    assert "Sumeet Kumar" in res["response"]
    assert "SK Enterprises" in res["response"]

def test_assistant_memory_store_and_recall_intent(test_db):
    # Store
    res_store = AssistantService.process_command(test_db, "Remember that I love dark mode HUDs")
    assert res_store["status"] == "COMPLETED"
    assert res_store["action"] == "STORE_MEMORY"
    assert "Memory Stored" in res_store["response"]

    # Recall
    res_recall = AssistantService.process_command(test_db, "What do you remember?")
    assert res_recall["status"] == "COMPLETED"
    assert "dark mode" in res_recall["response"].lower()

def test_assistant_screenshot_intent(test_db):
    res = AssistantService.process_command(test_db, "take a screenshot")
    assert res["status"] == "COMPLETED"
    assert res["action"] == "TAKE_SCREENSHOT"
    assert "Screenshot Captured" in res["response"]

def test_assistant_destructive_delete_triggers_safety_gate(test_db):
    res = AssistantService.process_command(test_db, "delete file important_system.txt")
    assert res["status"] == "REQUIRES_CONFIRMATION"
    assert res["action"] == "DELETE_FILE"
    assert "action_id" in res
    assert "Safety Confirmation Required" in res["response"]
