import json
from config import PATHS

class PersonaManager:
    def __init__(self, persona_name="SKAI"):
        self.persona_data = self._load_persona(persona_name)

    def _load_persona(self, name):
        persona_file = PATHS["BASE_DIR"] / f"core/personae/{name.lower()}.json"
        try:
            with open(persona_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"name": "SKAI", "voice": "assistant", "tone": "refinement"}
