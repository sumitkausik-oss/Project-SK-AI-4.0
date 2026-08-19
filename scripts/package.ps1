# ==============================================================================
# SK ENTERPRISES | SK AI 4.0 - RELEASE PACKAGING & CHECKSUM PIPELINE
# INVENTOR & SOLE ARCHITECT: SUMIT KUMAR
# ==============================================================================
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  SK ENTERPRISES | PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)" -ForegroundColor Cyan
Write-Host "  INVENTOR & SOLE ARCHITECT: SUMIT KUMAR | RELEASE PACKAGING PIPELINE" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

# 1. Run Standalone Build if dist not present
if (-not (Test-Path "dist\SK_AI_4.0\SK_AI_4.0.exe")) {
    Write-Host "`n[STEP 1/4] Running standalone PyInstaller build..." -ForegroundColor Yellow
    & ".\scripts\build.ps1"
    if ($LASTEXITCODE -ne 0) { Exit $LASTEXITCODE }
}

# 2. Ensure release directory exists
$ReleaseDir = Join-Path $RootDir "release"
if (-not (Test-Path $ReleaseDir)) {
    New-Item -Path $ReleaseDir -ItemType Directory -Force | Out-Null
}

# 3. Create Portable ZIP
Write-Host "`n[STEP 2/4] Packaging Portable ZIP Distribution..." -ForegroundColor Yellow
$ZipPath = Join-Path $ReleaseDir "SK_AI_4.0_Portable_x64_v5.0.0.zip"
if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }

Compress-Archive -Path "dist\SK_AI_4.0\*" -DestinationPath $ZipPath -CompressionLevel Optimal
$ZipSize = (Get-Item $ZipPath).Length / 1MB
Write-Host "  [PORTABLE ZIP CREATED]: $ZipPath ($([math]::Round($ZipSize, 2)) MB)" -ForegroundColor Green

# 4. Compile Inno Setup Installer if ISCC is installed
Write-Host "`n[STEP 3/4] Checking for Inno Setup Compiler (ISCC.exe)..." -ForegroundColor Yellow
$IsccPaths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "ISCC.exe"
)

$IsccFound = $false
foreach ($p in $IsccPaths) {
    if (Get-Command $p -ErrorAction SilentlyContinue) {
        $IsccExe = $p
        $IsccFound = $true
        break
    } elseif (Test-Path $p) {
        $IsccExe = $p
        $IsccFound = $true
        break
    }
}

if ($IsccFound) {
    Write-Host "  Found Inno Setup Compiler at: $IsccExe" -ForegroundColor Green
    Write-Host "  Compiling Windows Installer..." -ForegroundColor Yellow
    & $IsccExe "installer_setup_sk4.iss"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [INSTALLER CREATED]: release\SK_AI_4.0_Setup_x64_v5.0.0.exe" -ForegroundColor Green
    } else {
        Write-Warning "Inno Setup compilation returned exit code $LASTEXITCODE."
    }
} else {
    Write-Host "  [NOTE]: Inno Setup Compiler (ISCC.exe) not found on local PATH." -ForegroundColor Gray
    Write-Host "  To generate the .exe installer, install Inno Setup 6 and run 'ISCC installer_setup_sk4.iss'." -ForegroundColor Gray
}

# 5. Generate SHA-256 Checksums
Write-Host "`n[STEP 4/4] Generating SHA-256 Release Checksums..." -ForegroundColor Yellow
$ChecksumFile = Join-Path $ReleaseDir "SHA256SUMS.txt"
$ReleaseFiles = Get-ChildItem -Path $ReleaseDir -File | Where-Object { $_.Name -ne "SHA256SUMS.txt" -and $_.Name -ne "RELEASE_NOTES.md" }

$ChecksumContent = @()
foreach ($file in $ReleaseFiles) {
    $hash = (Get-FileHash -Path $file.FullName -Algorithm SHA256).Hash
    $ChecksumContent += "$hash  $($file.Name)"
}

$ChecksumContent | Out-File -FilePath $ChecksumFile -Encoding utf8
Write-Host "  Checksums recorded to: $ChecksumFile" -ForegroundColor Green

Write-Host "`n========================================================================" -ForegroundColor Green
Write-Host "  RELEASE PACKAGING COMPLETE!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
