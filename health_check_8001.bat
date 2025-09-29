@echo off
setlocal
cd /d %~dp0
powershell -NoProfile -ExecutionPolicy Bypass -Command "(Invoke-RestMethod -UseBasicParsing http://localhost:8001/health) | ConvertTo-Json -Depth 5" || echo Health check failed
endlocal
