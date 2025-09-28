#!/usr/bin/env python3
"""
🧠 AI Expert Consultant Backend - ปรึกษา แนะนำ แก้ไข ออกแบบ
สร้างแอปสวยๆ มาตรฐานสากล พร้อม Modern UI Libraries
"""
import os
import json
import asyncio
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
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
app = FastAPI(title="AI Chat Backend", description="🤖 Backend for AI Chat Interface")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/generated_apps", StaticFiles(directory=str(WORKSPACE)), name="generated_apps")

# Models
class ChatRequest(BaseModel):
    message: str
    app_type: str = "auto"  # auto, mobile, web (auto = AI will detect)
    framework: str = "auto"  # auto, react_native, flutter, react, vue

class ChatResponse(BaseModel):
    success: bool
    message: str
    app_name: Optional[str] = None
    app_path: Optional[str] = None
    app_url: Optional[str] = None
    files_created: int = 0
    code_preview: Optional[str] = None
    description: Optional[str] = None
    error: Optional[str] = None
    # AI Expert Consultant fields
    ai_consultation: Optional[Dict[str, Any]] = None
    needs_more_info: bool = False
    expert_recommendations: Optional[List[str]] = None
    tech_stack_suggestions: Optional[Dict[str, Any]] = None

async def ai_expert_consultant(prompt: str, mode: str = "analyze") -> Dict[str, Any]:
    """🧠 AI Expert Consultant - ปรึกษา แนะนำ แก้ไข ออกแบบ"""
    
    if mode == "analyze":
        expert_prompt = f"""
คุณเป็น AI Expert Consultant ที่เชี่ยวชาญใน Software Development, UI/UX Design, และ Code Review

User Request: "{prompt}"

ให้วิเคราะห์และตอบสนองในรูปแบบ JSON:
{{
    "consultation_type": "project_analysis|code_review|design_advice|recommendation",
    "response_mode": "ask_questions|provide_solution|give_recommendations",
    "expert_analysis": {{
        "project_type": "mobile_app|web_app|website|desktop_app|api_service",
        "confidence": 0.95,
        "recommended_tech_stack": {{
            "frontend": "React Native|Flutter|React|Vue|Next.js|Angular",
            "backend": "Node.js|Python|PHP|Java|Go",
            "database": "MongoDB|PostgreSQL|MySQL|Firebase",
            "ui_library": "Tailwind CSS|Material-UI|Bootstrap|Chakra UI|Ant Design"
        }},
        "modern_libraries": [
            "framer-motion (animations)",
            "react-spring (smooth animations)", 
            "styled-components (CSS-in-JS)",
            "react-hook-form (forms)",
            "react-query (data fetching)",
            "zustand (state management)",
            "lucide-react (icons)",
            "react-hot-toast (notifications)"
        ],
        "design_system": {{
            "color_palette": "modern gradient|corporate|playful|minimalist",
            "typography": "Inter|Poppins|Roboto|Open Sans",
            "layout": "grid|flexbox|css-grid",
            "components": ["buttons", "forms", "cards", "modals", "navigation"]
        }}
    }},
    "questions_for_user": [
        "คำถามเพื่อให้ได้ข้อมูลเพิ่มเติม"
    ],
    "expert_recommendations": [
        "คำแนะนำจากผู้เชี่ยวชาญ"
    ],
    "code_suggestions": {{
        "improvements": ["การปรับปรุง code"],
        "best_practices": ["แนวทางปฏิบัติที่ดี"],
        "security_tips": ["เทคนิคความปลอดภัย"]
    }},
    "ready_to_build": true|false,
    "needs_more_info": true|false
}}

กฎการตัดสินใจ (STRICT MODE - ห้ามสร้างทันที):
- **ถ้าเป็นครั้งแรก** → ask_questions, needs_more_info: true (ถามเสมอ!)
- **ถ้าข้อมูลไม่ครบ 100%** → ask_questions, needs_more_info: true
- **ready_to_build: true** เฉพาะเมื่อมีข้อมูลครบ:
  1. ประเภทโครงการชัดเจน (เว็บไซต์/เว็บแอป/มือถือ)  
  2. หมวดธุรกิจ (ร้านกาแฟ/คลินิก/โรงเรียน)
  3. ฟีเจอร์หลัก (login/payment/booking)
  4. กลุ่มเป้าหมาย (ลูกค้า/เจ้าของ/ผู้ดูแล)

หากเป็นคำถามเรื่อง:
- "แนะนำ", "library", "framework" → consultation_type: "recommendation", needs_more_info: false
- "code", "review", "ช่วยดู", "แก้ไข" → consultation_type: "code_review", needs_more_info: false  
- "สี", "design", "UI", "UX", "สวย" → consultation_type: "design_advice", needs_more_info: false
- "สร้าง", "ทำ", "app", "เว็บ" → consultation_type: "project_analysis", needs_more_info: true (ถามเพิ่มเสมอ!)

**สำคัญ**: ถ้าผู้ใช้บอก "สร้าง" ต้องถามคำถามเพิ่มเติมเสมอ ห้ามสร้างทันที!
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": expert_prompt}],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean JSON
        if result_text.startswith('```json'):
            result_text = result_text[7:-3].strip()
        elif result_text.startswith('```'):
            result_text = result_text[3:-3].strip()
            
        # Fix trailing commas
        import re
        result_text = re.sub(r',(\s*[}\]])', r'\1', result_text)
        
        analysis = json.loads(result_text)
        return analysis
        
    except Exception as e:
        print(f"Analysis Error: {e}")
        # Fallback analysis
        return {
            "project_type": "mobile_app" if any(word in prompt.lower() for word in ["แอป", "app", "mobile"]) else "web_app",
            "confidence": 0.7,
            "reasoning": "Fallback detection based on keywords",
            "recommended_framework": "react_native",
            "app_category": "other",
            "complexity": "medium",
            "estimated_screens": 5,
            "key_features_detected": ["Basic functionality"],
            "target_platform": "mobile",
            "preview_type": "mobile_phone"
        }

async def generate_mobile_app_real(prompt: str, framework: str = "react_native") -> Dict[str, Any]:
    """🎨 AI Expert สร้าง Mobile App สวยๆ มาตรฐานสากล"""
    
    ai_prompt = f"""
