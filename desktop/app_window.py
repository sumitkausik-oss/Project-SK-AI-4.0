"""
SK Enterprises | Native Desktop Window Shell Wrapper
Founder & Sole Architect: Sumeet Kumar
Platform: Jarvis Platform V5.0
"""
import os
import sys
import webbrowser
import subprocess
from pathlib import Path

def open_desktop_window(target_url: str, title: str = "SK AI 4.0 | Project JARVIS 4.0", width: int = 1440, height: int = 900):
    """
    Opens the desktop application shell.
    Tries:
    1. pywebview (Native Webview2 on Windows)
    2. Microsoft Edge / Chrome in --app mode (Frameless Desktop App Mode)
    3. Default system browser
    """
    # 1. Try pywebview if installed
    try:
        import webview
        window = webview.create_window(
            title=title,
            url=target_url,
            width=width,
            height=height,
            resizable=True,
            fullscreen=False,
            min_size=(1024, 700),
            background_color='#030712'
        )
        webview.start(debug=False)
        return
    except Exception:
        pass

    # 2. Try Microsoft Edge / Chrome in frameless App Mode on Windows
    if sys.platform == "win32":
        edge_paths = [
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe")
        ]
        for p in edge_paths:
            if os.path.exists(p):
                try:
                    subprocess.Popen([p, f"--app={target_url}", f"--window-size={width},{height}"])
                    return
                except Exception:
                    pass

        chrome_paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
        ]
        for p in chrome_paths:
            if os.path.exists(p):
                try:
                    subprocess.Popen([p, f"--app={target_url}", f"--window-size={width},{height}"])
                    return
                except Exception:
                    pass

    # 3. Fallback to standard browser launch
    webbrowser.open(target_url)
