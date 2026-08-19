# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - TEST SUITE RUNNER
# INVENTOR & SOLE ARCHITECT: SUMIT KUMAR
# ==============================================================================
param(
    [switch]$VerboseOutput,
    [switch]$Coverage
)

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  RUNNING SK AI 4.0 AUTOMATED TEST SUITE" -ForegroundColor Cyan
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
