# DEVELOPER GUIDE — SK AI 4.0 (PROJECT JARVIS 4.0)

**Platform Version:** Jarvis Platform V5.0  
**Founder & Sole Architect:** Sumeet Kumar (SK Enterprises)  

---

## 1. PREREQUISITES

- **Operating System:** Windows 10 / 11 (64-bit)
- **Python:** 3.11 or 3.12+ (64-bit)
- **PowerShell:** 5.1 or PowerShell Core 7+
- **Browser:** Any modern Chromium or Gecko-based browser (Chrome, Edge, Brave, Firefox)

---

## 2. QUICK START (ONE-COMMAND SETUP)

Open PowerShell in the repository root directory and run:

```powershell
# Setup environment, dependencies and SQLite database
.\scripts\setup.ps1
```

To launch the live application in development mode:

```powershell
.\scripts\dev.ps1
```

This starts the FastAPI backend on `http://127.0.0.1:8000` and automatically opens the Cyberpunk 3D HUD in your default browser.

---

## 3. PROJECT DIRECTORY LAYOUT

```
Project SK AI 4.0/
├── src_backend/                 # Python FastAPI Backend
│   ├── app/                     # Modular Clean Architecture
│   │   ├── main.py              # Application factory & lifespan
│   │   ├── core/                # Settings & structured logging
│   │   ├── database/            # SQLAlchemy session & init
│   │   ├── models/              # Declarative database models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── repositories/        # Database access layer
│   │   ├── services/            # Business & cognitive domain services
│   │   ├── api/v1/              # Versioned API routes (/api/v1/...)
│   │   ├── websocket/           # Real-time telemetry stream manager
│   │   └── middleware/          # Request logging & exception handling
│   └── main_engine.py           # Legacy entrypoint (backward-compatible)
│
├── src_frontend/                # WebGL Cyberpunk 3D HUD
│   ├── index.html               # 3D holographic neural sphere & agent town
│   ├── super_admin.html         # Super Admin portal
│   └── js/
│       ├── api_client.js        # Centralized typed REST client
│       └── ws_manager.js        # WebSocket telemetry manager
│
├── core/                        # Core system utilities & path resolvers
│   └── system_paths.py          # Windows UAC-safe path resolution
│
├── scripts/                     # PowerShell automation scripts
│   ├── setup.ps1                # Automated dev environment bootstrap
│   ├── dev.ps1                  # Local development launcher
│   ├── test.ps1                 # Pytest test suite runner
│   ├── build.ps1                # PyInstaller standalone executable compiler
│   └── package.ps1              # Release packager & checksum generator
│
├── tests/                       # Automated test suites
├── docs/                        # Complete technical documentation
├── assets/                      # Icons, logos, and graphic assets
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Dev & test dependencies
├── SK_AI_4.0.spec               # PyInstaller build specification
└── installer_setup_sk4.iss      # Inno Setup Windows installer script
```

---

## 4. RUNNING TESTS

To run the complete automated test suite:

```powershell
.\scripts\test.ps1
```

For verbose output with code coverage metrics:

```powershell
.\scripts\test.ps1 -VerboseOutput -Coverage
```

---

## 5. CODE CONVENTIONS & QUALITY

- **Type Annotations**: All backend functions and methods must include Python type hints.
- **Pydantic Validation**: All API inputs and outputs must define explicit Pydantic schemas.
- **Database Safety**: Never execute raw SQL without ORM parameter binding.
- **Path Resolution**: Always use `system_paths.py` or `settings.DATABASE_PATH` for filesystem operations. Never hardcode absolute disk paths.