คุณเป็น Senior Mobile Developer & UI/UX Expert ที่สร้างแอปมือถือระดับมาตรฐานสากล

User Request: {prompt}

🎯 สร้าง mobile app ระดับ Production-Ready:

1. 🧠 วิเคราะห์ความต้องการและเลือก UI Library ที่เหมาะสม
2. 🎨 ใช้ Modern Design System (Material Design 3 หรือ iOS Design Guidelines) 
3. 📱 เขียนโค้ดที่ทำงานได้จริง พร้อม Navigation & State Management
4. ⚡ Performance Optimization และ Smooth Animations
5. 🔒 Security Best Practices และ Error Handling

✨ Modern Tech Stack ที่ใช้:
- React Native 0.73+ with TypeScript
- React Navigation 6 (smooth transitions)
- React Native Reanimated 3 (60fps animations)  
- React Native Gesture Handler
- Zustand (lightweight state management)
- React Hook Form (performance forms)
- React Query (smart data fetching)
- NativeBase/UI Kitten (beautiful components)
- Lottie (premium animations)
- React Native Vector Icons (Feather, Material)

🎨 UI/UX Standards:
- Modern color palette (gradients, glassmorphism)
- Inter/SF Pro typography hierarchy
- 8px grid system
- 44px minimum touch targets (iOS HIG)
- Material Design elevation & shadows
- Consistent spacing (4, 8, 16, 24, 32, 48px)
- Dark/Light mode support

JSON Response Format:
{{
    "app_name": "ชื่อแอป (professional naming)",
    "description": "คำอธิบายแอปแบบ professional", 
    "design_system": {{
        "primary_color": "#6366f1",
        "secondary_color": "#f59e0b", 
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "typography": "SF Pro Display, Inter",
        "ui_library": "NativeBase|UI Kitten|Tamagui"
    }},
    "package_json": {{
        "name": "app-name",
        "version": "1.0.0",
        "dependencies": {{
            "react": "18.2.0",
            "react-native": "0.73.2",
            "@react-navigation/native": "^6.1.9",
            "@react-navigation/stack": "^6.3.20", 
            "react-native-reanimated": "^3.6.0",
            "react-native-gesture-handler": "^2.14.0",
            "zustand": "^4.4.7",
            "react-hook-form": "^7.48.2",
            "@tanstack/react-query": "^5.8.4",
            "native-base": "^3.4.28",
            "react-native-vector-icons": "^10.0.2",
            "lottie-react-native": "^6.4.1"
        }}
    }},
    "main_component": "โค้ด App.tsx พร้อม Navigation & Theme Provider",
    "additional_files": [
        {{"filename": "src/screens/HomeScreen.tsx", "content": "หน้า Home พร้อม modern UI"}},
        {{"filename": "src/components/ui/Button.tsx", "content": "Custom Button component"}},
        {{"filename": "src/components/ui/Card.tsx", "content": "Modern Card component"}},
        {{"filename": "src/theme/colors.ts", "content": "Color palette & design tokens"}},
        {{"filename": "src/theme/typography.ts", "content": "Typography scale"}},
        {{"filename": "src/navigation/AppNavigator.tsx", "content": "Navigation setup"}},
        {{"filename": "src/store/useAppStore.ts", "content": "Zustand store"}},
        {{"filename": "src/utils/animations.ts", "content": "Reanimated helpers"}}
    ],
    "features": ["ฟีเจอร์หลักที่สร้าง"],
    "ui_highlights": ["จุดเด่นของ UI/UX"]
}}

