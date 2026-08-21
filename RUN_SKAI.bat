@echo off
title SKAI — Powered by SK Enterprises
color 0B
echo ================================================================================
echo   SKAI — Sovereign Local-First Desktop AI Assistant (v0.0.1)
echo   Founder ^& Sole Architect: Sumeet Kumar ^| Powered by SK Enterprises
echo ================================================================================
echo.
echo Launching SKAI Desktop Container...
echo.

cd /d "%~dp0"

REM If dist-electron exists, launch electron directly
if exist "dist-electron\main.js" (
    echo Starting SKAI...
    start "" npx electron .
    goto done
)

REM If not built, build first
echo First-time run detected. Compiling React + TypeScript frontend and Electron shell...
call npm run build
start "" npx electron .

:done
echo.
echo [ONLINE] SKAI process launched successfully!
timeout /t 3 >nul
exit /b 0
