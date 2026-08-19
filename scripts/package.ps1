# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - ELECTRON BUILDER PACKAGING PIPELINE
# FOUNDER & SOLE ARCHITECT: SUMEET KUMAR
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)" -ForegroundColor Cyan
Write-Host "  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR | ELECTRON BUILDER PACKAGING" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

function Invoke-PkgStep {
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
        throw "CRITICAL FAILURE: Packaging step '$Name' exited with code $global:LASTEXITCODE"
    }
    Write-Host "PASSED: $Name" -ForegroundColor Green
}

# 1. Clean Stale Release Outputs
Invoke-PkgStep -Name "Clean Release Directory" -Action {
    if (Test-Path "release") {
        Get-ChildItem -Path "release" -Exclude "*.md" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        New-Item -ItemType Directory -Path "release" -Force | Out-Null
    }
}

# 2. Run Master Build Verification
Invoke-PkgStep -Name "Pre-Packaging Validation" -Action {
    & "$PSScriptRoot\build.ps1"
}

# 3. Prepare Environment & winCodeSign Cache
Invoke-PkgStep -Name "Prepare Environment and CodeSign Cache" -Action {
    python scripts\prepare_wincodesign.py
    $env:CSC_IDENTITY_AUTO_DISCOVERY = "false"
}

# 4. Compile Windows NSIS Installer via Electron Builder
Invoke-PkgStep -Name "Electron Builder Windows NSIS Compilation" -Action {
    $env:CSC_IDENTITY_AUTO_DISCOVERY = "false"
    npx electron-builder --win nsis --x64
}

# 5. Verify Installer Artifact
Invoke-PkgStep -Name "Verify Output Installer" -Action {
    $installer = Get-ChildItem -Path "release" -Filter "SK_AI_4.0_Setup_x64_v*.exe" | Select-Object -First 1
    if (-not $installer) {
        throw "CRITICAL FAILURE: Output installer 'SK_AI_4.0_Setup_x64_v*.exe' not found in release/ directory!"
    }
    $sizeMb = [math]::Round($installer.Length / 1MB, 2)
    Write-Host "Installer Found: $($installer.FullName) ($sizeMb MB)"
    if ($sizeMb -lt 20) {
        throw "CRITICAL WARNING: Installer size ($sizeMb MB) is unexpectedly small!"
    }
}

# 6. Generate SHA-256 Checksums
Invoke-PkgStep -Name "Generate SHA-256 Checksums" -Action {
    $checksumFile = "release\SHA256SUMS.txt"
    $lines = @()
    Get-ChildItem -Path "release" -Filter "*.exe" | ForEach-Object {
        $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
        $lines += "$hash  $($_.Name)"
    }
    $lines | Set-Content -Path $checksumFile -Encoding utf8
    Write-Host "Checksums written to: $checksumFile"
    Get-Content $checksumFile | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
}

Write-Host "`n========================================================================" -ForegroundColor Green
Write-Host "  ELECTRON BUILDER PACKAGING VERIFIED AND COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
