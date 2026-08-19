# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - AUTOMATED ENVIRONMENT SETUP SCRIPT
# INVENTOR & SOLE ARCHITECT: SUMIT KUMAR
# ==============================================================================
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)" -ForegroundColor Cyan
Write-Host "  INVENTOR & SOLE ARCHITECT: SUMIT KUMAR | SETUP & BOOTSTRAP PIPELINE" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

# 1. Verify Python Installation
Write-Host "`n[STEP 1/4] Verifying Python Environment..." -ForegroundColor Yellow
$PythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python is not installed or not available on PATH."
    Exit 1
}
Write-Host "  Found: $PythonVersion" -ForegroundColor Green

# 2. Install Required Python Packages
Write-Host "`n[STEP 2/4] Installing Production & Development Dependencies..." -ForegroundColor Yellow
pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies from requirements-dev.txt"
    Exit 1
}
Write-Host "  Dependencies installed successfully." -ForegroundColor Green

# 3. Create UAC-Safe Data & Log Directories
Write-Host "`n[STEP 3/4] Initializing %APPDATA% Storage Directories..." -ForegroundColor Yellow
$AppDataDir = [System.Environment]::ExpandEnvironmentVariables("%APPDATA%\SK Enterprises\SK AI 4.0")
$LogsDir = Join-Path $AppDataDir "logs"
$StorageDir = Join-Path $AppDataDir "storage"

New-Item -Path $AppDataDir -ItemType Directory -Force | Out-Null
New-Item -Path $LogsDir -ItemType Directory -Force | Out-Null
New-Item -Path $StorageDir -ItemType Directory -Force | Out-Null
Write-Host "  Storage directories verified at: $AppDataDir" -ForegroundColor Green

# 4. Bootstrap SQLite Database Schema
Write-Host "`n[STEP 4/4] Initializing SQLite Database & Default Admin..." -ForegroundColor Yellow
python -c "from src_backend.app.database.init_db import init_database; init_database(); print('  Database schema created successfully.')"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Database initialization failed."
    Exit 1
}

Write-Host "`n========================================================================" -ForegroundColor Green
Write-Host "  SETUP COMPLETE: SK AI 4.0 is ready for development & deployment!" -ForegroundColor Green
Write-Host "  Run '.\scripts\dev.ps1' to launch the live application." -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
