# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - PYINSTALLER PRODUCTION BUILD PIPELINE
# FOUNDER & SOLE ARCHITECT: SUMEET KUMAR
# ==============================================================================
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)" -ForegroundColor Cyan
Write-Host "  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR | STANDALONE BUILD SCRIPT" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

# 1. Clean previous build artifacts
Write-Host "`n[STEP 1/3] Cleaning previous build artifacts..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item "build" -Recurse -Force | Out-Null }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force | Out-Null }
Write-Host "  Cleaned build and dist directories." -ForegroundColor Green

# 2. Run PyInstaller
Write-Host "`n[STEP 2/3] Compiling Standalone Executable with PyInstaller..." -ForegroundColor Yellow
pyinstaller --noconfirm SK_AI_4.0.spec
$BuildExitCode = $LASTEXITCODE

if ($BuildExitCode -ne 0) {
    Write-Error "PyInstaller build failed with exit code $BuildExitCode."
    Exit $BuildExitCode
}

# 3. Verify Output
Write-Host "`n[STEP 3/3] Verifying Output Executable..." -ForegroundColor Yellow
$ExePath = Join-Path $RootDir "dist\SK_AI_4.0\SK_AI_4.0.exe"

if (Test-Path $ExePath) {
    $ExeSize = (Get-Item $ExePath).Length / 1MB
    Write-Host "  [BUILD SUCCESS]: Executable generated at: $ExePath" -ForegroundColor Green
    Write-Host "  [SIZE]: $([math]::Round($ExeSize, 2)) MB" -ForegroundColor Green
} else {
    Write-Error "Executable not found at expected location: $ExePath"
    Exit 1
}

Write-Host "`n========================================================================" -ForegroundColor Green
Write-Host "  BUILD COMPLETE: Production standalone bundle ready in dist\SK_AI_4.0" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
