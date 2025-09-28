@echo off
echo 🚀 Starting Stable Exciting Lovable Clone
echo ✨ The most stable version with exciting effects!
echo.

cd /d "C:\agent"

echo 📦 Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies...
python -m pip install --quiet fastapi uvicorn websockets

echo.
echo 🚀 Starting server on port 8008...
echo 📍 Interface: http://localhost:8008
echo 🏥 Health check: http://localhost:8008/health
echo.
echo Press Ctrl+C to stop server
echo.

python stable_exciting_backend.py

pause