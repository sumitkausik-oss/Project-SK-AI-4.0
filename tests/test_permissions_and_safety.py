"""
Unit and Integration Tests for SKAI Permissions and Safety Layer
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
from src_backend.app.services.permission_service import PermissionService, ActionCategory
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

def test_action_categorization():
    assert PermissionService.categorize_action("SEARCH_LOCAL_FILES") == ActionCategory.READ_ONLY
    assert PermissionService.categorize_action("READ_FILE") == ActionCategory.READ_ONLY
    assert PermissionService.categorize_action("TAKE_SCREENSHOT") == ActionCategory.READ_ONLY
    assert PermissionService.categorize_action("CREATE_FILE") == ActionCategory.REVERSIBLE_WRITE
    assert PermissionService.categorize_action("DELETE_FILE") == ActionCategory.DESTRUCTIVE_HIGH_IMPACT
    assert PermissionService.categorize_action("TERMINAL_COMMAND") == ActionCategory.DESTRUCTIVE_HIGH_IMPACT

def test_evaluation_of_read_only_action():
    eval_res = PermissionService.evaluate_request("READ_FILE", {"file_path": "test.txt"}, "Read test file")
    assert eval_res["allowed"] is True
    assert eval_res["requires_confirmation"] is False

def test_evaluation_of_destructive_action():
    eval_res = PermissionService.evaluate_request("DELETE_FILE", {"target_path": "test.txt"}, "Delete test file")
    assert eval_res["allowed"] is False
    assert eval_res["requires_confirmation"] is True
    assert "action_id" in eval_res
    
    # Check pending list
    pending = PermissionService.get_pending_action(eval_res["action_id"])
    assert pending is not None
    assert pending["action_type"] == "DELETE_FILE"

def test_confirm_pending_action_workflow(test_db):
    eval_res = PermissionService.evaluate_request("DELETE_FILE", {"target_path": "non_existent_dummy.txt"}, "Delete dummy file")
    action_id = eval_res["action_id"]

    # Reject
    reject_res = AssistantService.execute_confirmed_action(test_db, action_id, approved=False)
    assert reject_res["success"] is True
    assert reject_res["status"] == "REJECTED"

    # Verify popped
    assert PermissionService.get_pending_action(action_id) is None
