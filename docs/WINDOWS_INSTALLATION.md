# WINDOWS INSTALLATION & DEPLOYMENT GUIDE — SK AI 4.0

**Platform Version:** Jarvis Platform V5.0  
**Target Operating System:** Windows 10 / Windows 11 (64-bit)  
**Publisher:** SK Enterprises (Sumeet Kumar)  

---

## 1. INSTALLATION METHODS

### Option A: Standalone Portable ZIP (Zero Installation)
1. Download `SK_AI_4.0_Portable_x64_v5.0.0.zip` from the official release assets.
2. Extract the contents to any local folder (e.g. `C:\SK_AI_4.0\` or `D:\Apps\SK_AI_4.0\`).
3. Double-click `SK_AI_4.0.exe` to launch the application.
4. The system initializes local storage in `%APPDATA%\SK Enterprises\SK AI 4.0\` automatically.

---

### Option B: Windows Setup Wizard (Inno Setup Installer)
1. Download and run `SK_AI_4.0_Setup_x64_v5.0.0.exe`.
2. Follow the setup wizard prompts:
   - Select installation directory (Default: `C:\Program Files\SK Enterprises\SK AI 4.0\`).
   - Choose whether to create a Desktop Shortcut.
   - Click **Install**.
3. On completion, click **Launch SK AI 4.0** or start from the Windows Start Menu.

---

## 2. UNINSTALLATION

- Open **Windows Settings** > **Apps** > **Installed Apps**.
- Locate **SK AI 4.0** and click **Uninstall**.
- The uninstaller cleanly removes all application binaries and Start Menu shortcuts.
- User database files in `%APPDATA%\SK Enterprises\SK AI 4.0\` are preserved to prevent accidental data loss. To perform a complete wipe, manually delete the `%APPDATA%\SK Enterprises\SK AI 4.0\` folder.
