"""
SK Enterprises | SK AI 4.0 Local Development Launcher
Founder & Sole Architect: Sumeet Kumar
Platform: Jarvis Platform V5.0
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.launcher import launch_desktop

if __name__ == "__main__":
    launch_desktop()
