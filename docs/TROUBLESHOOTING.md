# TROUBLESHOOTING & RECOVERY GUIDE — SK AI 4.0

**Platform Version:** Jarvis Platform V5.0  
**Founder & Sole Architect:** Sumeet Kumar (SK Enterprises)  

---

## 1. PORT 8000 ALREADY IN USE

**Symptom:** Backend fails to bind socket with `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`.

**Resolution:**
1. The launcher (`run_sk_ai_4.py`) includes automatic stale PID detection and recovery.
2. To manually release the port via PowerShell:
```powershell
$pidToKill = (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).OwningProcess
if ($pidToKill) { Stop-Process -Id $pidToKill -Force }
```

---

## 2. DATABASE FILE LOCKED OR CORRUPTED

**Symptom:** SQLite reports `database is locked` or `file is not a database`.

**Resolution:**
1. Close all active instances of SK AI 4.0.
2. Check `%APPDATA%\SK Enterprises\SK AI 4.0\` for `.db-wal` or `.db-shm` temporary files.
3. If corruption occurred, restore from the last automatic backup or remove `sk_ai_master.db` to let the system re-seed clean baseline tables on next launch.

---

## 3. LOG LOCATIONS & CRASH REPORTING

All operational and error logs are stored in:
```text
%APPDATA%\SK Enterprises\SK AI 4.0\logs\
├── application.log      # General operational events
├── error.log            # Errors and critical exceptions
└── startup_crash.log    # Fatal bootstrap stack traces
```
To view real-time logs in PowerShell:
```powershell
Get-Content "$env:APPDATA\SK Enterprises\SK AI 4.0\logs\application.log" -Wait -Tail 30
```
