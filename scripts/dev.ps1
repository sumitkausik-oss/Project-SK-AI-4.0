# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - DEVELOPMENT LAUNCHER SCRIPT
# INVENTOR & SOLE ARCHITECT: SUMIT KUMAR
# ==============================================================================
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  LAUNCHING SK AI 4.0 (PROJECT JARVIS 4.0) IN DEVELOPMENT MODE" -ForegroundColor Cyan
Write-Host "  FOUNDER & SOLE ARCHITECT: SUMIT KUMAR | SK ENTERPRISES" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

python run_sk_ai_4.py
