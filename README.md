# SKAI — Sovereign Desktop AI Assistant (v0.0.1)

> **Powered by SK Enterprises**  
> **Founder & Sole Architect:** Sumeet Kumar  
> **License:** MIT Open Core

---

## 🚀 Overview

**SKAI** is a local-first, voice-driven desktop AI assistant built from the ground up for Windows. It combines operating system actuation, encrypted credential management, local vector memory, and Google Gemini API intelligence into a dark glassmorphic desktop interface.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Shell & Core** | Electron 33 (CommonJS Main Process + Strict Typed IPC Bridge) |
| **Frontend UI** | React 18, TypeScript 5, Tailwind CSS, Lucide Icons |
| **Build System** | Vite 6 + TypeScript Compiler (`tsc`) |
| **Voice & Speech** | Web Speech / WebRTC Audio Streaming + SpeechSynthesis TTS |
| **Intelligence** | Google Gemini 2.0 Flash / Pro with Tool Calling |
| **Secrets Vault** | Electron `safeStorage` (OS-native Windows DPAPI Encryption at Rest) |
| **Local Memory** | Embedded Vector Store with Cosine Similarity Search |
| **Packaging** | Electron Builder (NSIS 64-bit Installer) |

---

## ⚡ Quick Start & Running Locally

### Option 1: 1-Click Windows Launcher
Double-click [`RUN_SKAI.bat`](file:///d:/Project%20SK%20AI%204.0/RUN_SKAI.bat) in the project root.

### Option 2: Command Line (Developer Mode)
```bash
# Install dependencies
npm install

# Start Vite dev server + Electron with hot-reloading
npm run dev
```

### Option 3: Production Build & Packaging
```bash
# Build React frontend & Electron main process
npm run build

# Package NSIS Windows Installer (release\SKAI_Setup_v0.0.1.exe)
npm run dist:win
```

---

## 🛡️ Security & Privacy Architecture

- **Encrypted Secrets:** API keys entered into the Settings panel are encrypted using the operating system's native cryptographic vault (Windows DPAPI via Electron `safeStorage`). Plaintext keys are **never** stored in files.
- **Strict IPC Separation:** The React renderer runs in a sandboxed context with zero direct access to Node.js `fs` or `child_process`. All OS interactions go through a typed `window.skaiApi` bridge.
- **Interactive Safety Gates:** Destructive operations (such as file deletions or terminal commands) trigger an interactive **Action Confirmation Modal** requiring explicit user approval before execution.

---

## 🧠 Core Features

1. **Voice Conversation Loop:** Real-time audio capture, animated speech waveform, listening/thinking/speaking status indicators, and spoken audio responses.
2. **OS Actuation:** Open/close apps, create/read/write/delete files, list directory contents, and run terminal commands.
3. **Display Capture:** Take instant high-resolution screenshots with live visual previews.
4. **Local Vector Memory:** Store preferences and facts that persist across restarts with cosine similarity retrieval.
5. **Coding Helper Mode:** Scan project directories, inspect source files, apply surgical code replacements, and run automated test suites.
6. **Web Awareness:** Integrated search engine summarizing online documentation and queries.
7. **System Audit Timeline:** Real-time stream of all executed OS actions with severity ratings and timestamps.

---

## 📜 Copyright & Ownership

**Copyright © 2026 Sumeet Kumar | SK Enterprises. All Rights Reserved.**
