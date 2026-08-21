# ⚡ SKAI — Desktop AI Assistant
### SKAI — Powered by SK Enterprises

**Founder & Sole Architect:** Sumeet Kumar  
**Company:** SK Enterprises  
**Target Platform:** Windows 10 / 11 (64-bit), macOS, Linux  
**License:** MIT License  

---

## 🌟 Overview

**SKAI** is a **local-first desktop AI assistant** engineered by **Sumeet Kumar** under **SK Enterprises** that genuinely acts on your computer — not just chat. 

The core interaction model:
> **You speak or type a command → SKAI understands it → SKAI executes it on the operating system → SKAI reports back clearly what it did with structured before/after feedback and transparent safety confirmation.**

---

## 🚀 "Try SKAI in 2 minutes" (Interactive Demo Script)

Once SKAI is launched, try any of these immediate example commands (by typing into the command box or speaking via the 🎙️ mic button):

| # | Command to Speak / Type | What SKAI Does | Expected Structured Result |
|---|---|---|---|
| 1 | `open notepad` | Launches Windows Notepad application | Notepad opens on desktop; SKAI reports `🚀 Application Launched: Successfully opened notepad` |
| 2 | `take a screenshot` | Captures high-res display screen | Full-screen screenshot saved to `%APPDATA%\screenshots`; thumbnail preview displayed in chat & timeline |
| 3 | `create a file called test.txt on the desktop` | Creates a new text file on your Desktop | File created at `Desktop/test.txt`; SKAI returns path and confirmation |
| 4 | `remember that I prefer dark mode` | Stores a durable fact into local SQLite | Fact saved permanently; inspectable in the in-app **🧠 Memory Store** modal |
| 5 | `what do you remember about my preferences?` | Recalls saved facts associatively | Lists all remembered facts with keyword relevance |
| 6 | `search my documents for python` | Content-aware local file search | Ranked search results with file paths and matched line snippets |
| 7 | `run command echo "SKAI Online"` | Runs shell/PowerShell command | Terminal output and exit code streamed back in chat and audit timeline |
| 8 | `delete file test.txt` | Triggers Safety Confirmation Gate | ⚠️ **Safety Confirmation Modal** appears with Approve/Reject buttons before deleting |

---

## 🔒 Local Core vs. Optional Online Features

SKAI is strictly designed as a **local-first, privacy-respecting cognitive assistant**.

| Feature | Offline / Local | Cloud / Online (Optional) | Description |
|---|---|---|---|
| **Application Control** | ✅ 100% Local | — | Open and close installed applications |
| **File & Folder Management** | ✅ 100% Local | — | Create, read, write, move, rename, delete files |
| **Terminal & Shell Execution** | ✅ 100% Local | — | Execute PowerShell / CMD commands safely |
| **Intelligent File Search** | ✅ 100% Local | — | Content-aware keyword search across drives |
| **Screenshot Capture** | ✅ 100% Local | — | High-res display grab and base64 preview |
| **Local Memory Store** | ✅ 100% Local | — | SQLite persistent facts, preferences, and context |
| **Coding Assistant** | ✅ 100% Local | — | Scoped project file scanning and surgical editing |
| **Safety & Audit Trail** | ✅ 100% Local | — | Tamper-evident command and event logging |
| **Web Research Tools** | — | 🌐 Optional | Off-by-default add-on for web searches |

---

## 🛡️ Safety & Permission Gatekeeper

Because SKAI has real operating system control, it enforces a built-in safety gatekeeper:
- **READ_ONLY** (search, read file, list folder, screenshot): Auto-approved with zero friction.
- **REVERSIBLE_WRITE** (create file/folder, move file, open app): Auto-approved or light confirmation based on settings.
- **DESTRUCTIVE_HIGH_IMPACT** (delete file, close app, run terminal command, overwrite): Explicit interactive user confirmation modal required before execution.

---

## ⚡ Quick Start & Setup

### Prerequisites
- **Node.js**: v18+ (tested on Node v24.18.0)
- **Python**: 3.10+ (tested on Python 3.11.9)
- **Electron**: Bundled via npm

### 1. Installation
```powershell
# Install Node dependencies
npm install

# (Optional) Install Python requirements if using virtual environment
pip install -r requirements.txt
```

### 2. Launch SKAI Desktop App
```powershell
# Start Electron desktop interface + FastAPI backend supervisor
npm start
```
*Or alternatively launch via Python directly:*
```powershell
python run_sk_ai_4.py
```

### 3. Run Automated Tests
```powershell
# Run the complete test suite (50 tests covering OS control, memory, safety, and assistant dispatch)
pytest
```

---

## 🏛️ System Architecture

```
+--------------------------------------------------------------------------+
|                 SKAI Electron Desktop Application                        |
|       (Animated 3D HUD • Waveform Speech-to-Text • Audit Timeline)       |
+--------------------------------------------------------------------------+
             |                                              |
     (HTTP REST API)                                (WebSocket Stream)
             v                                              v
+--------------------------------------------------------------------------+
|                     SKAI Backend Engine (FastAPI)                        |
|                                                                          |
|  [Assistant Intent Dispatcher] ---> [Permission & Safety Gatekeeper]     |
|                                              |                           |
|                                              +---> [Approved Actions]    |
|                                                          |               |
|  +-------------------------------------------------------+------------+  |
|  |                   OS Control & Actuator Suite                      |  |
|  |  • App Manager (Open / Close / List)                               |  |
|  |  • File Manager (Create / Read / Write / Move / Delete)            |  |
|  |  • Terminal Runner (PowerShell / CMD Subprocess)                   |  |
|  |  • Intelligent Search (Content & Filename Matcher)                 |  |
|  |  • Screenshot Actuator (Display Capture & Preview)                 |  |
|  |  • Project Coding Assistant (Tree & Surgical Edit)                 |  |
|  +--------------------------------------------------------------------+  |
|                                                                          |
|  [SQLite Database Persistence]                                           |
|  • Durable Memory Store (%APPDATA%\skai_master.db)                       |
|  • Security Audit Log (%APPDATA%\logs\)                                  |
+--------------------------------------------------------------------------+
```

---

## 📜 Legal & Compliance

- [`LICENSE`](LICENSE) — MIT License (Copyright © 2026 Sumeet Kumar | SK Enterprises)
- [`EULA.md`](EULA.md) — End User License Agreement
- [`PRIVACY_POLICY.md`](PRIVACY_POLICY.md) — Privacy Policy (Local-First Guarantee)
- [`TERMS_OF_USE.md`](TERMS_OF_USE.md) — Terms of Use
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — Open-Source Software Notices

---

**Engineered with pride by Sumeet Kumar | SK Enterprises © 2026**
