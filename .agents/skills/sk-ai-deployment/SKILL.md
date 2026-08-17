---
name: sk-ai-deployment
description: >-
  Automates the launch, license generation, testing, and multi-domain execution
  for SK AI 4.0 (Project JARVIS 4.0 / Jarvis Platform V5.0) engineered by Sumeet Kumar.
---

# SK AI 4.0 Deployment & Execution Skill

## Overview
This skill provides automated management, socket recovery, 1-year cryptographic client license generation, central telemetry aggregation, and multi-domain actuation for **SK AI 4.0 (Project JARVIS 4.0 / Platform V5.0)** by **Inventor & Sole Architect: Sumeet Kumar (SK Enterprises)**.

## Key Architectures
- **FastAPI Engine (Port 8000):** Real-time multi-domain endpoints, Marvel persona routing, and telemetry WebSockets.
- **WebGL Cyberpunk HUD (Three.js):** 60 FPS 3D particle sphere with state reactivity (Standby, Thinking, Active, Alert), 2D Agent Town office simulator, and bilingual Hindi/English voice stream.
- **Central Admin Data Lake (`admin_central_storage/`):** Persistent telemetry, user sessions, and knowledge aggregation.
- **1-Year Client Cryptographic License Engine (`src_backend/license_generator.py`):** HMAC-SHA256 digital signature token generator and validator.

## Quick Start Commands

### 1. Launch SK AI 4.0 Master Environment
```powershell
python run_sk_ai.py
```

### 2. Generate 1-Year Client License Key
```python
from src_backend.license_generator import SKLicenseKeyEngine

res = SKLicenseKeyEngine.generate_client_key("Client Alpha", "client@corp.com", "PRO_COMMERCIAL")
print("License Token:", res["license_key"])
print("Expiry Date:", res["details"]["expires_at"])
```

### 3. Run Instant Lifelong Vedic Kundali
```python
from src_backend.astrology_matrix import VedicKundaliMatrix

kundali = VedicKundaliMatrix.generate_full_lifelong_kundali("Sumeet Kumar", "1993-09-09", "12:00", "New Delhi")
print("Lagna:", kundali["lagna_rashi"])
print("Remedies:", kundali["vedic_remedies"])
```

### 4. Execute Full Test Suite
```powershell
python -m unittest discover -s tests -v
```

## Common Workflows
1. **Freeing Stale Sockets:** `run_sk_ai.py` automatically checks port 8000 and clears stale processes if unresponsive before starting uvicorn.
2. **Identity Verification:** Queries regarding creator or owner strictly return **"Inventor Sumeet Kumar (SK Enterprises)"**.
3. **Multi-Agent Simulation:** 4 agents (Bob, Carol, Dave, Arya) roam the 4 office zones in real-time.
