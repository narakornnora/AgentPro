@echo off
echo ========================================
echo 🚀 AI Chat System - Fixed Version
echo ========================================
cd /d C:\agent

echo 1. Starting AI Chat Backend...
start "AI_Chat_Backend" python ai_chat_backend.py

echo 2. Waiting for backend to start (8 seconds)...
timeout /t 8 /nobreak > nul

echo 3. Testing AI Generation...
python quick_test.py

echo 4. Opening Chat Interface in Browser...
start http://localhost:8001

echo ========================================
echo ✅ System Ready!
echo 💬 Chat Interface: http://localhost:8001
echo 📊 API Docs: http://localhost:8001/docs
echo ========================================
pause