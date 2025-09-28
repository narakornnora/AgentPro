@echo off
echo 🚀 Starting Real Full-Stack App Generator...
echo.
echo ========================================
echo   Real Full-Stack App Generator
echo   สร้างแอปจริงที่ใช้งานได้ 100%
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ไม่พบ! กรุณาติดตั้ง Python ก่อน
    pause
    exit /b 1
)

echo ✅ Python พบแล้ว
echo.

REM Install dependencies
echo 📦 กำลังติดตั้ง dependencies...
pip install fastapi uvicorn python-multipart openai python-dotenv aiofiles
if errorlevel 1 (
    echo ❌ ติดตั้ง dependencies ไม่สำเร็จ
    pause
    exit /b 1
)

echo ✅ Dependencies ติดตั้งเรียบร้อย
echo.

REM Check .env file
if not exist .env (
    echo 📝 สร้างไฟล์ .env...
    echo OPENAI_API_KEY=your_openai_api_key_here > .env
    echo ⚠️  กรุณาเพิ่ม OpenAI API Key ใน .env file
    echo.
)

REM Start backend
echo 🚀 เริ่มต้น Backend Server...
start "Real FullStack Backend" python ai_chat_backend_new.py

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Open frontend
echo 🌐 เปิด Frontend Interface...
start "" real_fullstack_interface.html

echo.
echo ✅ ระบบเริ่มต้นแล้ว!
echo.
echo 📍 Backend: http://localhost:8001
echo 📍 Frontend: real_fullstack_interface.html
echo.
echo 🎯 ตอนนี้คุณสามารถสร้างแอป Full-Stack จริงได้แล้ว!
echo    ไม่ใช่ mockup อีกต่อไป 🚀
echo.
pause