💎 Code Quality Requirements:
- TypeScript strict mode
- ESLint + Prettier configuration  
- Proper error boundaries
- Loading & empty states
- Accessibility (a11y) support
- Performance monitoring ready
- Clean architecture (hooks, services, utils)
- Professional comments ภาษาไทย
- ใส่ comments เป็นไทย
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "คุณเป็น expert mobile developer ที่สร้างแอปจริง ตอบเป็น JSON เท่านั้น"},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=3500,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Parse JSON - แก้ไข trailing commas และ JSON format
        if ai_response.startswith('```json'):
            ai_response = ai_response.replace('```json', '').replace('```', '').strip()
        elif ai_response.startswith('```'):
            ai_response = ai_response.replace('```', '').strip()
        
        # แก้ไข trailing commas ใน JSON
        import re
        # ลบ trailing comma ก่อน } หรือ ]
        ai_response = re.sub(r',(\s*[}\]])', r'\1', ai_response)
        
        try:
            app_data = json.loads(ai_response)
        except json.JSONDecodeError as e:
            # ถ้า JSON ยังไม่ถูกต้อง ลองแก้ไขเพิ่มเติม
            print(f"JSON Parse Error: {e}")
            print(f"Response: {ai_response[:500]}...")
            
            # พยายามหา JSON object ใน response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_part = ai_response[json_start:json_end]
                # แก้ไข trailing commas อีกครั้ง
                json_part = re.sub(r',(\s*[}\]])', r'\1', json_part)
                app_data = json.loads(json_part)
            else:
                raise e
        
        # สร้างโฟลเดอร์แอป
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        app_name = app_data.get('app_name', 'MobileApp').replace(' ', '_')
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

## การติดตั้งและรัน

```bash
npm install
npx react-native run-android
npx react-native run-ios
```

## ฟีเจอร์

- สร้างด้วย AI อัตโนมัติ
- ใช้ React Native + TypeScript
- ทำงานได้จริง (ไม่ใช่ mockup)
- Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        readme_file = app_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        files_created += 1
        
        return {
            'success': True,
            'app_name': app_data.get('app_name'),
            'description': app_data.get('description'),
            'app_path': str(app_dir),
            'app_url': f"/generated_apps/{app_dir.name}",
            'files_created': files_created,
            'code_preview': app_data.get('main_component', '')[:400] + "...",
            'message': f"✅ สร้าง {app_data.get('app_name')} สำเร็จ! ({files_created} ไฟล์)"
        }
        
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f"AI ตอบกลับในรูปแบบที่ไม่ถูกต้อง: {str(e)}",
            'message': "❌ AI ตอบกลับไม่ถูกต้อง กรุณาลองใหม่"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"❌ เกิดข้อผิดพลาด: {str(e)}"
        }

