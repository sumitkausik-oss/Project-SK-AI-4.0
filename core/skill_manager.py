from typing import Dict, Any

class SkillManager:
    def __init__(self):
        self.skills = {}

    def register_skill(self, name: str, skill_func: callable):
        self.skills[name] = skill_func

    def execute_skill(self, name: str, *args, **kwargs) -> Any:
        if name in self.skills:
            return self.skills[name](*args, **kwargs)
        return f"Skill {name} not found."
