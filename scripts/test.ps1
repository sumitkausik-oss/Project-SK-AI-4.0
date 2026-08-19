# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - AUTOMATED PYTEST SUITE RUNNER
# FOUNDER & SOLE ARCHITECT: SUMEET KUMAR
# ==============================================================================
param(
    [switch]$VerboseOutput,
    [switch]$Coverage
)

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)" -ForegroundColor Cyan
Write-Host "  FOUNDER & SOLE ARCHITECT: SUMEET KUMAR | AUTOMATED TEST RUNNER" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$pytestArgs = @("tests/")

if ($VerboseOutput) {
    $pytestArgs += "-v"
}

if ($Coverage) {
    $pytestArgs += "--cov=src_backend"
    $pytestArgs += "--cov-report=term-missing"
}

python -m pytest $pytestArgs
$TestExitCode = $LASTEXITCODE

if ($TestExitCode -eq 0) {
    Write-Host "`n[TEST RESULT]: ALL TESTS PASSED SUCCESSFULLY! (EXIT 0)" -ForegroundColor Green
} else {
    Write-Host "`n[TEST RESULT]: TESTS FAILED WITH CODE $TestExitCode" -ForegroundColor Red
}

Exit $TestExitCode
