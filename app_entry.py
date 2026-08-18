"""
Entry point for the packaged (.exe) build.

PyInstaller needs a plain Python entry point that starts the server
programmatically — the `python -m uvicorn ...` CLI form used for
development doesn't get bundled correctly. This is that entry point.
"""
import webbrowser
import threading
import time

import uvicorn

from main import app
from settings import config


def _open_browser_when_ready():
    time.sleep(1.5)
    webbrowser.open(f"http://{config.HOST}:{config.PORT}/docs")


if __name__ == "__main__":
    threading.Thread(target=_open_browser_when_ready, daemon=True).start()
    print(f"Starting {config.APP_NAME} on http://{config.HOST}:{config.PORT}")
    print("Close this window to stop the server.")
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="info")
