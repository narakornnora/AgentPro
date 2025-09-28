#!/usr/bin/env python3
"""
🚀 Lovable Clone - AI App Generator
สร้างแอปจริงจาก Chat เหมือน Lovable.dev
"""
import os
import json
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from openai import OpenAI

# Configuration
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY") or "test-key"
print(f"🔑 API Key: {'✅ Found' if API_KEY != 'test-key' else '❌ Not found - using test mode'}")

try:
    client = OpenAI(api_key=API_KEY) if API_KEY != "test-key" else None
    print("🤖 OpenAI client initialized")
except Exception as e:
    print(f"⚠️ OpenAI client error: {e}")
    client = None
ROOT_DIR = Path("C:/agent")
GENERATED_DIR = ROOT_DIR / "generated_apps"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI App
app = FastAPI(title="Lovable Clone", description="🚀 AI App Generator like Lovable.dev")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

# Active sessions and connections
active_sessions = {}
websocket_connections = {}

class LovableAI:
    """AI Engine เหมือน Lovable.dev"""
    
    def __init__(self):
        self.sessions = {}
    
    async def chat(self, message: str, session_id: str) -> Dict[str, Any]:
        """แชทกับ AI และตัดสินใจจะสร้างแอปหรือถามต่อ"""
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'messages': [],
                'requirements': {},
                'status': 'chatting'
            }
        
        session = self.sessions[session_id]
        session['messages'].append({"role": "user", "content": message})
        
        # ใช้ OpenAI ตัดสินใจว่าจะทำอะไรต่อ
        decision = await self._ai_decide_next_action(session)
        
        if decision['action'] == 'build_app':
            # เริ่มสร้างแอป
            session['status'] = 'building'
            return {
                'type': 'start_building',
                'message': decision['message'],
                'requirements': decision['requirements']
            }
        else:
            # ถามคำถามต่อ
            session['messages'].append({"role": "assistant", "content": decision['message']})
            return {
                'type': 'question',
                'message': decision['message'],
                'confidence': decision.get('confidence', 0.5)
            }
    
    async def _ai_decide_next_action(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """AI ตัดสินใจว่าจะสร้างแอปหรือถามต่อ"""
        
        conversation = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in session['messages'][-10:]  # เอา 10 messages ล่าสุด
        ])
        
        # ถ้าไม่มี OpenAI API ใช้ logic แบบง่าย
        if not client:
            return self._simple_decision_logic(conversation)
        
        prompt = f"""
คุณเป็น AI ของ Lovable.dev ที่ฉลาดมาก

บทสนทนา:
{conversation}

ตัดสินใจ:
1. ถ้าข้อมูลพอสร้างแอปได้แล้ว ให้ action = "build_app"
2. ถ้าต้องถามเพิ่ม ให้ action = "ask_question"

กฎ:
- คำถามสั้น กระชับ ทีละเรื่อง
- ถามแค่สิ่งจำเป็นจริงๆ
- อย่าถามมาก ให้เริ่มสร้างแอปเร็วๆ

ตอบเป็น JSON:
{{
    "action": "build_app" หรือ "ask_question",
    "message": "ข้อความตอบกลับ",
    "confidence": 0.8,
    "requirements": {{
        "app_type": "...",
        "features": [...],
        "description": "..."
    }}
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Clean JSON
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:-3].strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response[3:-3].strip()
            
            return json.loads(ai_response)
            
        except Exception as e:
            print(f"AI decision error: {e}")
            return self._simple_decision_logic(conversation)
    
    def _simple_decision_logic(self, conversation: str) -> Dict[str, Any]:
        """Logic ง่ายๆ เมื่อไม่มี OpenAI API"""
        
        # นับจำนวน message
        message_count = conversation.count("user:")
        
        # ถ้ามี message มากกว่า 2 ข้อ ให้สร้างแอป
        if message_count >= 2:
            return {
                "action": "build_app",
                "message": "เริ่มสร้างแอปตามที่คุณต้องการเลย! 🚀",
                "confidence": 0.8,
                "requirements": {
                    "app_type": "web_app",
                    "features": ["basic_crud", "responsive_ui"],
                    "description": "แอปเว็บพื้นฐานตามความต้องการ"
                }
            }
        
        # ถ้า message น้อย ให้ถามเพิ่ม
        questions = [
            "อยากได้ฟีเจอร์อะไรเพิ่มเติมไหมครับ?",
            "ต้องการฟังก์ชั่นพิเศษอะไรไหม?",
            "มีข้อมูลเพิ่มเติมที่อยากบอกไหม?"
        ]
        
        return {
            "action": "ask_question",
            "message": questions[message_count % len(questions)],
            "confidence": 0.6
        }
    
    async def build_app(self, requirements: Dict[str, Any], session_id: str, websocket: WebSocket = None) -> Dict[str, Any]:
        """สร้างแอปจริงเหมือน Lovable.dev"""
        
        app_id = f"app_{uuid.uuid4().hex[:8]}"
        app_dir = GENERATED_DIR / app_id
        app_dir.mkdir(exist_ok=True)
        
        try:
            # ส่งสถานะผ่าน WebSocket
            await self._send_status(websocket, "🎯 วิเคราะห์ความต้องการ...")
            
            # 1. AI วิเคราะห์และวางแผน
            plan = await self._ai_analyze_and_plan(requirements)
            
            await self._send_status(websocket, "🗄️ สร้างฐานข้อมูล...")
            
            # 2. สร้างฐานข้อมูล
            database_result = await self._ai_create_database(plan, app_dir, websocket)
            
            await self._send_status(websocket, "🔧 สร้าง Backend API...")
            
            # 3. สร้าง Backend
            backend_result = await self._ai_create_backend(plan, app_dir, websocket)
            
            await self._send_status(websocket, "🎨 สร้าง Frontend...")
            
            # 4. สร้าง Frontend
            frontend_result = await self._ai_create_frontend(plan, app_dir, websocket)
            
            await self._send_status(websocket, "📦 สร้างไฟล์เสริม...")
            
            # 5. สร้างไฟล์เสริม
            extras_result = await self._ai_create_extras(plan, app_dir)
            
            await self._send_status(websocket, "✅ แอปสร้างเสร็จแล้ว!")
            
            return {
                'app_id': app_id,
                'app_path': str(app_dir),
                'plan': plan,
                'files_created': (
                    database_result.get('files', []) +
                    backend_result.get('files', []) +
                    frontend_result.get('files', []) +
                    extras_result.get('files', [])
                ),
                'status': 'completed'
            }
            
        except Exception as e:
            await self._send_status(websocket, f"❌ เกิดข้อผิดพลาด: {str(e)}")
            raise
    
    async def _send_status(self, websocket: WebSocket, status: str):
        """ส่งสถานะผ่าน WebSocket"""
        if websocket:
            try:
                await websocket.send_json({
                    'type': 'status_update',
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                })
            except:
                pass
    
    async def _send_file_created(self, websocket: WebSocket, filename: str, content: str, file_path: str):
        """ส่งข้อมูลไฟล์ที่สร้างผ่าน WebSocket"""
        if websocket:
            try:
                await websocket.send_json({
                    'type': 'file_created',
                    'filename': filename,
                    'content': content[:5000],  # ส่งแค่ 5000 ตัวอักษรแรก
                    'filePath': file_path,
                    'timestamp': datetime.now().isoformat()
                })
            except:
                pass
    
    async def _send_code_preview(self, websocket: WebSocket, filename: str, content: str):
        """ส่ง code preview ผ่าน WebSocket"""
        if websocket:
            try:
                await websocket.send_json({
                    'type': 'code_preview',
                    'filename': filename,
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                })
            except:
                pass
    
    async def _ai_analyze_and_plan(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """AI วิเคราะห์และวางแผนแอป"""
        
        # ถ้าไม่มี OpenAI API ใช้ template พร้อมสร้าง
        if not client:
            return self._get_default_plan(requirements)
        
        prompt = f"""
