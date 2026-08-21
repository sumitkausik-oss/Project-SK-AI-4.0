"""
SK Enterprises | SKAI Safety & Permission Gatekeeper
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System

Enforces strict action categories, trust levels, and user confirmations:
- READ_ONLY: Auto-approved (search, read file, list folder, screenshot, status)
- REVERSIBLE_WRITE: Light confirmation or pre-approved (create file/folder, move file, open app)
- DESTRUCTIVE_HIGH_IMPACT: Strict confirmation gate (delete file/folder, run terminal command, close apps, overwrite files)
"""
import uuid
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from core.system_paths import APPDATA_DIR, BASE_DIR
from src_backend.app.repositories.memory_repo import AuditRepository

PERMISSIONS_CONFIG_FILE = APPDATA_DIR / "permissions_config.json"

class ActionCategory:
    READ_ONLY = "READ_ONLY"
    REVERSIBLE_WRITE = "REVERSIBLE_WRITE"
    DESTRUCTIVE_HIGH_IMPACT = "DESTRUCTIVE_HIGH_IMPACT"

class PermissionService:
    """Manages safety policies, folder whitelisting, and pending confirmation queues."""

    _pending_actions: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def get_policy(cls) -> Dict[str, Any]:
        """Loads permission policies or returns sensible defaults."""
        defaults = {
            "auto_approve_read_only": True,
            "auto_approve_reversible": True,
            "require_confirmation_for_destructive": True,
            "require_confirmation_for_terminal": True,
            "web_tools_enabled": False,  # Off by default per master requirements
            "allowed_directories": [
                str(Path.home() / "Desktop"),
                str(Path.home() / "Documents"),
                str(Path.home() / "Downloads"),
                str(BASE_DIR)
            ]
        }

        if PERMISSIONS_CONFIG_FILE.exists():
            try:
                data = json.loads(PERMISSIONS_CONFIG_FILE.read_text(encoding="utf-8"))
                defaults.update(data)
            except Exception:
                pass

        return defaults

    @classmethod
    def save_policy(cls, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Persists updated permissions settings to disk."""
        current = cls.get_policy()
        current.update(policy)
        try:
            PERMISSIONS_CONFIG_FILE.write_text(json.dumps(current, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"[PERMISSION ERROR]: Failed to save policy: {e}")
        return current

    @classmethod
    def set_policy(cls, **kwargs) -> Dict[str, Any]:
        """Helper to update policy flags directly via keyword arguments."""
        return cls.save_policy(kwargs)

    @classmethod
    def categorize_action(cls, action_type: str) -> str:
        """Determines the trust level category for a requested action."""
        action = action_type.upper()
        if action in ["SEARCH_LOCAL_FILES", "READ_FILE", "LIST_FOLDER", "TAKE_SCREENSHOT", "SYSTEM_STATUS", "GET_MEMORY"]:
            return ActionCategory.READ_ONLY
        elif action in ["CREATE_FILE", "CREATE_FOLDER", "OPEN_APP", "MOVE_FILE", "STORE_MEMORY"]:
            return ActionCategory.REVERSIBLE_WRITE
        elif action in ["DELETE_FILE", "CLOSE_APP", "TERMINAL_COMMAND", "WRITE_FILE", "DELETE_MEMORY", "CODE_ASSIST_EDIT"]:
            return ActionCategory.DESTRUCTIVE_HIGH_IMPACT
        else:
            return ActionCategory.DESTRUCTIVE_HIGH_IMPACT

    @classmethod
    def evaluate_request(cls, action_type: str, params: Dict[str, Any], description: str) -> Dict[str, Any]:
        """
        Evaluates whether an action can execute immediately or requires explicit user confirmation.
        Returns evaluation dict with 'allowed', 'category', and optional 'action_id'.
        """
        category = cls.categorize_action(action_type)
        policy = cls.get_policy()

        # 1. READ_ONLY actions are always allowed immediately
        if category == ActionCategory.READ_ONLY:
            return {
                "allowed": True,
                "category": category,
                "requires_confirmation": False
            }

        # 2. REVERSIBLE_WRITE
        if category == ActionCategory.REVERSIBLE_WRITE:
            if policy.get("auto_approve_reversible", True):
                return {
                    "allowed": True,
                    "category": category,
                    "requires_confirmation": False
                }

        # 3. DESTRUCTIVE_HIGH_IMPACT
        needs_confirm = False
        if action_type.upper() == "TERMINAL_COMMAND":
            needs_confirm = policy.get("require_confirmation_for_terminal", True)
        else:
            needs_confirm = policy.get("require_confirmation_for_destructive", True)

        if needs_confirm:
            action_id = f"act_{uuid.uuid4().hex[:8]}"
            cls._pending_actions[action_id] = {
                "action_id": action_id,
                "action_type": action_type,
                "category": category,
                "params": params,
                "description": description,
                "status": "PENDING",
                "created_at": datetime.utcnow().isoformat()
            }
            return {
                "allowed": False,
                "category": category,
                "requires_confirmation": True,
                "action_id": action_id,
                "message": f"Action '{action_type}' is classified as {category} and requires explicit confirmation."
            }

        return {
            "allowed": True,
            "category": category,
            "requires_confirmation": False
        }

    @classmethod
    def get_pending_action(cls, action_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves details of a pending action by ID."""
        return cls._pending_actions.get(action_id)

    @classmethod
    def pop_pending_action(cls, action_id: str) -> Optional[Dict[str, Any]]:
        """Pops and removes a pending action from the queue."""
        return cls._pending_actions.pop(action_id, None)

    @classmethod
    def list_pending_actions(cls) -> List[Dict[str, Any]]:
        """Lists all currently pending confirmation requests."""
        return list(cls._pending_actions.values())
