#!/usr/bin/env python3
"""
🚀 Simple AI Code Generator - ทำงานได้จริง ไม่ใช่ mockup!
เขียนใหม่ทั้งหมด เพื่อให้ AI สร้างโค้ดได้จริง ๆ
"""
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from openai import OpenAI

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is required!")

client = OpenAI(api_key=API_KEY)
WORKSPACE = Path("C:/agent/generated_apps")
WORKSPACE.mkdir(parents=True, exist_ok=True)

# FastAPI App
app = FastAPI(title="AI Code Generator", description="🤖 AI ที่เขียนโค้ดได้จริง ๆ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount generated apps
app.mount("/apps", StaticFiles(directory=str(WORKSPACE)), name="generated_apps")

# Models
class CodeRequest(BaseModel):
    prompt: str
    app_type: str = "mobile"  # mobile, web, desktop
    framework: str = "react_native"  # react_native, flutter, react, vue

class CodeResponse(BaseModel):
    success: bool
    message: str
    app_path: Optional[str] = None
    app_url: Optional[str] = None
    files_created: int = 0
    code_preview: Optional[str] = None
    error: Optional[str] = None

# AI Code Generation Functions
async def generate_mobile_app_with_ai(prompt: str, framework: str = "react_native") -> Dict[str, Any]:
    """ใช้ AI สร้าง Mobile App จริง ๆ"""
    
    try:
        # AI Prompt สำหรับสร้าง Mobile App
        ai_prompt = f"""
คุณเป็น expert mobile app developer ที่สร้าง {framework} app ที่ทำงานได้จริง

User Request: {prompt}

สร้าง mobile app ที่สมบูรณ์ตาม request โดย:

1. วิเคราะห์ความต้องการจาก prompt
2. สร้างโครงสร้าง app ที่เหมาะสม  
3. เขียนโค้ดที่ทำงานได้จริง มี navigation, state management
4. ใช้ UI components ที่เหมาะสมกับธุรกิจ
5. มี error handling และ loading states

ส่งกลับเป็น JSON format:
{{
    "app_name": "ชื่อแอป",
    "description": "คำอธิบายแอป", 
    "main_component": "โค้ด App.tsx หลัก (ต้องครบถ้วนพร้อมใช้งาน)",
    "package_json": "package.json configuration",
    "additional_files": [
        {{"filename": "components/Header.tsx", "content": "โค้ดไฟล์"}},
        {{"filename": "screens/HomeScreen.tsx", "content": "โค้ดไฟล์"}}
    ]
}}

โค้ดต้อง:
- ใช้ TypeScript
- มี proper imports
- ทำงานได้จริงไม่ใช่ mockup
- มี state management
- responsive design
- ใส่ comments เป็นไทย
"""

        print(f"🤖 AI กำลังสร้าง mobile app: {prompt}")
        
        response = client.chat.completions.create(
            model="gpt-4o",  # ใช้ model ดีสุด
            messages=[
                {"role": "system", "content": "คุณเป็น expert mobile app developer ที่สร้างแอปที่ทำงานได้จริง"},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=4000,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Parse AI response
        if ai_response.startswith('```json'):
            ai_response = ai_response.replace('```json', '').replace('```', '')
        
        app_data = json.loads(ai_response)
        
        # สร้างโฟลเดอร์แอป
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        app_name = app_data.get('app_name', 'mobile_app').replace(' ', '_')
        app_dir = WORKSPACE / f"{app_name}_{timestamp}"
        app_dir.mkdir(parents=True, exist_ok=True)
        
        files_created = 0
        
        # สร้าง package.json
        if app_data.get('package_json'):
            package_file = app_dir / "package.json"
            with open(package_file, 'w', encoding='utf-8') as f:
                if isinstance(app_data['package_json'], str):
                    f.write(app_data['package_json'])
                else:
                    json.dump(app_data['package_json'], f, indent=2, ensure_ascii=False)
            files_created += 1
        
        # สร้าง App.tsx หลัก
        if app_data.get('main_component'):
            main_file = app_dir / "App.tsx"
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(app_data['main_component'])
            files_created += 1
        
        # สร้างไฟล์เพิ่มเติม
        if app_data.get('additional_files'):
            for file_info in app_data['additional_files']:
                file_path = app_dir / file_info['filename']
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info['content'])
                files_created += 1
        
        # สร้าง README.md
        readme_content = f"""# {app_data.get('app_name', 'Mobile App')}

{app_data.get('description', 'AI Generated Mobile Application')}

## การติดตั้ง

```bash
npm install
# สำหรับ React Native
npx react-native run-android
npx react-native run-ios
```

## ฟีเจอร์

- สร้างด้วย AI อัตโนมัติ
- ใช้ {framework}
- ทำงานได้จริง (ไม่ใช่ mockup)
- Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## โครงสร้างไฟล์

- App.tsx - Main component
- components/ - UI Components  
- screens/ - App Screens
- package.json - Dependencies
"""
        
        readme_file = app_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        files_created += 1
        
        return {
            'success': True,
            'app_path': str(app_dir),
            'app_url': f"/apps/{app_dir.name}",
            'files_created': files_created,
            'code_preview': app_data.get('main_component', '')[:500] + "...",
            'message': f"✅ สร้าง {app_data.get('app_name')} สำเร็จ! ({files_created} ไฟล์)"
        }
        
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f"AI response ไม่ใช่ JSON ที่ถูกต้อง: {str(e)}",
            'message': "❌ AI ตอบกลับในรูปแบบที่ไม่ถูกต้อง"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"❌ เกิดข้อผิดพลาด: {str(e)}"
        }

async def generate_web_app_with_ai(prompt: str, framework: str = "react") -> Dict[str, Any]:
    """ใช้ AI สร้าง Web App จริง ๆ"""
    
    try:
        ai_prompt = f"""
คุณเป็น expert web developer ที่สร้าง {framework} web application

User Request: {prompt}

สร้าง web application ที่สมบูรณ์ตาม request โดย:

1. วิเคราะห์ความต้องการจาก prompt
2. สร้าง responsive web app
3. ใช้ modern CSS และ JavaScript
4. มี interactive features
5. ทำงานได้จริงไม่ใช่ static

ส่งกลับเป็น JSON format:
{{
    "app_name": "ชื่อเว็บไซต์",
    "description": "คำอธิบาย",
    "index_html": "โค้ด HTML หลัก (ครบถ้วน)",
    "styles_css": "โค้ด CSS (สวยงาม responsive)",
    "script_js": "โค้ด JavaScript (interactive)",
    "additional_files": [
        {{"filename": "components.js", "content": "โค้ดไฟล์"}}
    ]
}}

เว็บไซต์ต้อง:
- Responsive design
- Modern UI/UX
- Interactive features
- ทำงานได้จริงบน browser
- ใส่ comments เป็นไทย
"""

        print(f"🌐 AI กำลังสร้าง web app: {prompt}")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "คุณเป็น expert web developer ที่สร้างเว็บไซต์ที่ทำงานได้จริง"},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=4000,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        if ai_response.startswith('```json'):
            ai_response = ai_response.replace('```json', '').replace('```', '')
        
        app_data = json.loads(ai_response)
        
        # สร้างโฟลเดอร์เว็บไซต์
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        app_name = app_data.get('app_name', 'web_app').replace(' ', '_')
        app_dir = WORKSPACE / f"{app_name}_{timestamp}"
        app_dir.mkdir(parents=True, exist_ok=True)
        
        files_created = 0
        
        # สร้าง index.html
        if app_data.get('index_html'):
            with open(app_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(app_data['index_html'])
            files_created += 1
        
        # สร้าง styles.css
        if app_data.get('styles_css'):
            with open(app_dir / "styles.css", 'w', encoding='utf-8') as f:
                f.write(app_data['styles_css'])
            files_created += 1
        
        # สร้าง script.js
        if app_data.get('script_js'):
            with open(app_dir / "script.js", 'w', encoding='utf-8') as f:
                f.write(app_data['script_js'])
            files_created += 1
        
        # สร้างไฟล์เพิ่มเติม
        if app_data.get('additional_files'):
            for file_info in app_data['additional_files']:
                file_path = app_dir / file_info['filename']
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info['content'])
                files_created += 1
        
        return {
            'success': True,
            'app_path': str(app_dir),
            'app_url': f"/apps/{app_dir.name}/index.html",
            'files_created': files_created,
            'code_preview': app_data.get('index_html', '')[:500] + "...",
            'message': f"✅ สร้าง {app_data.get('app_name')} เว็บไซต์สำเร็จ! ({files_created} ไฟล์)"
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"❌ เกิดข้อผิดพลาดสร้างเว็บไซต์: {str(e)}"
        }

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "message": "🤖 AI Code Generator พร้อมทำงาน!",
        "timestamp": datetime.now().isoformat(),
        "workspace": str(WORKSPACE),
        "openai_available": bool(API_KEY)
    }

