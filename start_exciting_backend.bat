@echo off
setlocal
cd /d %~dp0

REM Stop any process currently listening on port 8001 (optional)
powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-NetTCPConnection -State Listen -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess) | ForEach-Object { if ($_){ Stop-Process -Id $_ -Force } }" >NUL 2>&1

REM Launch backend in a new window and keep it open
start "Exciting Lovable Backend" cmd /c "python -u \"%cd%\exciting_lovable_backend_clean.py\" & echo. & echo Press any key to close... & pause >nul"

echo Backend launching in a new window on http://localhost:8001
echo If Windows Defender asks, allow access for Python.
endlocal
