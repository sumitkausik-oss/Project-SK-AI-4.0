import os
import shutil
import subprocess
from pathlib import Path

cache_dir = Path(os.environ["LOCALAPPDATA"]) / "electron-builder" / "Cache" / "winCodeSign"
seven_za = Path(r"D:\Project SK AI 4.0\node_modules\7zip-bin\win\x64\7za.exe")

archives = list(cache_dir.glob("*.7z"))
if archives and seven_za.exists():
    archive = archives[0]
    target = cache_dir / "winCodeSign-2.6.0"
    target.mkdir(parents=True, exist_ok=True)
    cmd = [str(seven_za), "x", "-y", f"-o{target}", str(archive), "-xr!darwin"]
    subprocess.run(cmd, capture_output=True, text=True)
    
    # Also mirror contents into any hash directories
    for p in cache_dir.iterdir():
        if p.is_dir() and p.name != "winCodeSign-2.6.0":
            for item in target.iterdir():
                dest = p / item.name
                if not dest.exists():
                    if item.is_dir():
                        shutil.copytree(item, dest)
                    else:
                        shutil.copy2(item, dest)
    print("winCodeSign cache prepared successfully.")
