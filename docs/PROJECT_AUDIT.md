# PROJECT AUDIT — SK AI 4.0 (Project JARVIS 4.0)

**Audit Date:** 2026-08-19  
**Auditor:** Antigravity Principal Engineering System  
**Phase:** PHASE 0  
**Git Commit Inspected:** `1e64b89`  
**Python Runtime Found:** 3.11.9

---

## 1. EXISTING PROJECT OVERVIEW

### Product Description
**SK AI 4.0** (codename: Project JARVIS 4.0 / Jarvis Platform V5.0) is a Windows desktop AI platform by **Sumeet Kumar / SK Enterprises** with cognitive modules including: 2D Agent Town, Vedic Astrology/Kundali Engine, Universal STEM & Education Matrix, Autonomous Data Analyst & SQL Studio, Cloud DevOps Actuator, Super Admin licensing, bilingual Hindi/English voice interface, and a 3D WebGL HUD.

---

## 2. DIRECTORY STRUCTURE

```
d:\Project SK AI 4.0\
├── Main_SK_AI_4.py              # Entry A: GUI + headless launcher
├── run_sk_ai_4.py               # Entry B: browser-based launcher (PRIMARY)
├── run_sk_ai.py                 # Entry C: legacy/alternate
├── app_entry.py                 # Entry D: lightweight
├── run_jarvis.py                # Entry E: another duplicate
├── config.py                    # Global config (uses dotenv — NOT in requirements)
├── SK_AI_4.0.spec               # PyInstaller spec (HARDCODED absolute path bug)
├── installer_setup_sk4.iss      # Inno Setup (ships .py source, not EXE — BROKEN)
├── requirements.txt             # Only 2 packages (fastapi + uvicorn) — INCOMPLETE
├── .env                         # Stub only
│
├── src_backend/                 # FastAPI backend
│   ├── main_engine.py           # PRIMARY active API server (468 lines)
│   ├── engine.py                # DUPLICATE API server — diverged endpoints
│   ├── anti_extraction_security.py
│   ├── astrology_matrix.py
│   ├── central_data_lake.py
│   ├── cloud_admin_engine.py    # DUPLICATE of core/cloud_admin_engine.py
│   ├── data_analyst_engine.py   # DUPLICATE of core/data_analyst_engine.py
│   ├── education_matrix.py      # DUPLICATE of core/education_matrix.py
│   ├── installer_wizard_app.py
│   ├── key_generator_master.py
│   ├── license_generator.py
│   ├── marvel_personas.py
│   ├── super_admin.py           # TWO super admin implementations
│   ├── super_admin_hub.py
│   └── user_deployment_engine.py
│
├── core/                        # Tkinter GUI + cognitive engines
│   ├── gui_dashboard.py         # Tkinter HUD (381 lines)
│   ├── coral_brain_logic.py     # In-memory brain schema
│   ├── system_paths.py          # Windows APPDATA path management (GOOD)
│   └── [8 other engine modules]
│
├── src_frontend/
│   ├── index.html               # 712-line HTML monolith (Three.js + Tailwind CDN)
│   └── super_admin.html
│
├── config/
│   ├── admin_credentials.json   # ⚠️ CRITICAL: Plaintext credentials in repo
│   ├── admin_credentials.txt    # ⚠️ CRITICAL: Plaintext credentials in repo
│   ├── admin_key.json           # ⚠️ CRITICAL: Key material in repo
│   ├── license.key              # ⚠️ CRITICAL: License secret in repo
│   └── system_identity.json
│
├── tests/                       # 17 tests (all passing)
├── docs/                        # EMPTY before this audit
├── scripts/                     # EMPTY — no build scripts
└── [20+ giant build scripts at root — 20-83KB each, legacy]
```

---

## 3. TECHNOLOGIES

