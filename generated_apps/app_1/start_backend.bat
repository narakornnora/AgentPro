@echo off
cd /d %~dp0
python -m uvicorn backend.main:app --host 0.0.0.0 --port 9000 --log-level info
pause

