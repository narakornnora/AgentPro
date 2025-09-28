@echo off
echo.
echo ================================
echo  🚀 Lovable Clone - Quick Test  
echo ================================
echo.

echo [Step 1] Starting the system...
cd /d "C:\agent\apps\orchestrator"

echo [Step 2] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo [Step 3] Installing dependencies...
pip install -r requirements.txt >nul 2>&1

echo [Step 4] Starting FastAPI server...
start /b python main.py

echo [Step 5] Waiting for server startup...
timeout /t 5 >nul

echo [Step 6] Opening Landing Page...
cd /d "C:\agent"
start lovable_landing.html

echo [Step 7] Opening Chat Interface...
timeout /t 2 >nul
start lovable_chat.html

echo.
echo ✅ System started successfully!
echo.
echo 📖 Testing Instructions:
echo   1. Landing page should open automatically
echo   2. Chat interface should open automatically  
echo   3. Type a message in chat to test AI response
echo   4. Check preview panel for generated code
echo.
echo 🔧 Troubleshooting:
echo   - If chat doesn't work, check: http://localhost:8001/docs
echo   - If errors occur, see TESTING_GUIDE.md
echo.
echo Press any key to exit...
pause >nul