| Layer | Technology | Version | Status |
|---|---|---|---|
| Language | Python | 3.11.9 | ✅ (target ≥ 3.12) |
| Backend | FastAPI | 0.115.5 | ✅ |
| ASGI | Uvicorn | 0.32.1 | ✅ |
| Validation | Pydantic | 2.10.3 | ✅ |
| ORM | SQLAlchemy | 2.0.36 | ✅ Installed, UNUSED |
| Migrations | Alembic | 1.14.0 | ✅ Installed, UNUSED |
| HTTP Client | httpx | 0.28.1 | ✅ Installed, UNUSED |
| Testing | pytest 8.3.4 | - | ✅ 17/17 passing |
| Packaging | PyInstaller | 6.22.1 | ✅ Installed |
| Desktop GUI | Tkinter | stdlib | ✅ |
| Frontend | Vanilla HTML/JS | - | ⚠️ Monolith |
| 3D Graphics | Three.js r128 | CDN | ⚠️ CDN dependency |
| CSS | Tailwind CSS | CDN | ⚠️ CDN dependency |
| Installer | Inno Setup | .iss file | ❌ Broken (ships source) |
| Database | None | - | ❌ Not implemented |

---

## 4. PROBLEMS IDENTIFIED

### P001 — CRITICAL SECURITY: Admin Credentials in Git
- **Files:** `config/admin_credentials.json`, `config/admin_credentials.txt`, `config/admin_key.json`, `config/license.key`
- **Finding:** Admin username `sumeet.admin@skenterprises.ai` and PIN `SK-SUMIT-2026-ROOT` committed to repository history
- **Impact:** Anyone with repo access has full admin credentials
- **Priority:** P0 — Fix BEFORE next commit

### P002 — CRITICAL: Installer Requires Python on End-User Machine
- **File:** `installer_setup_sk4.iss`
- **Finding:** Shortcuts call `python.exe run_sk_ai_4.py`. End users must manually install Python + dependencies.
- **Impact:** Product cannot be distributed as a standalone Windows app
- **Priority:** P0

### P003 — HIGH: PyInstaller Spec Has Hardcoded Absolute Path
- **File:** `SK_AI_4.0.spec` line 5: `['D:/Project SK AI 4.0/run_sk_ai.py']`
- **Impact:** Build fails on any machine where project is not at that exact path
- **Priority:** P1

### P004 — HIGH: Two Duplicate FastAPI Backend Servers
- **Files:** `src_backend/engine.py` (121L) and `src_backend/main_engine.py` (468L)
- **Impact:** Overlapping but different APIs. Maintenance confusion. One will diverge.
- **Priority:** P1

### P005 — HIGH: `requirements.txt` Critically Incomplete
- **Current content:** Only `fastapi` and `uvicorn[standard]`
- **Missing:** `python-dotenv`, `pydantic`, `httpx`, `sqlalchemy`, `alembic`, `pytest`, `pytest-asyncio`, `pytest-cov`
- **Impact:** Fresh install fails
- **Priority:** P1

### P006 — HIGH: No Database Layer
- **Impact:** SQLAlchemy+Alembic installed but zero models/migrations. All data (users, sessions, memory, settings) is in-memory and lost on restart. "Data Lake" feature is fabricated.
- **Priority:** P1

### P007 — HIGH: CORS Open to All Origins
- **Code:** `allow_origins=["*"]` in both backend files
- **Impact:** High risk when application is running; any webpage can call the API
- **Priority:** P1

### P008 — HIGH: Business Logic Embedded in Route Handlers
- **Impact:** Keyword-matching chat logic, SQL generation, all inline in route functions. Untestable, unmaintainable.
- **Priority:** P1

### P009 — MEDIUM: `config.py` Has Wrong Owner Name
- **Code:** `OWNER = "Inventor Sumeet Kumar"` (should be Sumeet Kumar)
- **Priority:** P2

### P010 — MEDIUM: Frontend is 712-Line HTML Monolith with CDN Dependencies
- **Impact:** Requires internet at launch. No modular JS. All `fetch()` calls scattered inline. Difficult to maintain or extend.
- **Priority:** P2

### P011 — MEDIUM: No Standard Health Endpoints
- **Impact:** No `/api/v1/health`, `/health/ready`, `/health/live`
- **Priority:** P2

### P012 — MEDIUM: No Structured Logging
- **Impact:** No operational log output. Crash log only. No log rotation.
- **Priority:** P2

### P013 — MEDIUM: No API Versioning (`/api/v1/` prefix)
- **Impact:** No version prefix on any routes. Breaking changes will break clients.
- **Priority:** P2