async def generate_web_app_real(prompt: str, framework: str = "react") -> Dict[str, Any]:
    """🚀 REAL Full-Stack App Generator - เหมือน Lovable.dev (Frontend + Backend + Database)"""
    
    ai_prompt = f"""
คุณเป็น Senior Full-Stack Developer ที่สร้าง PRODUCTION-READY Web Application ที่ใช้งานได้จริง 100%

User Request: {prompt}

🎯 สร้าง Full-Stack Application จริงๆ (ไม่ใช่ mockup):

**REQUIREMENTS (จำเป็น):**
1. 🗄️ **SQLite Database จริง** - สร้างตารางและข้อมูล
2. 🔧 **Python Flask/FastAPI Backend** - API endpoints ที่ทำงานได้
3. 💻 **Frontend ที่เชื่อมต่อ Backend** - เรียก API จริง
4. 🔐 **Authentication System** - Login/Register ทำงานได้
5. 📝 **CRUD Operations** - Create/Read/Update/Delete จริง
6. 💾 **Data Persistence** - บันทึกข้อมูลถาวร
7. 🎨 **Modern UI** - สวยงาม responsive

1. 🧠 วิเคราะห์ความต้องการและเลือก Tech Stack ที่ดีที่สุด
2. 🎨 ใช้ Modern Design System (Material Design 3, Fluent UI, หรือ Tailwind)
3. 💻 เขียน Clean Code พร้อม TypeScript & Best Practices
4. ⚡ Performance Optimization & SEO Ready
5. 🔐 Security & Accessibility Standards
6. 📱 Fully Responsive (Mobile-first approach)

✨ Modern Tech Stack Options:
- Next.js 14 + TypeScript (if SSR/SSG needed)
- Vite + React 18 + TypeScript (if SPA)
- Tailwind CSS 3 (utility-first CSS)
- Framer Motion (smooth animations)
- React Hook Form + Zod (type-safe forms)
- Zustand/Redux Toolkit (state management)
- React Query/SWR (data fetching)
- Radix UI/Headless UI (accessible components)
- Lucide React (beautiful icons)
- React Hot Toast (notifications)

🎨 UI Library Options:
- Shadcn/ui (modern, customizable)
- Chakra UI (simple, modular)
- Material-UI (Google Material Design)
- Ant Design (enterprise-class UI)
- Mantine (full-featured)
- NextUI (modern & beautiful)

🌈 Design Standards:
- Modern color palette (CSS custom properties)
- Inter/Poppins typography system
- 4px/8px grid system for spacing
- Consistent border-radius (4px, 8px, 12px, 16px)
- Proper elevation & shadows
- Dark/Light mode toggle
- Smooth micro-interactions
- Loading skeletons & empty states

JSON Response Format (Full-Stack Application จริง):
{{
    "app_name": "ชื่อแอป",
    "description": "คำอธิบายแอป", 
    "database_schema": {{
        "users": "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)",
        "products": "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT, image_url TEXT)",
        "orders": "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, quantity INTEGER, total REAL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"
    }},
    "backend_files": {{
        "main.py": "# Flask/FastAPI backend code ที่ใช้งานได้จริง\\nfrom flask import Flask, request, jsonify\\nfrom flask_cors import CORS\\nimport sqlite3...",
        "database.py": "# Database connection and operations\\nimport sqlite3\\ndef init_db():\\n    conn = sqlite3.connect('app.db')...",
        "auth.py": "# Authentication functions\\nimport hashlib\\ndef hash_password(password):\\n    return hashlib.sha256(password.encode()).hexdigest()...",
        "requirements.txt": "flask\\nflask-cors\\nsqlite3"
    }},
    "frontend_files": {{
        "index.html": "<!DOCTYPE html>...HTML ที่เชื่อมต่อกับ Backend API",
        "app.js": "// JavaScript ที่เรียก API จริง\\nconst API_BASE = 'http://localhost:5000';\\nasync function login(username, password){{...}}",
        "styles.css": "/* Modern CSS สวยงาม responsive */",
        "login.html": "<!DOCTYPE html>...หน้า Login ที่ทำงานได้",
        "dashboard.html": "<!DOCTYPE html>...หน้า Dashboard พร้อมข้อมูลจาก DB"
    }},
    "setup_instructions": [
        "1. pip install -r requirements.txt",
        "2. python database.py (สร้าง database)",
        "3. python main.py (เริ่ม backend server)",
        "4. เปิด index.html ใน browser",
        "5. ลองใช้งาน Login/Register"
    ],
    "api_endpoints": [
        "POST /api/register - สมัครสมาชิก",
        "POST /api/login - เข้าสู่ระบบ", 
        "GET /api/products - ดูสินค้า",
        "POST /api/orders - สั่งซื้อ",
        "GET /api/profile - โปรไฟล์ผู้ใช้"
    ],
    "features": ["Authentication", "CRUD Operations", "Database Integration", "REST API"],
    "database_type": "SQLite",
    "backend_framework": "Flask/FastAPI",
    "deployment_ready": true
}}

**CRITICAL**: สร้างแอปที่ใช้งานได้จริง 100% ไม่ใช่ mockup!

💎 Code Quality Requirements:
- TypeScript strict mode
- ESLint + Prettier + Husky
- Proper SEO meta tags
- Accessibility (WCAG 2.1 AA)
- Performance (Core Web Vitals optimized)
- Error boundaries & error handling  
- Loading states & skeletons
- Professional Thai comments

สร้าง web application ที่สมบูรณ์ตาม request โดย:
1. วิเคราะห์ความต้องการจาก prompt
2. สร้าง responsive web app
3. ใช้ modern CSS และ JavaScript
4. มี interactive features
5. ทำงานได้จริงไม่ใช่ static

ส่งกลับเป็น JSON format:
{{
    "app_name": "ชื่อเว็บไซต์ (สั้น ๆ)",
    "description": "คำอธิบาย",
    "index_html": "โค้ด HTML หลัก (ครบถ้วน มี title, meta tags)",
    "styles_css": "โค้ด CSS (สวยงาม responsive)",
    "script_js": "โค้ด JavaScript (interactive มี functions)"
}}

เว็บไซต์ต้อง:
- Responsive design
- Modern UI/UX
- Interactive features
- ทำงานได้จริงบน browser
- ใส่ comments เป็นไทย
- มี proper HTML structure
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "คุณเป็น expert web developer ที่สร้างเว็บไซต์จริง ตอบเป็น JSON เท่านั้น"},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=3500,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        if ai_response.startswith('```json'):
            ai_response = ai_response.replace('```json', '').replace('```', '').strip()
        elif ai_response.startswith('```'):
            ai_response = ai_response.replace('```', '').strip()
        
        # แก้ไข trailing commas ใน JSON
        import re
        ai_response = re.sub(r',(\s*[}\]])', r'\1', ai_response)
        
        try:
            web_data = json.loads(ai_response)
        except json.JSONDecodeError as e:
            print(f"Web JSON Parse Error: {e}")
            print(f"Web Response: {ai_response[:500]}...")
            
            # พยายามหา JSON object ใน response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_part = ai_response[json_start:json_end]
                json_part = re.sub(r',(\s*[}\]])', r'\1', json_part)
                web_data = json.loads(json_part)
            else:
                raise e
        
        # สร้างโฟลเดอร์ Full-Stack App
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        web_name = web_data.get('app_name', 'WebApp').replace(' ', '_')
        web_dir = WORKSPACE / f"{web_name}_{timestamp}"
        web_dir.mkdir(parents=True, exist_ok=True)
        
        files_created = 0
        
        # 🗄️ สร้าง Database Schema และ Initial Data
        if web_data.get('database_schema'):
            db_init_code = "import sqlite3\nimport os\n\ndef init_database():\n"
            db_init_code += "    conn = sqlite3.connect('app.db')\n    cursor = conn.cursor()\n\n"
            
            for table_name, schema in web_data['database_schema'].items():
                db_init_code += f"    cursor.execute('''{schema}''')\n"
            
            db_init_code += "\n    conn.commit()\n    conn.close()\n    print('✅ Database initialized!')\n\n"
            db_init_code += "if __name__ == '__main__':\n    init_database()\n"
            
            with open(web_dir / "database.py", 'w', encoding='utf-8') as f:
                f.write(db_init_code)
            files_created += 1
        
        # 🔧 สร้าง Backend Files (Python Flask/FastAPI)
        if web_data.get('backend_files'):
            for filename, content in web_data['backend_files'].items():
                with open(web_dir / filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_created += 1
        
        # 💻 สร้าง Frontend Files
        if web_data.get('frontend_files'):
            for filename, content in web_data['frontend_files'].items():
                with open(web_dir / filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_created += 1
        
        # 📋 สร้าง Setup Instructions
        if web_data.get('setup_instructions'):
            readme_content = f"# {web_data.get('app_name', 'Full-Stack App')}\n\n"
            readme_content += f"{web_data.get('description', '')}\n\n"
            readme_content += "## 🚀 Setup Instructions\n\n"
            
            for i, instruction in enumerate(web_data['setup_instructions'], 1):
                readme_content += f"{i}. {instruction}\n"
            
            readme_content += "\n## 📡 API Endpoints\n\n"
            if web_data.get('api_endpoints'):
                for endpoint in web_data['api_endpoints']:
                    readme_content += f"- {endpoint}\n"
            
            readme_content += f"\n## ✨ Features\n\n"
            if web_data.get('features'):
                for feature in web_data['features']:
                    readme_content += f"- {feature}\n"
            
            readme_content += f"\n## 🛠️ Tech Stack\n\n"
            readme_content += f"- Backend: {web_data.get('backend_framework', 'Flask')}\n"
            readme_content += f"- Database: {web_data.get('database_type', 'SQLite')}\n"
            readme_content += f"- Frontend: HTML5 + CSS3 + JavaScript\n"
            
            with open(web_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
            files_created += 1
        
        # 🚀 สร้าง Auto-Start Script
        startup_script = f'''@echo off
echo 🚀 Starting {web_data.get('app_name', 'Full-Stack App')}...

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🗄️ Initializing database...
python database.py

echo 🔧 Starting backend server...
start "Backend Server" python main.py

echo ⏱️ Waiting for server to start...
timeout /t 3

echo 🌐 Opening app in browser...
start "" http://localhost:5000

echo ✅ App is running!
echo Backend: http://localhost:5000
echo Frontend: Open index.html or visit backend URL
pause
'''
        
        with open(web_dir / "start_app.bat", 'w', encoding='utf-8') as f:
            f.write(startup_script)
        files_created += 1
        
        return {
            'success': True,
            'app_name': web_data.get('app_name'),
            'description': web_data.get('description'),
            'app_path': str(web_dir),
            'app_url': f"/generated_apps/{web_dir.name}/index.html",
            'files_created': files_created,
            'code_preview': web_data.get('index_html', '')[:400] + "...",
            'message': f"✅ สร้าง {web_data.get('app_name')} เว็บไซต์สำเร็จ! ({files_created} ไฟล์)"
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"❌ เกิดข้อผิดพลาดสร้างเว็บไซต์: {str(e)}"
        }

# API Endpoints
@app.get("/")
async def serve_chat_interface():
    """Serve the chat interface"""
    chat_file = Path("C:/agent/ai_chat_interface.html")
    if chat_file.exists():
        return FileResponse(chat_file)
    else:
        return HTMLResponse("<h1>Chat interface not found</h1>", status_code=404)

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "message": "🤖 AI Chat Backend พร้อมทำงาน!",
        "timestamp": datetime.now().isoformat(),
        "workspace": str(WORKSPACE),
        "openai_available": bool(API_KEY)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """🧠 AI Expert Consultant - ปรึกษา แนะนำ แก้ไข ออกแบบ"""
    
    try:
        print(f"🎯 Expert Consultation Request: {request.message}")
        
        # Step 1: AI Expert Consultation & Analysis (ถามเสมอสำหรับโครงการใหม่)
        print("🧠 AI Expert Consultant analyzing...")
        consultation = await ai_expert_consultant(request.message, "analyze")
        
        # Force consultation for project creation requests
        project_keywords = ["สร้าง", "ทำ", "app", "เว็บ", "แอป", "website", "mobile", "ระบบ"]
        is_project_request = any(keyword in request.message.lower() for keyword in project_keywords)
        
        print(f"🔍 Project Request Detection: {is_project_request}")
        print(f"🤔 Needs More Info: {consultation.get('needs_more_info', False)}")
        
        # ALWAYS ask questions for project requests (แก้ปัญหาการสร้างทันที)
        if is_project_request or consultation.get("needs_more_info", False):
            return ChatResponse(
                success=True,
                message="🤔 <strong>AI Expert ต้องการข้อมูลเพิ่มเติม</strong><br>เพื่อสร้างโครงการที่ตรงใจคุณที่สุด",
                ai_consultation=consultation,
                needs_more_info=True
            )
        
        # Check if this is a general question/recommendation request
        if consultation.get("consultation_type") == "recommendation":
            expert_advice = consultation.get("expert_recommendations", [])
            code_suggestions = consultation.get("code_suggestions", {})
            
            advice_message = "🧠 <strong>AI Expert Consultant คำแนะนำ:</strong><br><br>"
            
            if expert_advice:
                advice_message += "💡 <strong>คำแนะนำจากผู้เชียวชาญ:</strong><br>"
                for advice in expert_advice:
                    advice_message += f"• {advice}<br>"
                advice_message += "<br>"
            
            if code_suggestions.get("best_practices"):
                advice_message += "⭐ <strong>Best Practices:</strong><br>"
                for practice in code_suggestions["best_practices"]:
                    advice_message += f"• {practice}<br>"
                advice_message += "<br>"
            
            if code_suggestions.get("improvements"):
                advice_message += "🔧 <strong>การปรับปรุง Code:</strong><br>"
                for improvement in code_suggestions["improvements"]:
                    advice_message += f"• {improvement}<br>"
                advice_message += "<br>"
            
            # Add modern libraries recommendation
            if consultation.get("expert_analysis", {}).get("modern_libraries"):
                advice_message += "📚 <strong>Modern Libraries แนะนำ:</strong><br>"
                for lib in consultation["expert_analysis"]["modern_libraries"][:5]:
                    advice_message += f"• {lib}<br>"
                advice_message += "<br>"
            
            advice_message += "✨ พร้อมช่วยสร้างแอป/เว็บไซต์ หรือตอบคำถามเพิ่มเติม!"
            
            return ChatResponse(
                success=True,
                message=advice_message,
                ai_consultation=consultation
            )
        
        # If ready to build, proceed with generation
        if consultation.get("ready_to_build", False):
            detected_type = consultation.get("expert_analysis", {}).get("project_type", "web_app")
            recommended_tech = consultation.get("expert_analysis", {}).get("recommended_tech_stack", {})
            
            print(f"🎯 AI Expert Decision: {detected_type} | Tech Stack: {recommended_tech}")
            
            # Improved project type detection (แก้ปัญหาสร้างผิดประเภท)
            msg_lower = request.message.lower()
            
            # Force correct type based on user keywords (แก้ปัญหา app = mobile)
            if any(keyword in msg_lower for keyword in ["แอปมือถือ", "mobile app", "มือถือ", "ios", "android"]):
                final_type = "mobile"  
                print("🔧 Force corrected to: MOBILE")
            else:
                # Default เป็น WEB เสมอ เพราะต้องการ Full-Stack App
                final_type = "web"
                print("🔧 Default to: WEB (Full-Stack App)")
                
            final_framework = "react"  # ใช้ web framework เสมอ
            
            # Step 2: Generate app with expert recommendations
            if final_type == "mobile":
                result = await generate_mobile_app_real(request.message, final_framework)
            else:
                result = await generate_web_app_real(request.message, final_framework)
                
            # Add expert analysis to result
            result['ai_expert_analysis'] = consultation
            result['tech_stack_reasoning'] = consultation.get("expert_analysis", {})
            
        else:
            return ChatResponse(
                success=False,
                message="❌ AI Expert ไม่สามารถตัดสินใจได้ กรุณาให้ข้อมูลเพิ่มเติม",
                ai_consultation=consultation
            )
        
        # Add AI analysis info to result
        if consultation:
            result['ai_analysis'] = {
                'detected_type': consultation.get('expert_analysis', {}).get('project_type'),
                'confidence': consultation.get('confidence', 0.9),
                'reasoning': consultation.get('expert_analysis', {}).get('reasoning', ''),
                'tech_stack': consultation.get('expert_analysis', {}).get('recommended_tech_stack', {}),
                'modern_libraries': consultation.get('expert_analysis', {}).get('modern_libraries', []),
                'design_system': consultation.get('expert_analysis', {}).get('design_system', {})
            }
        
        return ChatResponse(**result)
        
    except Exception as e:
        return ChatResponse(
            success=False,
            message=f"❌ เกิดข้อผิดพลาด: {str(e)}",
            error=str(e)
        )

@app.get("/apps")
async def list_generated_apps():
    """แสดงรายการแอปที่สร้างแล้ว"""
    
    apps = []
    for app_dir in WORKSPACE.iterdir():
        if app_dir.is_dir():
            files = [f.name for f in app_dir.iterdir() if f.is_file()]
            apps.append({
                "name": app_dir.name,
                "path": str(app_dir),
                "url": f"/generated_apps/{app_dir.name}",
                "files": files,
                "created": datetime.fromtimestamp(app_dir.stat().st_ctime).isoformat()
            })
    
    return {"apps": apps, "total": len(apps)}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting AI Chat Backend...")
    print(f"📁 Workspace: {WORKSPACE}")
    print(f"🔑 OpenAI API: {'✅' if API_KEY else '❌'}")
    print("💬 Chat Interface: http://localhost:8001")
    print("📊 API Documentation: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")