"""
SK Enterprises | Fast Targeted Standardization to 'Sumeet Kumar'
Platform V5.0
"""
import os
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")

TARGET_DIRS = [
    ROOT_DIR / "src_backend",
    ROOT_DIR / "src_frontend",
    ROOT_DIR / "config",
    ROOT_DIR / "tests",
    ROOT_DIR / "cross_platform_builds",
    ROOT_DIR
]

REPLACEMENTS = [
    ("Sumeet Kumar", "Sumeet Kumar"),
    ("Sumeet Kumar", "Sumeet Kumar"),
    ("Sumeet Kumar", "Sumeet Kumar"),
    ("sumit.admin", "sumit.admin"),
    ("Sumit", "Sumit"),
    ("sumit", "sumit"),
    ("SUMIT", "SUMIT"),
]

def clean_file(p: Path):
    if p.suffix in {".py", ".json", ".html", ".js", ".css", ".txt", ".md", ".iss", ".spec", ".bat", ".svg"}:
        try:
            content = p.read_text(encoding="utf-8")
            new_content = content
            for old, new in REPLACEMENTS:
                new_content = new_content.replace(old, new)
            if new_content != content:
                p.write_text(new_content, encoding="utf-8")
                return True
        except Exception:
            pass
    return False

def standardize_fast():
    count = 0
    # Process root files
    for f in ROOT_DIR.iterdir():
        if f.is_file():
            if clean_file(f):
                count += 1
    # Process target directories
    for d in TARGET_DIRS:
        if d != ROOT_DIR and d.exists():
            for root, _, files in os.walk(d):
                for file in files:
                    if clean_file(Path(root) / file):
                        count += 1
    print(f"Fast standardization complete: updated {count} files to 'Sumeet Kumar'.")

if __name__ == "__main__":
    standardize_fast()
