"""
Memory Node
-----------
Stores durable facts and short-term session context locally in SQLite.
No cloud sync. No admin mirroring. This runs on your machine only.
"""
import os
import sqlite3
import sys
import time
from pathlib import Path
from typing import Optional


def _get_data_dir() -> Path:
    """
    Where the memory database lives.

    In a packaged .exe, `__file__` resolves inside a temp extraction
    folder that isn't a stable place to store real data — it's wiped
    between runs for a onefile build. A packaged desktop app needs a
    real per-user data folder instead, same as any other Windows
    installed application uses.
    """
    if getattr(sys, "frozen", False):
        base = Path(os.environ.get("APPDATA") or os.path.expanduser("~"))
        data_dir = base / "SK_AI_4.0"
    else:
        data_dir = Path(__file__).parent
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


DB_PATH = _get_data_dir() / "memory.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS session_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    """)
    return conn


def remember(key: str, value: str) -> None:
    conn = _connect()
    conn.execute(
        "INSERT INTO facts (key, value, created_at) VALUES (?, ?, ?)",
        (key, value, time.time()),
    )
    conn.commit()
    conn.close()


def recall(key: str) -> Optional[str]:
    conn = _connect()
    row = conn.execute(
        "SELECT value FROM facts WHERE key = ? ORDER BY created_at DESC LIMIT 1",
        (key,),
    ).fetchone()
    conn.close()
    return row[0] if row else None


def log_turn(role: str, content: str) -> None:
    conn = _connect()
    conn.execute(
        "INSERT INTO session_log (role, content, created_at) VALUES (?, ?, ?)",
        (role, content, time.time()),
    )
    conn.commit()
    conn.close()


def recent_turns(limit: int = 20) -> list[dict]:
    conn = _connect()
    rows = conn.execute(
        "SELECT role, content, created_at FROM session_log ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in reversed(rows)]
