# ⚡ SK AI 4.0 — SOVEREIGN COGNITIVE DESKTOP OPERATING SYSTEM
### (PROJECT JARVIS 4.0 | PLATFORM V5.0)

**Founder, Inventor & Sole Architect:** Sumeet Kumar  
**Organization:** SK Enterprises  
**Target Platform:** Windows 10 / 11 (64-bit)  
**License:** Sovereign Enterprise / MIT Open Core  

---

## 🚀 OVERVIEW

**SK AI 4.0** is a production-grade, local-first enterprise cognitive desktop application engineered for sovereign, high-performance artificial intelligence workflows on Windows. It combines a robust Python FastAPI backend, a reactive WebGL/Three.js Cyberpunk HUD, local SQLite relational persistence, real-time WebSocket telemetry, and seamless Windows standalone desktop packaging.

```
       +-------------------------------------------------------------+
       |             SK AI 4.0 Desktop Launcher (EXE)                |
       +-------------------------------------------------------------+
               |                                             |
               v                                             v
    +-----------------------+                    +-----------------------+
    |   Cyberpunk 3D HUD    | <--(WebSocket)---> |   FastAPI Backend     |
    |   Three.js Particle   | <---(HTTP REST)--->|   Pydantic & Services |
    |   2D Agent Town       |                    |   Anti-Extraction     |
    +-----------------------+                    +-----------------------+
                                                             |
                                                             v
                                                 +-----------------------+
                                                 |   SQLite Persistence  |
                                                 |   %APPDATA% Storage   |
                                                 +-----------------------+
```

---

## 🌟 CORE CAPABILITIES

- **🧠 Cognitive Multi-Persona Matrix**: Switch between JARVIS, Butler, Commander, Oracle, and 12 distinct persona souls.
- **🛡️ Anti-Extraction Cryptographic Shield**: Built-in defense against prompt injection, memory extraction, and reverse-engineering.
- **🤖 2D Multi-Agent Town**: Real-time multi-agent laboratory simulation with live telemetry stream.
- **🌌 1-Second Precision Vedic Kundali**: Instant lifelong astrological charts, ephemeris calculations, and Vedic remedies.
- **📚 Universal STEM & Education Matrix**: Automated curriculum-aligned assessments and first-principles physics/math derivations.
- **📊 Autonomous Data Analyst Suite**: Automated dataset profiling, missing value imputation, IQR outlier elimination, and BigQuery SQL generation.
- **☁️ Cloud DevOps & Zero-Trust Actuator**: Automated user provisioning and security policy enforcement for Google Workspace and Microsoft 365.
- **👑 Super Admin & Licensing Engine**: Cryptographic HMAC-SHA256 license token generation, client onboarding, and remote killswitch control.

---

## ⚡ QUICK START (DEVELOPMENT)

### Prerequisites
- Windows 10/11 (64-bit)
- Python 3.11+
- PowerShell 5.1+

### 1. One-Command Setup
```powershell
# Installs dependencies, sets up directories, and initializes SQLite database
.\scripts\setup.ps1
```

### 2. Launch in Development Mode
```powershell
# Option A: Python one-command launcher
python run_dev.py

# Option B: PowerShell dev script
.\scripts\dev.ps1
```

### 3. Run Automated Tests
```powershell
# Runs complete pytest suite (33 tests)
python -m pytest
```

---

## 📦 BUILD & WINDOWS PACKAGING

### Build Standalone Executable
```powershell
.\scripts\build.ps1
```
*Generates `dist\SK_AI_4.0\SK_AI_4.0.exe` (Self-contained standalone Windows executable requiring zero Python on client machines).*

### Generate Release ZIP & Hashes
```powershell
.\scripts\package.ps1
```
*Outputs `release\SK_AI_4.0_Portable_x64_v5.0.0.zip` and `release\SHA256SUMS.txt`.*

---

## 📖 COMPLETE DOCUMENTATION SITEMAP

| Document | Description |
|---|---|
| [`docs/PROJECT_AUDIT.md`](docs/PROJECT_AUDIT.md) | Comprehensive Phase 0 audit & problem analysis |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Full system design & clean architecture specification |
| [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) | Detailed developer guide, setup & conventions |
| [`docs/API.md`](docs/API.md) | Complete REST API & WebSocket documentation |
| [`docs/DATABASE.md`](docs/DATABASE.md) | Relational schema design & UAC storage paths |
| [`docs/SECURITY.md`](docs/SECURITY.md) | Threat model, anti-extraction shield & controls |
| [`docs/BUILD.md`](docs/BUILD.md) | PyInstaller and Inno Setup build instructions |
| [`docs/WINDOWS_INSTALLATION.md`](docs/WINDOWS_INSTALLATION.md) | End-user installation & uninstallation guide |
| [`docs/CODE_SIGNING.md`](docs/CODE_SIGNING.md) | Microsoft Signtool & certificate procedures |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Recovery from port conflicts & database locks |
| [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md) | Pre-flight production verification checklist |
| [`release/RELEASE_NOTES.md`](release/RELEASE_NOTES.md) | Release notes and SHA-256 asset checksums |

---

## 📜 LEGAL & COMPLIANCE

- [`LICENSE`](LICENSE) — MIT License
- [`EULA.md`](EULA.md) — End User License Agreement
- [`PRIVACY_POLICY.md`](PRIVACY_POLICY.md) — Privacy Policy
- [`TERMS_OF_USE.md`](TERMS_OF_USE.md) — Terms of Use
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — Open-Source Software Notices

---

**Engineered with pride by Sumeet Kumar | SK Enterprises © 2026**
