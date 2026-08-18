import json
from pathlib import Path
from config import PATHS

MEMORY_FILE = PATHS["BASE_DIR"] / "data/users/1001/memory/memory.json"

class MemoryManager:
    def __init__(self):
        self.memory = self._load_memory()

    def _load_memory(self):
        try:
            if MEMORY_FILE.exists():
                with open(MEMORY_FILE, 'r') as f:
                    return json.load(f)
            return {"interactions": [], "preferences": {}}
        except Exception:
            return {"interactions": [], "preferences": {}}

    def save_interaction(self, user_input, assistant_output):
        interaction = {"user": user_input, "assistant": assistant_output}
        self.memory["interactions"].append(interaction)
        self._save_to_disk()

    def _save_to_disk(self):
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def get_recent_interactions(self, limit=5):
        return self.memory["interactions"][-limit:]

    # NEW: Search functionality for Recall
    def search_memory(self, query, limit=5):
        results = []
        # Simple string matching for now
        for interaction in reversed(self.memory["interactions"]):
            if query.lower() in interaction["user"].lower() or query.lower() in interaction["assistant"].lower():
                results.append(interaction)
                if len(results) >= limit:
                    break
        return results