คุณเป็น Senior Software Architect ที่เก่งมาก

ความต้องการ:
{json.dumps(requirements, ensure_ascii=False, indent=2)}

วิเคราะห์และวางแผนแอปที่สมบูรณ์:

ตอบเป็น JSON:
{{
    "app_name": "ชื่อแอปที่สร้างสรรค์",
    "description": "คำอธิบายแอป",
    "tech_stack": {{
        "database": "sqlite",
        "backend": "flask",
        "frontend": "html_css_js"
    }},
    "database_schema": [
        {{
            "table": "users",
            "fields": [
                {{"name": "id", "type": "INTEGER PRIMARY KEY"}},
                {{"name": "username", "type": "TEXT UNIQUE NOT NULL"}}
            ]
        }}
    ],
    "api_endpoints": [
        {{
            "method": "GET",
            "path": "/api/users",
            "description": "ดึงรายการผู้ใช้"
        }}
    ],
    "pages": [
        {{
            "name": "index.html",
            "description": "หน้าแรก",
            "components": ["header", "main_content", "footer"]
        }}
    ]
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content.strip()
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:-3].strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response[3:-3].strip()
            
            return json.loads(ai_response)
        except Exception as e:
            print(f"AI planning error: {e}")
            return self._get_default_plan(requirements)
    
    def _get_default_plan(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """แผนเริ่มต้นเมื่อไม่มี OpenAI API"""
        return {
            "app_name": "แอปใหม่",
            "description": requirements.get('description', 'แอปเว็บสำหรับจัดการข้อมูล'),
            "tech_stack": {
                "database": "sqlite",
                "backend": "flask", 
                "frontend": "html_css_js"
            },
            "database_schema": [
                {
                    "table": "items",
                    "fields": [
                        {"name": "id", "type": "INTEGER PRIMARY KEY"},
                        {"name": "name", "type": "TEXT NOT NULL"},
                        {"name": "description", "type": "TEXT"},
                        {"name": "created_at", "type": "DATETIME DEFAULT CURRENT_TIMESTAMP"}
                    ]
                }
            ],
            "api_endpoints": [
                {"method": "GET", "path": "/api/items", "description": "ดึงรายการข้อมูล"},
                {"method": "POST", "path": "/api/items", "description": "เพิ่มข้อมูลใหม่"},
                {"method": "PUT", "path": "/api/items/<id>", "description": "แก้ไขข้อมูล"},
                {"method": "DELETE", "path": "/api/items/<id>", "description": "ลบข้อมูล"}
            ],
            "pages": [
                {
                    "name": "index.html",
                    "description": "หน้าแรก",
                    "components": ["header", "item_list", "add_form", "footer"]
                }
            ]
        }
    
    async def _ai_create_database(self, plan: Dict[str, Any], app_dir: Path, websocket: WebSocket = None) -> Dict[str, Any]:
        """AI สร้างฐานข้อมูล"""
        
        # ถ้าไม่มี OpenAI API ใช้ template
        if not client:
            code = self._get_default_database_code(plan)
        else:
            prompt = f"""
สร้างโค้ด Python สำหรับ SQLite database ตาม schema:

{json.dumps(plan.get('database_schema', []), ensure_ascii=False, indent=2)}

ให้โค้ดที่:
1. สร้างตารางทั้งหมด
2. เพิ่มข้อมูลตัวอย่าง
3. ใช้งานได้จริง

ตอบเป็น Python code เท่านั้น
"""
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.2
                )
                
                code = response.choices[0].message.content.strip()
                if code.startswith('```python'):
                    code = code[9:-3].strip()
                elif code.startswith('```'):
                    code = code[3:-3].strip()
            except Exception as e:
                print(f"AI database creation error: {e}")
                code = self._get_default_database_code(plan)
        
        # บันทึกไฟล์
        db_file = app_dir / "database.py"
        with open(db_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # ส่งข้อมูลไฟล์ที่สร้าง
        await self._send_file_created(websocket, "database.py", code, str(db_file))
        
        return {'files': ['database.py'], 'code': code}
    
    def _get_default_database_code(self, plan: Dict[str, Any]) -> str:
        """Database code เริ่มต้น"""
        return '''import sqlite3
import os

def init_database():
    """สร้างฐานข้อมูลและตารางพื้นฐาน"""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # สร้างตาราง items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # เพิ่มข้อมูลตัวอย่าง
    sample_data = [
        ('สินค้า 1', 'รายละเอียดสินค้า 1'),
        ('สินค้า 2', 'รายละเอียดสินค้า 2'),
        ('สินค้า 3', 'รายละเอียดสินค้า 3')
    ]
    
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            sample_data
        )
    
    conn.commit()
    conn.close()
    print("✅ ฐานข้อมูลสร้างเรียบร้อย!")

if __name__ == "__main__":
    init_database()
'''
    
    async def _ai_create_backend(self, plan: Dict[str, Any], app_dir: Path, websocket: WebSocket = None) -> Dict[str, Any]:
        """AI สร้าง Backend API"""
        
        prompt = f"""
สร้าง Flask backend สำหรับแอป: {plan.get('app_name')}

API endpoints ที่ต้องมี:
{json.dumps(plan.get('api_endpoints', []), ensure_ascii=False, indent=2)}

Database schema:
{json.dumps(plan.get('database_schema', []), ensure_ascii=False, indent=2)}

ให้โค้ด Flask ที่:
1. มี API endpoints ครบ
2. เชื่อมต่อ SQLite database
3. มี CORS support
4. ใช้งานได้จริง

ตอบเป็น Python code เท่านั้น
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500,
            temperature=0.2
        )
        
        code = response.choices[0].message.content.strip()
        if code.startswith('```python'):
            code = code[9:-3].strip()
        elif code.startswith('```'):
            code = code[3:-3].strip()
        
        # บันทึกไฟล์
        app_file = app_dir / "app.py"
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # ส่งข้อมูลไฟล์ที่สร้าง
        await self._send_file_created(websocket, "app.py", code, str(app_file))
        
        return {'files': ['app.py'], 'code': code}
    
    async def _ai_create_frontend(self, plan: Dict[str, Any], app_dir: Path, websocket: WebSocket = None) -> Dict[str, Any]:
        """AI สร้าง Frontend"""
        
        files_created = []
        
        # สร้าง templates และ static directories
        templates_dir = app_dir / "templates"
        static_dir = app_dir / "static"
        templates_dir.mkdir(exist_ok=True)
        static_dir.mkdir(exist_ok=True)
        
        # สร้าง HTML
        html_prompt = f"""
สร้าง HTML สำหรับแอป: {plan.get('app_name')}

หน้าที่ต้องมี:
{json.dumps(plan.get('pages', []), ensure_ascii=False, indent=2)}

ให้ HTML ที่:
1. สวยงาม responsive
2. เชื่อมต่อ API
3. ใช้งานได้จริง
4. มี CSS และ JavaScript

ตอบเป็น HTML code เท่านั้น
"""
        
        html_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": html_prompt}],
            max_tokens=2000,
            temperature=0.3
        )
        
        html_code = html_response.choices[0].message.content.strip()
        if html_code.startswith('```html'):
            html_code = html_code[7:-3].strip()
        elif html_code.startswith('```'):
            html_code = html_code[3:-3].strip()
        
        # บันทึก HTML
        html_file = templates_dir / "index.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_code)
        files_created.append('templates/index.html')
        
        # ส่งข้อมูลไฟล์ HTML ที่สร้าง
        await self._send_file_created(websocket, "index.html", html_code, str(html_file))
        
        # สร้าง CSS
        css_prompt = f"""
สร้าง CSS สำหรับแอป: {plan.get('app_name')}

ให้ CSS ที่:
1. สวยงาม modern
2. responsive
3. สีสันที่เข้ากับแอป
4. เอฟเฟกต์สวยๆ

ตอบเป็น CSS code เท่านั้น
"""
        
        css_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": css_prompt}],
            max_tokens=1500,
            temperature=0.4
        )
        
        css_code = css_response.choices[0].message.content.strip()
        if css_code.startswith('```css'):
            css_code = css_code[6:-3].strip()
        elif css_code.startswith('```'):
            css_code = css_code[3:-3].strip()
        
        # บันทึก CSS
        css_file = static_dir / "style.css"
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_code)
        files_created.append('static/style.css')
        
        # ส่งข้อมูลไฟล์ CSS ที่สร้าง
        await self._send_file_created(websocket, "style.css", css_code, str(css_file))
        
        # สร้าง JavaScript
        js_prompt = f"""
สร้าง JavaScript สำหรับแอป: {plan.get('app_name')}

API endpoints:
{json.dumps(plan.get('api_endpoints', []), ensure_ascii=False, indent=2)}

ให้ JavaScript ที่:
1. เชื่อมต่อ API
2. จัดการ UI interactions
3. ใช้งานได้จริง

ตอบเป็น JavaScript code เท่านั้น
"""
        
        js_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": js_prompt}],
            max_tokens=1500,
            temperature=0.3
        )
        
        js_code = js_response.choices[0].message.content.strip()
        if js_code.startswith('```javascript'):
            js_code = js_code[13:-3].strip()
        elif js_code.startswith('```'):
            js_code = js_code[3:-3].strip()
        
        # บันทึก JavaScript
        js_file = static_dir / "app.js"
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_code)
        files_created.append('static/app.js')
        
        # ส่งข้อมูลไฟล์ JS ที่สร้าง
        await self._send_file_created(websocket, "app.js", js_code, str(js_file))
        
        return {'files': files_created}
    
    async def _ai_create_extras(self, plan: Dict[str, Any], app_dir: Path) -> Dict[str, Any]:
        """สร้างไฟล์เสริม"""
        
        files_created = []
        
        # สร้าง requirements.txt
        requirements_content = """flask
flask-cors
"""
        req_file = app_dir / "requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        files_created.append('requirements.txt')
        
        # สร้าง start.bat
        start_content = f"""@echo off
echo Starting {plan.get('app_name', 'App')}...
python database.py
python app.py
"""
        start_file = app_dir / "start.bat"
        with open(start_file, 'w', encoding='utf-8') as f:
            f.write(start_content)
        files_created.append('start.bat')
        
        # สร้าง README.md
        readme_content = f"""# {plan.get('app_name', 'Generated App')}

{plan.get('description', 'แอปที่สร้างด้วย AI')}

## วิธีรัน

1. ติดตั้ง dependencies:
   ```
   pip install -r requirements.txt
   ```

2. รันแอป:
   ```
   start.bat
   ```

3. เปิดเบราเซอร์: http://localhost:5000

## สร้างด้วย Lovable Clone AI 🚀
"""
        readme_file = app_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        files_created.append('README.md')
        
        return {'files': files_created}


# Global AI instance
lovable_ai = LovableAI()


@app.get("/")
async def root():
    """Serve the main interface"""
    interface_file = ROOT_DIR / "lovable_split_interface.html"
    if interface_file.exists():
        return FileResponse(str(interface_file))
    return {"message": "🚀 Lovable Clone AI", "status": "ready"}


@app.post("/chat")
async def chat_endpoint(message_request: ChatMessage):
    """Chat with AI"""
    
    session_id = message_request.session_id or f"session_{uuid.uuid4().hex[:8]}"
    
    try:
        result = await lovable_ai.chat(message_request.message, session_id)
        result['session_id'] = session_id
        return result
        
    except Exception as e:
        return {
            'type': 'error',
            'message': f"เกิดข้อผิดพลาด: {str(e)}",
            'session_id': session_id
        }


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket for real-time updates"""
    await websocket.accept()
    websocket_connections[session_id] = websocket
    
    try:
        while True:
            # รอรับ build request
            data = await websocket.receive_json()
            
            if data.get('action') == 'build_app':
                requirements = data.get('requirements', {})
                
                # สร้างแอปพร้อม real-time updates
                result = await lovable_ai.build_app(requirements, session_id, websocket)
                
                # ส่งผลลัพธ์สุดท้าย
                await websocket.send_json({
                    'type': 'app_completed',
                    'result': result
                })
    
    except WebSocketDisconnect:
        if session_id in websocket_connections:
            del websocket_connections[session_id]


@app.post("/build/{session_id}")
async def build_app_endpoint(session_id: str, background_tasks: BackgroundTasks):
    """Build app endpoint (backup for non-websocket)"""
    
    session = lovable_ai.sessions.get(session_id)
    if not session or session.get('status') != 'building':
        return {"error": "Session not ready for building"}
    
    # Extract requirements from session
    requirements = session.get('requirements', {})
    
    try:
        result = await lovable_ai.build_app(requirements, session_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/apps")
async def list_apps():
    """List generated apps"""
    apps = []
    for app_dir in GENERATED_DIR.iterdir():
        if app_dir.is_dir():
            readme = app_dir / "README.md"
            if readme.exists():
                apps.append({
                    'id': app_dir.name,
                    'path': str(app_dir),
                    'created': datetime.fromtimestamp(app_dir.stat().st_mtime).isoformat()
                })
    
    return {"apps": apps}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Lovable Clone AI...")
    print("💬 Chat to build apps instantly")
    print("📍 Server: http://localhost:8004")
    uvicorn.run(app, host="0.0.0.0", port=8004)