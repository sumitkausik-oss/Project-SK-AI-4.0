from core.orchestrator import Orchestrator
from core.persona_manager import PersonaManager
from core.skill_manager import SkillManager
import sys

def main():
    print("Initializing SK AI 4.0 Core...")
    sk_orchestrator = Orchestrator()
    sk_persona = PersonaManager()
    sk_skills = SkillManager()
    
    # Simple console loop for final verification before build
    # In production, this would bridge to Visual Hub/Voice I/O
    print(f"{sk_persona.persona_data['name']} is Online.")
    
    # To prevent actual execution hang during build, we exit main early.
    print("Core build complete. Exiting startup sequence.")
    sys.exit(0)

if __name__ == "__main__":
    main()
