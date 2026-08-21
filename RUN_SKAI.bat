@echo off
title SKAI — Powered by SK Enterprises
color 0B
echo ================================================================================
echo   SKAI DESKTOP ASSISTANT
echo   Founder ^& Sole Architect: Sumeet Kumar ^| SK Enterprises
echo ================================================================================
echo.
echo Starting SKAI Autonomous Engine and Cyberpunk HUD...
echo.

cd /d "%~dp0"

REM Try to launch via Electron if npm/npx is present
where npx >nul 2>nul
if %errorlevel% equ 0 (
    echo Launching SKAI via Electron Desktop Container...
    start "" npx electron .
    goto done
)

REM Fallback to Python launcher
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Launching SKAI via Python Direct Desktop Launcher...
    start "" python run_sk_ai_4.py
    goto done
)

echo [ERROR] Neither Node.js (npx) nor Python was found on PATH.
pause
exit /b 1

:done
echo.
echo [ONLINE] SKAI process launched successfully!
timeout /t 3 >nul
exit /b 0
