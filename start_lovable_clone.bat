@echo off
echo 🚀 Starting Lovable Clone AI...
echo.
echo 💬 AI App Generator - เหมือน Lovable.dev
echo 📍 Server: http://localhost:8004
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing required packages...
    pip install fastapi uvicorn openai python-dotenv
)

REM Check for OpenAI API Key
if "%OPENAI_API_KEY%"=="" (
    echo.
    echo ⚠️  OpenAI API Key not found!
    echo Please set your API key:
    echo.
    echo 1. Create .env file in this folder
    echo 2. Add: OPENAI_API_KEY=your_api_key_here
    echo.
    echo Or set environment variable:
    echo set OPENAI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)

echo ✅ All checks passed!
echo.
echo Starting server...
python ai_chat_backend_final.py

pause