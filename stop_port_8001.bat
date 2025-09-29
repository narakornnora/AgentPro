@echo off
setlocal
cd /d %~dp0
for /f "tokens=*" %%p in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-NetTCPConnection -State Listen -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess)"') do (
  echo Stopping PID %%p on port 8001
  taskkill /PID %%p /F >NUL 2>&1
)
echo Done.
endlocal