### P014 — MEDIUM: `python-dotenv` Used but Not in requirements.txt
- **Impact:** `ImportError` on fresh environment
- **Priority:** P1 (severity upgraded due to startup failure)

### P015 — MEDIUM: 20+ Large Legacy Build Scripts at Project Root
- **Files:** `build_sk_ai_v5_master_sovereign.py` (55KB), `deploy_super_admin_master.py` (83KB), etc.
- **Impact:** Confusing project structure. Active build path unclear.
- **Priority:** P2

### P016 — MEDIUM: Duplicate Module Implementations (core/ vs src_backend/)
- **Examples:** `cloud_admin_engine.py`, `data_analyst_engine.py`, `education_matrix.py` exist in both directories
- **Priority:** P2

### P017 — MEDIUM: `.gitignore` Excludes `*.spec` Files
- **Impact:** PyInstaller spec not tracked, breaking reproducible builds
- **Priority:** P2

### P018 — LOW: Multiple Conflicting Entry Points (5 launcher files)
- **Priority:** P3

### P019 — LOW: `pytest-asyncio` Deprecation Warning
- **Priority:** P3

### P020 — LOW: WebSocket Telemetry Streams Hardcoded Fabricated Data
- **Priority:** P3

### P021 — INFORMATIONAL: Chat Uses Keyword Matching, Not LLM
- **Status:** Known design decision. Must be documented as current limitation.

---

## 5. RECOMMENDATIONS

| ID | Problem | Recommended Solution | Priority |
|---|---|---|---|
| R001 | P001: Credentials in git | Remove from tracking, add to .gitignore, rotate credentials | P0 |
| R002 | P002: Installer broken | PyInstaller → self-contained EXE → Inno Setup ships dist/ binary | P0 |
| R003 | P003: Hardcoded spec path | Use relative path in spec | P1 |
| R004 | P004: Duplicate backends | Consolidate to `src_backend/main_engine.py`, archive `engine.py` | P1 |
| R005 | P005: requirements.txt | Regenerate complete requirements from active venv | P1 |
| R006 | P006: No database | Implement SQLite + SQLAlchemy + Alembic migrations | P1 |
| R007 | P007: Open CORS | Restrict to `http://127.0.0.1` family | P1 |
| R008 | P008: Logic in routes | Extract service layer under `src_backend/app/services/` | P1 |
| R009 | P009: Wrong owner | Fix `config.py` OWNER field | P2 |
| R010 | P010: Monolith frontend | Bundle deps locally; add JS module structure; add API client | P2 |
| R011 | P011: No health endpoints | Add `/api/v1/health`, `/api/v1/health/ready`, `/api/v1/health/live` | P2 |
| R012 | P012: No logging | Add structured logging to APPDATA logs with rotation | P2 |
| R013 | P013: No versioning | Add `/api/v1/` prefix via FastAPI APIRouter | P2 |
| R014 | P014: dotenv missing | Add `python-dotenv` to requirements.txt | P1 |
| R015 | P015: Root clutter | Move legacy scripts to `archive/` folder | P2 |
| R016 | P016: Duplicate modules | Canonicalize to `src_backend/`, remove `core/` duplicates | P2 |
| R017 | P017: .gitignore spec | Remove `*.spec` exclusion, track fixed spec | P2 |

---

## 6. GATE 0 ASSESSMENT

| Criterion | Status | Notes |
|---|---|---|
| Repository fully inspected | ✅ PASS | All directories and key files reviewed |
| Primary entry points identified | ✅ PASS | `run_sk_ai_4.py` (browser) + `Main_SK_AI_4.py` (GUI/headless) |
| Build process identified | ✅ PASS | PyInstaller + Inno Setup (both currently broken/incomplete) |
| Run process identified | ✅ PASS | `python run_sk_ai_4.py` starts backend + opens browser frontend |
| Test process identified | ✅ PASS | `python -m pytest tests/` — 17/17 passing |
| Major technical risks identified | ✅ PASS | 21 issues catalogued; P0 credential exposure and installer breakage documented |

> **GATE 0: ✅ PASS** — Proceeding to Phase 1 Architecture.

---

*Generated by Antigravity Engineering System | Phase 0 Audit*  
*Project: SK AI 4.0 | Inventor: Sumeet Kumar | SK Enterprises | 2026-08-19*
