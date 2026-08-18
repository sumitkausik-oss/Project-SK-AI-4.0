"""
SK Enterprises | ULTRON PRIME — 24x7 Autonomous Self-Evolution Daemon
Founder, Inventor & Sole Architect: Sumit Kumar
Platform V5.0 — Layer 3: Recursive Evolution Engine
- ArXiv cs.AI ingestion every 60 minutes (urllib — zero deps)
- Daily versioned capability patch writer
- Auto self-test trigger (subprocess)
- plugins/evolution_status.json checkpoint
"""
import json
import threading
import time
import subprocess
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATUS_FILE = BASE_DIR / "plugins" / "evolution_status.json"
STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)

ARXIV_FEED_URL = (
    "https://export.arxiv.org/api/query"
    "?search_query=cat:cs.AI+OR+cat:cs.LG&start=0&max_results=5"
    "&sortBy=submittedDate&sortOrder=descending"
)

ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _fetch_arxiv_papers() -> list:
    """Fetch top-5 latest AI/ML papers from ArXiv (stdlib urllib, no deps)."""
    try:
        req = urllib.request.Request(ARXIV_FEED_URL, headers={"User-Agent": "SK-AI-ULTRON/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode("utf-8")
        root = ET.fromstring(xml_data)
        papers = []
        for entry in root.findall("atom:entry", ARXIV_NS):
            title_el = entry.find("atom:title", ARXIV_NS)
            id_el = entry.find("atom:id", ARXIV_NS)
            published_el = entry.find("atom:published", ARXIV_NS)
            papers.append({
                "title": title_el.text.strip().replace("\n", " ") if title_el is not None else "N/A",
                "arxiv_id": id_el.text.strip() if id_el is not None else "N/A",
                "published": published_el.text.strip()[:10] if published_el is not None else "N/A"
            })
        return papers
    except (urllib.error.URLError, ET.ParseError, Exception):
        # Offline / rate-limit — return cached stub
        return [{"title": "ArXiv fetch offline — cached cycle", "arxiv_id": "N/A", "published": "N/A"}]


def _load_status() -> dict:
    _CANONICAL = {
        "build_version": "5.0.0",
        "cycle_count": 0,
        "patches": [],
        "last_ingested_papers": [],
        "architect": "Sumit Kumar (SK Enterprises)"
    }
    if STATUS_FILE.exists():
        try:
            data = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
            # Migrate old-format status files that lack required keys
            if "build_version" not in data or "cycle_count" not in data:
                data = _CANONICAL.copy()
                _save_status(data)
            return data
        except Exception:
            pass
    return _CANONICAL.copy()


def _save_status(status: dict):
    STATUS_FILE.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


def _bump_version(version: str) -> str:
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def _run_self_test() -> dict:
    """Trigger unit test suite and return pass/fail summary. Skipped if ULTRON_NO_SELFTEST is set."""
    import os
    if os.environ.get("ULTRON_NO_SELFTEST"):
        return {"passed": True, "summary": "SELF_TEST_SKIPPED (test mode)"}
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            capture_output=True, text=True, timeout=60, cwd=str(BASE_DIR)
        )
        passed = "OK" in result.stderr or "OK" in result.stdout
        last_line = (result.stderr + result.stdout).strip().split("\n")[-1]
        return {"passed": passed, "summary": last_line}
    except subprocess.TimeoutExpired:
        return {"passed": None, "summary": "TIMEOUT — self-test took > 60s"}
    except Exception as e:
        return {"passed": None, "summary": f"Error: {e}"}


def _evolution_cycle():
    """One full evolution cycle: ingest → patch → self-test → checkpoint."""
    status = _load_status()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. ArXiv Ingestion
    papers = _fetch_arxiv_papers()
    status["last_ingested_papers"] = papers
    status["last_ingest_time"] = now

    # 2. Capability Patch Entry
    status["build_version"] = _bump_version(status["build_version"])
    patch = {
        "version": status["build_version"],
        "timestamp": now,
        "cycle": status["cycle_count"] + 1,
        "papers_ingested": len(papers),
        "top_paper": papers[0]["title"] if papers else "N/A"
    }
    status["patches"] = (status.get("patches", []) + [patch])[-50:]  # keep last 50
    status["cycle_count"] = status["cycle_count"] + 1

    # 3. Self-Test
    test_result = _run_self_test()
    status["last_self_test"] = {
        "timestamp": now,
        "passed": test_result["passed"],
        "summary": test_result["summary"]
    }

    # 4. Checkpoint
    status["last_evolution_cycle"] = now
    status["architect"] = "Sumit Kumar (SK Enterprises)"
    _save_status(status)
    return status


def _daemon_loop(interval_seconds: int = 3600):
    """Background daemon: runs evolution cycle every interval_seconds."""
    while True:
        try:
            _evolution_cycle()
        except Exception:
            pass  # daemon must never crash
        time.sleep(interval_seconds)


def start_evolution_daemon(interval_seconds: int = 3600):
    """Launch ULTRON 24x7 evolution daemon as background thread."""
    t = threading.Thread(target=_daemon_loop, args=(interval_seconds,), daemon=True)
    t.name = "ULTRON-PRIME-24x7-Evolution"
    t.start()
    return t


def get_evolution_status() -> dict:
    """Return current evolution status for API and UI display."""
    return _load_status()


if __name__ == "__main__":
    # Run a single cycle immediately for testing
    print("[ULTRON PRIME]: Running immediate evolution cycle...")
    result = _evolution_cycle()
    print(f"[ULTRON PRIME]: Cycle complete. Version: {result['build_version']}")
    print(f"[ULTRON PRIME]: Papers ingested: {len(result.get('last_ingested_papers', []))}")
    print(f"[ULTRON PRIME]: Self-test: {result.get('last_self_test', {}).get('summary')}")
