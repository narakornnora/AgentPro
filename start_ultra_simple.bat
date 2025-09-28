@echo off
echo 🚀 Starting Ultra Simple Lovable Clone...
echo 📍 No dependencies required!
echo ✨ Built-in Python libraries only
echo.

REM Kill any existing Python processes
taskkill /f /im python.exe >nul 2>&1

echo 🔥 Starting server...
python ultra_simple_backend.py

pause