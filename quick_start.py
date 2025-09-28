#!/usr/bin/env python3
"""
🚀 Simple AI Orchestrator Launcher
รันระบบ AI Orchestrator แบบง่ายๆ
"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """ตรวจสอบ dependencies"""
    required_packages = ['fastapi', 'uvicorn', 'openai', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)

def check_env():
    """ตรวจสอบ .env file"""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("⚠️  Please add your OpenAI API Key to .env file")
        return False
    return True

def main():
    print("🎼 Starting AI Orchestrator System...")
    
    # ตรวจสอบ dependencies
    check_dependencies()
    
    # ตรวจสอบ .env
    if not check_env():
        input("Press Enter after adding your API key...")
    
    # สร้าง workspace
    workspace = Path("workspace")
    workspace.mkdir(exist_ok=True)
    
    # รัน workflow_orchestrator.py
    print("🚀 Starting backend server...")
    try:
        subprocess.Popen([sys.executable, 'workflow_orchestrator.py'])
        
        # รอ server startup
        time.sleep(3)
        
        # เปิด browser
        print("🌐 Opening interface...")
        webbrowser.open('http://localhost:8003')
        
        print("✅ System started successfully!")
        print("📍 Backend: http://localhost:8003")
        print("💬 Ready to chat!")
        
        input("\nPress Enter to stop the system...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()