"""
Soul Node
---------
Selects a response tone/style profile. This is a configuration switch,
not a separate "consciousness" — worth naming plainly since the modes
below map directly to the personas from the original spec.
"""

PERSONAS = {
    "tactical": {
        "label": "Tactical / concise",
        "tone": "Direct, minimal, prioritizes speed over explanation.",
    },
    "workflow": {
        "label": "Workflow / execution",
        "tone": "Task-focused, checklist-driven, high throughput.",
    },
    "analytical": {
        "label": "Analytical / research",
        "tone": "Thorough, cites reasoning, flags uncertainty.",
    },
    "advisory": {
        "label": "Advisory / domain expert",
        "tone": "Explains tradeoffs, gives recommendations with caveats.",
    },
}

DEFAULT_PERSONA = "workflow"


def get_persona(name: str | None = None) -> dict:
    return PERSONAS.get(name or DEFAULT_PERSONA, PERSONAS[DEFAULT_PERSONA])


def list_personas() -> dict:
    return PERSONAS
