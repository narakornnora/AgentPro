@echo off
echo 🎼 Starting AI Orchestrator System...
echo.
echo ==========================================
echo   AI Orchestrator System
echo   AI Chat + Team Lead + Specialized Agents
echo   แชทธรรมดา แต่ AI ทำงานประสานกันเบื้องหลัง
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
echo 📦 กำลังติดตั้ง dependencies สำหรับ AI Orchestrator...
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

REM Create workspace directories
echo 📁 สร้าง workspace directories...
if not exist "workspace" mkdir "workspace"

echo ✅ Directories สร้างเรียบร้อย
echo.

REM Start AI Orchestrator System
echo 🎼 เริ่มต้น AI Orchestrator System...
start "AI Orchestrator Backend" python workflow_orchestrator.py

REM Wait a moment
timeout /t 5 /nobreak >nul

REM Open interface
echo 🌐 เปิด Orchestrator Interface...
start "" orchestrator_interface.html

echo.
echo ✅ AI Orchestrator System เริ่ต้นแล้ว!
echo.
echo 📍 Backend: http://localhost:8003
echo 📍 Frontend: orchestrator_interface.html
echo 📁 Workspace: workspace/
echo.
echo 🎯 วิธีใช้งาน:
echo    💬 แชทธรรมดาเหมือน ChatGPT
echo    📝 AI จะถามจนได้ข้อมูลครบถ้วน
echo    👨‍💼 Team Lead บันทึกและวางแผน
echo    👥 Specialized Agents ทำงานประสานกัน
echo    ✅ ได้ผลงานสมบูรณ์แบบ
echo.
pause