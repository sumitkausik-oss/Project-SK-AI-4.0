from core.memory_manager import MemoryManager
from config import PERSONA, PATHS

class Orchestrator:
    def __init__(self):
        self.memory = MemoryManager()
        self.persona = PERSONA
        self.visual_hub_running = False

    def handle_user_input(self, user_input):
        # 1. Recall past memories (simplified search)
        context = self.memory.search_memory(user_input, limit=2)
        
        # 2. Logic to generate response (Placeholder for now)
        response = f"[{self.persona['name']}] Processing: {user_input}"
        
        # 3. Save to memory
        self.memory.save_interaction(user_input, response)
        
        return response

    def get_recent_history(self):
        return self.memory.get_recent_interactions()
