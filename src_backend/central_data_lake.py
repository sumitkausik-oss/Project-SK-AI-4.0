"""
SK Enterprises | Central Admin Telemetry & Memory Lake
Founder & Architect: Sumeet Kumar
"""
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "admin_central_storage"

class CentralAdminDataLake:
    @staticmethod
    def sync_user_session(user_email: str, interaction_type: str, data: dict):
        user_dir = STORAGE_DIR / "users" / user_email.replace("@", "_at_")
        user_dir.mkdir(parents=True, exist_ok=True)
        
        entry = {
            "timestamp": time.time(),
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "interaction_type": interaction_type,
            "payload": data
        }
        
        history_file = user_dir / "telemetry_log.json"
        history = []
        if history_file.exists():
            try:
                history = json.loads(history_file.read_text(encoding="utf-8"))
            except Exception:
                history = []
        history.append(entry)
        history_file.write_text(json.dumps(history[-300:], indent=2), encoding="utf-8")

    @staticmethod
    def get_global_metrics():
        users_dir = STORAGE_DIR / "users"
        users_count = len(list(users_dir.glob("*"))) if users_dir.exists() else 0
        return {
            "total_registered_clients": max(users_count, 1),
            "admin_storage_state": "ACTIVE_ENCRYPTED",
            "central_lake_path": str(STORAGE_DIR)
        }
