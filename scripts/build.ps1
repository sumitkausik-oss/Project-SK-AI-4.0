# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - MASTER BUILD PIPELINE
# FOUNDER & SOLE ARCHITECT: SUMEET KUMAR
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)" -ForegroundColor Cyan
Write-Host "  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR | MASTER BUILD SCRIPT" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

function Invoke-BuildStep {
    param(
        [Parameter(Mandatory=$true)][string]$Name,
        [Parameter(Mandatory=$true)][scriptblock]$Action
    )
    Write-Host "`n--------------------------------------------------" -ForegroundColor Yellow
    Write-Host ">> STEP: $Name" -ForegroundColor Yellow
    Write-Host "--------------------------------------------------" -ForegroundColor Yellow
    $global:LASTEXITCODE = 0
    & $Action
    if ($global:LASTEXITCODE -ne 0) {
        throw "CRITICAL FAILURE: Build step '$Name' exited with code $global:LASTEXITCODE"
    }
    Write-Host "PASSED: $Name" -ForegroundColor Green
}

# 1. Verify Node and Python Environment
Invoke-BuildStep -Name "Environment Verification" -Action {
    node --version
    npm --version
    python --version
}

# 2. Run Test Suite
Invoke-BuildStep -Name "Automated Test Suite (pytest)" -Action {
    python -m pytest
}

# 3. Validate Electron and Electron Builder Dependencies
Invoke-BuildStep -Name "Electron and Electron Builder Check" -Action {
    npx electron -v
    npx electron-builder --version
}

# 4. Verify Frontend Assets
Invoke-BuildStep -Name "Frontend Asset Validation" -Action {
    if (-not (Test-Path "frontend\index.html")) {
        throw "Missing frontend\index.html"
    }
    if (-not (Test-Path "frontend\js\three.min.js")) {
        throw "Missing frontend\js\three.min.js"
    }
    Write-Host "Frontend HTML and Three.js offline core verified."
}

Write-Host "`n========================================================================" -ForegroundColor Green
Write-Host "  MASTER BUILD VERIFICATION COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
