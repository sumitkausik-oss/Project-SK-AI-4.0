"""
SK Enterprises | Production Build & Inno Setup Packaging Script
Inventor & Sole Architect: Sumeet Kumar
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DIST_DIR = ROOT_DIR / "dist" / "SK_AI_4.0"
OUTPUT_INSTALLER_DIR = ROOT_DIR / "Output_Installer"
ISCC_PATH = Path(r"C:\Users\cpspu\AppData\Local\Programs\Inno Setup 6\ISCC.exe")

def clean_build_artifacts():
    print("[1/4] Cleaning previous build artifacts...")
    for folder in [ROOT_DIR / "build", ROOT_DIR / "dist", OUTPUT_INSTALLER_DIR]:
        if folder.exists():
            shutil.rmtree(folder, ignore_errors=True)
    OUTPUT_INSTALLER_DIR.mkdir(parents=True, exist_ok=True)
    print(" -> Cleaned build and dist directories.")

def compile_pyinstaller():
    print("\n[2/4] Compiling Standalone Executable via PyInstaller...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=SK_AI_4.0",
        "--windowed",
        "--noconsole",
        f"--icon={ROOT_DIR / 'assets' / 'jarvis.ico'}",
        f"--add-data={ROOT_DIR / 'assets'};assets",
        f"--add-data={ROOT_DIR / 'config'};config",
        f"--add-data={ROOT_DIR / 'plugins'};plugins",
        f"--add-data={ROOT_DIR / 'core'};core",
        "--collect-all=tkinter",
        "--collect-all=PIL",
        "--clean",
        "--noconfirm",
        str(ROOT_DIR / "Main_SK_AI_4.py")
    ]
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=ROOT_DIR)
    if res.returncode != 0:
        raise RuntimeError(f"PyInstaller compilation failed with return code {res.returncode}")
    
    # In PyInstaller --onedir with --name=SK_AI_4.0, the executable is SK_AI_4.0.exe.
    # Let's ensure Main_SK_AI_4.exe exists or rename SK_AI_4.0.exe -> Main_SK_AI_4.exe
    exe_path = DIST_DIR / "SK_AI_4.0.exe"
    target_exe = DIST_DIR / "Main_SK_AI_4.exe"
    if exe_path.exists() and not target_exe.exists():
        shutil.copy2(exe_path, target_exe)
    print(" -> PyInstaller compiled successfully in dist/SK_AI_4.0/.")

def copy_runtime_assets():
    print("\n[3/4] Bundling dynamic configurations and assets...")
    shutil.copytree(ROOT_DIR / "assets", DIST_DIR / "assets", dirs_exist_ok=True)
    shutil.copytree(ROOT_DIR / "config", DIST_DIR / "config", dirs_exist_ok=True)
    shutil.copytree(ROOT_DIR / "plugins", DIST_DIR / "plugins", dirs_exist_ok=True)
    print(" -> Assets, configs and plugins mirrored to dist/SK_AI_4.0/.")

def compile_inno_setup():
    print("\n[4/4] Compiling Windows Inno Setup Installer (x64)...")
    if not ISCC_PATH.exists():
        raise FileNotFoundError(f"Inno Setup compiler not found at {ISCC_PATH}")
    
    iss_file = ROOT_DIR / "installer_setup_sk4.iss"
    cmd = [str(ISCC_PATH), str(iss_file)]
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=ROOT_DIR)
    if res.returncode != 0:
        raise RuntimeError(f"Inno Setup compilation failed with code {res.returncode}")
    
    installer_exe = OUTPUT_INSTALLER_DIR / "SK_AI_4.0_Setup_x64.exe"
    if installer_exe.exists():
        size_mb = installer_exe.stat().st_size / (1024 * 1024)
        print(f"\n[SUCCESS] Production Installer Created: {installer_exe.name} ({size_mb:.2f} MB)")
        print(f"Path: {installer_exe}")
    else:
        print("[WARNING] Installer executable not found in Output_Installer.")

if __name__ == "__main__":
    try:
        clean_build_artifacts()
        compile_pyinstaller()
        copy_runtime_assets()
        compile_inno_setup()
        print("\n" + "=" * 80)
        print("  SK AI 4.0 PRODUCTION BUILD & PACKAGING COMPLETE!")
        print("  Inventor & Sole Architect: Sumeet Kumar | SK Enterprises")
        print("=" * 80)
    except Exception as e:
        print(f"\n[BUILD ERROR]: {e}", file=sys.stderr)
        sys.exit(1)
