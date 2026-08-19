# BUILD & PACKAGING PIPELINE — SK AI 4.0

**Platform Version:** Jarvis Platform V5.0  
**Target Platform:** Windows 10/11 64-bit (x86_64)  
**Architect:** Sumeet Kumar (SK Enterprises)  

---

## 1. OVERVIEW

SK AI 4.0 uses a dual packaging system:
1. **PyInstaller** (`SK_AI_4.0.spec`): Compiles the entire Python 3.11 runtime, FastAPI dependencies, SQLite engine, frontend static files, assets, and core engines into a self-contained bundle (`dist/SK_AI_4.0/SK_AI_4.0.exe`).
2. **Inno Setup 6** (`installer_setup_sk4.iss`): Packages the compiled `dist/SK_AI_4.0` directory into an enterprise-grade Windows Setup Wizard (`release/SK_AI_4.0_Setup_x64_v5.0.0.exe`).
3. **Portable ZIP Generator** (`scripts/package.ps1`): Compresses the standalone application bundle into `release/SK_AI_4.0_Portable_x64_v5.0.0.zip` alongside cryptographic SHA-256 verification hashes.

---

## 2. REPRODUCIBLE BUILD STEPS

### Step 1: Run PyInstaller Standalone Build
```powershell
.\scripts\build.ps1
```
*Output: `dist\SK_AI_4.0\SK_AI_4.0.exe` (13+ MB standalone executable).*

### Step 2: Package Release & Installer
```powershell
.\scripts\package.ps1
```
*Outputs:*
- `release/SK_AI_4.0_Portable_x64_v5.0.0.zip`
- `release/SK_AI_4.0_Setup_x64_v5.0.0.exe` (when ISCC is installed)
- `release/SHA256SUMS.txt`

---

## 3. VERIFYING BUILD INTEGRITY

To verify the generated binaries using PowerShell:

```powershell
Get-FileHash release\SK_AI_4.0_Portable_x64_v5.0.0.zip -Algorithm SHA256
```
Compare the output against the values recorded in `release/SHA256SUMS.txt`.
