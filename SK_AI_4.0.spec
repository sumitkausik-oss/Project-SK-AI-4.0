# -*- mode: python ; coding: utf-8 -*-
# SK Enterprises | PyInstaller Build Specification
# Inventor & Sole Architect: Sumeet Kumar
# Platform: Jarvis Platform V5.0

import os
from pathlib import Path

ROOT_DIR = os.path.abspath(SPECPATH)

datas = [
    (os.path.join(ROOT_DIR, 'src_frontend'), 'src_frontend'),
    (os.path.join(ROOT_DIR, 'assets'), 'assets'),
    (os.path.join(ROOT_DIR, 'config'), 'config'),
    (os.path.join(ROOT_DIR, 'src_backend'), 'src_backend'),
    (os.path.join(ROOT_DIR, 'core'), 'core'),
]

hidden_imports = [
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespans',
    'uvicorn.lifespans.on',
    'fastapi',
    'pydantic',
    'pydantic_settings',
    'sqlalchemy',
    'sqlalchemy.dialects.sqlite',
    'sqlite3',
    'dotenv',
    'httpx',
    'engineio.async_drivers.asgi',
]

a = Analysis(
    ['run_sk_ai_4.py'],
    pathex=[ROOT_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'unittest.test'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SK_AI_4.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True so logs/status are visible on launcher
    icon=os.path.join(ROOT_DIR, 'assets', 'jarvis.ico'),
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SK_AI_4.0',
)
