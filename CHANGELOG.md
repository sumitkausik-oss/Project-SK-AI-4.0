# SKAI Changelog

All notable changes to the **SKAI** desktop assistant platform are documented in this file.

---

## [0.0.1] - 2026-08-21

### 🚀 Initial Master Build Release
- **Sovereign Local Architecture:**
  - Complete rebuild with **React 18 + TypeScript + Electron + Vite + Tailwind CSS**.
  - Strict IPC security boundary with typed `contextBridge` exposing `window.skaiApi` (zero direct Node.js API leakage to renderer).
- **Encrypted Secrets Vault (SafeStorage):**
  - Google API key stored at rest using OS-native encryption (Windows DPAPI / Electron `safeStorage`).
  - Key validation tool and show/hide toggle in Settings modal.
- **Voice Conversation Loop:**
  - Real-time Web Speech / WebRTC audio capture.
  - Audio waveform pulse with honest status indicators (`READY`, `LISTENING`, `THINKING`, `SPEAKING`).
  - Natural speech synthesis (TTS) audio response playback.
- **Operating System Control & Tools:**
  - `openApp`, `closeApp`, `listRunningApps`.
  - `createFile`, `readFile`, `writeFile`, `deleteFile`, `createFolder`, `listFolder`.
  - `runTerminalCommand` (PowerShell / CMD subprocess executor).
  - Native display screenshot capture via `desktopCapturer` with instant thumbnail previews.
- **Safety Gatekeeper & Permission Engine:**
  - Interactive Action Confirmation Modal for destructive actions (`DELETE_FILE`, `TERMINAL_COMMAND`).
  - Customizable safety policies (auto-approve read-only, require confirmation for destructive).
- **Local Vector & SQLite Memory Store:**
  - Durable vector memory embedding and semantic search.
  - Keyword and cosine similarity matching persisting across app restarts.
  - Memory Inspector UI with fact search, creation, and deletion.
- **Web Awareness & Search:**
  - Integrated web search with instant summarization and citation links.
- **Coding Helper Mode:**
  - Project directory scanner and file tree visualizer.
  - Surgical code editor with live syntax view.
  - Subprocess test runner with test output console.
- **Design & UI:**
  - Dark glassmorphic interface with violet/indigo accent (`#6366f1` / `#818cf8`) and sky blue highlights (`#38bdf8`).
  - Custom frameless titlebar with minimize, maximize, and close controls.
  - Real-time audit trail inspector.
- **Packaging:**
  - Windows NSIS 64-bit installer (`SKAI_Setup_v0.0.1.exe`) and portable binary.
  - One-click Windows batch launcher (`RUN_SKAI.bat`).
