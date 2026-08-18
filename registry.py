"""
Skills Node
-----------
A registry of callable functions the system can invoke. Each skill is
explicit, reviewed code you write and register here — not arbitrary
sandboxed code execution or auto-installed packages. That boundary is
intentional: it's what keeps this debuggable and safe to run.
"""
from typing import Callable

_REGISTRY: dict[str, Callable] = {}


def register(name: str):
    def decorator(fn: Callable):
        _REGISTRY[name] = fn
        return fn
    return decorator


def list_skills() -> list[str]:
    return sorted(_REGISTRY.keys())


def run_skill(name: str, **kwargs):
    if name not in _REGISTRY:
        raise KeyError(f"No skill registered as '{name}'. Available: {list_skills()}")
    return _REGISTRY[name](**kwargs)


# --- Starter skills ---

@register("echo")
def echo_skill(text: str) -> str:
    return text


@register("word_count")
def word_count_skill(text: str) -> int:
    return len(text.split())
