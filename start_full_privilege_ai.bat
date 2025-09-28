@echo off
echo 🤖 Starting Full-Privilege AI Agent System...
echo.
echo ==========================================
echo   Full-Privilege AI Agent System
echo   AI ที่มีสิทธิ์เต็มที่ในการทำงาน
echo   เหมือน Lovable แต่ราคาไม่แพง
echo ==========================================
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
echo 📦 กำลังติดตั้ง dependencies สำหรับ Full-Privilege AI...
pip install fastapi uvicorn python-multipart openai python-dotenv aiofiles sqlite3 gitpython
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

REM Create workspace directories
echo 📁 สร้าง workspace directories...
if not exist "user_workspaces" mkdir "user_workspaces"
if not exist "templates" mkdir "templates"

echo ✅ Directories สร้างเรียบร้อย
echo.

REM Start Full-Privilege AI System
echo 🚀 เริ่มต้น Full-Privilege AI System...
start "Full-Privilege AI System" python full_privilege_ai_system.py

REM Wait a moment
timeout /t 5 /nobreak >nul

REM Open interface
echo 🌐 เปิด AI Interface...
start "" full_privilege_interface.html

echo.
echo ✅ Full-Privilege AI System เริ่มต้นแล้ว!
echo.
echo 📍 Backend: http://localhost:8002
echo 📍 Frontend: full_privilege_interface.html
echo 📁 User Workspaces: user_workspaces/
echo.
echo 🎯 คุณสมบัติพิเศษ:
echo    🤖 AI มีสิทธิ์เต็มที่ในการสร้าง/แก้ไข/ลบไฟล์
echo    👥 Multi-User System - แต่ละ User มี workspace แยก
echo    🔗 GitHub Integration - เชื่อมต่อและ deploy ได้จริง
echo    💰 Cost-Effective - เหมือน Lovable แต่ราคาไม่แพง
echo.
pause