@app.post("/generate", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    """🚀 สร้างโค้ดด้วย AI จริง ๆ"""
    
    try:
        print(f"🎯 Request: {request.prompt} | Type: {request.app_type} | Framework: {request.framework}")
        
        if request.app_type == "mobile":
            result = await generate_mobile_app_with_ai(request.prompt, request.framework)
        elif request.app_type == "web":
            result = await generate_web_app_with_ai(request.prompt, request.framework)
        else:
            return CodeResponse(
                success=False,
                message="❌ รองรับเฉพาะ mobile และ web app เท่านั้น",
                error="Unsupported app_type"
            )
        
        return CodeResponse(**result)
        
    except Exception as e:
        return CodeResponse(
            success=False,
            message=f"❌ เกิดข้อผิดพลาด: {str(e)}",
            error=str(e)
        )

@app.get("/apps/{app_name}")
async def view_app(app_name: str):
    """ดูแอปที่สร้างแล้ว"""
    app_dir = WORKSPACE / app_name
    
    if not app_dir.exists():
        raise HTTPException(status_code=404, detail="ไม่พบแอปที่ต้องการ")
    
    # หา index file
    index_files = ["index.html", "App.tsx", "README.md"]
    
    for index_file in index_files:
        if (app_dir / index_file).exists():
            return FileResponse(app_dir / index_file)
    
    # แสดงรายการไฟล์
    files = [f.name for f in app_dir.iterdir() if f.is_file()]
    return {"app_name": app_name, "files": files}

@app.get("/list")
async def list_generated_apps():
    """แสดงรายการแอปที่สร้างแล้ว"""
    
    apps = []
    for app_dir in WORKSPACE.iterdir():
        if app_dir.is_dir():
            files = [f.name for f in app_dir.iterdir() if f.is_file()]
            apps.append({
                "name": app_dir.name,
                "path": str(app_dir),
                "url": f"/apps/{app_dir.name}",
                "files": files,
                "created": datetime.fromtimestamp(app_dir.stat().st_ctime).isoformat()
            })
    
    return {"apps": apps, "total": len(apps)}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting AI Code Generator...")
    print(f"📁 Workspace: {WORKSPACE}")
    print(f"🔑 OpenAI API: {'✅' if API_KEY else '❌'}")
    print("📊 API Documentation: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    print("📱 Generated Apps: http://localhost:8001/list")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")