# SK AI 4.0 — SYSTEM ARCHITECTURE SPECIFICATION
### (PROJECT JARVIS 4.0 | PLATFORM V5.0)

**Founder & Sole Architect:** Sumeet Kumar  
**Organization:** SK Enterprises  
**Target Desktop Platform:** Windows 10 / 11 (64-bit)  
**Desktop Runtime:** Electron  
**Windows Packaging:** Electron Builder (NSIS x64 Target)  

---

## 1. Six-Layer Cognitive System Architecture

```text
+=============================================================================+
|                       LAYER 6: GOVERNANCE & RELEASE                         |
|  Electron Desktop Shell | Electron Builder NSIS Installer | Audit Logs     |
+=============================================================================+
                                      |
                                      v
+=============================================================================+
|                      LAYER 5: CYBER HUD & VISUALIZATION                     |
|  Three.js 3D Sphere | 2D Agent Town Canvas | Agent Office | Super Admin Hub |
+=============================================================================+
                                      |
                                      v
+=============================================================================+
|                 LAYER 4: MULTI-DOMAIN COGNITIVE MATRIX                      |
|  STEM Matrix | Vedic Astrology | Data Analytics | Cloud DevOps | Media      |
+=============================================================================+
                                      |
                                      v
+=============================================================================+
|                    LAYER 3: CONTINUOUS EVOLUTION ENGINE                     |
|  Research Scheduler | Knowledge Indexer | Capability Sandbox | Change Eval  |
+=============================================================================+
                                      |
                                      v
+=============================================================================+
|                       LAYER 2: FOUR-NODE BRAIN                              |
|  [MEMORY Node]     [SKILLS Node]      [SOUL Node]       [SETTINGS Node]     |
+=============================================================================+
                                      |
                                      v
+=============================================================================+
|                  LAYER 1: HYBRID INTELLIGENCE GATEWAY                       |
|  FastAPI REST API | WebSocket Telemetry | Anti-Extraction | SQLite Storage  |
+=============================================================================+
```

---

## 2. Electron Desktop Runtime Architecture

```text
+-----------------------------------------------------------------------------+
|                          ELECTRON MAIN PROCESS                              |
|  - Window Manager (1440x900, frameless/acrylic dark HUD)                    |
|  - Backend Process Manager (spawns FastAPI backend & monitors health)       |
|  - Single Instance Lock (prevents duplicate processes)                      |
|  - Graceful Shutdown Manager (terminates backend on window close)           |
+-----------------------------------------------------------------------------+
               |                                             |
     (Preload IPC Bridge)                         (Process Supervision)
               |                                             |
               v                                             v
+-----------------------------+               +-----------------------------+
|      RENDERER PROCESS       |               |       FASTAPI BACKEND       |
|  - Context Isolation: true  |               |  - Host: 127.0.0.1:8000     |
|  - Node Integration: false  | <--(WS/REST)->|  - 5-Layer Intel Graph      |
|  - Typed window.electronAPI |               |  - Agent Registry (8 Agents)|
|  - Cyberpunk HUD Frontend   |               |  - SQLite Persistence       |
+-----------------------------+               +-----------------------------+
```

---

## 3. Four-Node Brain Specification

1. **MEMORY Node:**
   - Short-term context & session cache
   - Long-term associative memories in SQLite (`memory_records` table)
   - Privacy-scoped memory search and deletion APIs
2. **SKILLS Node:**
   - Controlled tool executions with explicit risk levels (`SAFE`, `LOW`, `MEDIUM`, `HIGH`)
   - Anti-extraction prompt shield prevents arbitrary code injection
3. **SOUL Node:**
   - 12 active cognitive personas (`JARVIS`, `FRIDAY`, `VERONICA`, `ULTRON`, `VISION`, `STRANGE`, etc.)
   - Real-time execution tracing (Intent → Agent → Tools → Status → Output)
4. **SETTINGS Node:**
   - Persistent configuration for AI providers, UI themes, audio, security, and diagnostics

---

## 4. Electron-Builder Windows Installer Specification

- **Target:** NSIS (`win.target: [{ target: "nsis", arch: ["x64"] }]`)
- **Product Name:** `SK AI 4.0`
- **Output Artifact:** `release/SK_AI_4.0_Setup_x64_v5.0.0.exe`
- **Capabilities:**
  - Standard user and per-machine installation
  - Desktop shortcut and Start Menu program group creation
  - Clean Windows uninstallation with complete registry and file cleanup
  - Bundled standalone dependencies
