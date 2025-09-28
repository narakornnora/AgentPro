#!/usr/bin/env python3
"""
🚀 Full-Privilege AI Agent - เหมือน Lovable.dev แต่ไม่แพงและทำงานเต็มสิทธิ์
AI ทำงานในสภาพแวดล้อมจริง มีสิทธิ์เต็มในการสร้าง/แก้ไข/ลบ ไฟล์ DB Config Tests
"""
import os
import json
import asyncio
import re
import subprocess
import shutil
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
app = FastAPI(title="Real Full-Stack Generator", description="🚀 สร้างแอปจริงที่ใช้งานได้")

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
    app_type: str = "auto"
    framework: str = "auto"

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


async def generate_fullstack_app(prompt: str) -> Dict[str, Any]:
    """🚀 Full-Privilege AI Agent - สร้างแอปจริงด้วยสิทธิ์เต็ม"""
    
    ai_prompt = f"""
คุณเป็น Full-Privilege AI Agent ที่ทำงานในสภาพแวดล้อมจริง เหมือน Lovable.dev

User Request: {prompt}

🎯 สร้าง PRODUCTION-READY Application ที่ใช้งานได้จริง 100%:

**FULL PRIVILEGES - ทำได้ทุกอย่าง:**
1. 🗄️ สร้าง Database จริง - SQLite/PostgreSQL/MySQL 
2. 🔧 สร้าง Backend API - Flask/FastAPI/Django
3. 💻 สร้าง Frontend - React/Vue/Vanilla JS
4. 🔐 Authentication & Authorization - JWT/Session
5. 📝 CRUD Operations ครบถ้วน
6. 📦 Package Management - requirements.txt/package.json
7. 🔧 Configuration Files - .env/config.yaml
8. 🧪 Unit Tests - pytest/jest
9. 🚀 Deployment Scripts - Docker/Heroku/Vercel
10. 📚 Documentation - README/API docs
11. 🎨 Modern UI/UX - Tailwind/Bootstrap
12. 🔄 State Management - Redux/Vuex
13. 📊 Data Visualization - Charts.js/D3.js
14. 🔔 Real-time Features - WebSocket/SSE
15. 💳 Payment Integration - Stripe/PayPal (sandbox)
16. � Email System - SMTP/SendGrid
17. 🌐 Multi-language Support
18. 📱 Responsive Design
19. 🔍 SEO Optimization
20. ⚡ Performance Optimization

สร้าง JSON ที่ครบถ้วน Production-Ready:
{{
    "app_name": "ชื่อแอป",
    "description": "คำอธิบายแอป",
    "tech_stack": "React + Flask + SQLite + JWT",
    "features": ["Authentication", "CRUD Operations", "Real-time Updates", "Responsive Design"],
    
    "database_init": "# Production Database Setup\\nimport sqlite3\\nimport hashlib\\nfrom datetime import datetime\\n\\ndef init_db():\\n    conn = sqlite3.connect('app.db')\\n    cursor = conn.cursor()\\n    \\n    # Users table with proper schema\\n    cursor.execute('''CREATE TABLE IF NOT EXISTS users (\\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\\n        username TEXT UNIQUE NOT NULL,\\n        email TEXT UNIQUE NOT NULL,\\n        password_hash TEXT NOT NULL,\\n        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\\n        is_active BOOLEAN DEFAULT TRUE\\n    )''')\\n    \\n    # Add more tables based on app requirements\\n    conn.commit()\\n    conn.close()\\n    print('Database initialized successfully!')\\n\\nif __name__ == '__main__':\\n    init_db()",
    
    "backend_main": "# Production Flask Backend\\nfrom flask import Flask, request, jsonify, render_template, session\\nfrom flask_cors import CORS\\nfrom flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request\\nimport sqlite3\\nimport hashlib\\nimport os\\nfrom datetime import timedelta\\n\\napp = Flask(__name__)\\napp.config['SECRET_KEY'] = os.urandom(24)\\napp.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!\\napp.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)\\n\\njwt = JWTManager(app)\\nCORS(app, origins=['*'])\\n\\n# Database helper\\ndef get_db():\\n    conn = sqlite3.connect('app.db')\\n    conn.row_factory = sqlite3.Row\\n    return conn\\n\\n@app.route('/')\\ndef home():\\n    return render_template('index.html')\\n\\n@app.route('/api/register', methods=['POST'])\\ndef register():\\n    data = request.json\\n    username = data.get('username')\\n    email = data.get('email')\\n    password = data.get('password')\\n    \\n    if not username or not email or not password:\\n        return jsonify({'error': 'Missing required fields'}), 400\\n    \\n    # Hash password\\n    password_hash = hashlib.sha256(password.encode()).hexdigest()\\n    \\n    try:\\n        db = get_db()\\n        db.execute(\\n            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',\\n            (username, email, password_hash)\\n        )\\n        db.commit()\\n        db.close()\\n        \\n        # Create token\\n        token = create_access_token(identity=username)\\n        return jsonify({'success': True, 'token': token, 'username': username})\\n        \\n    except sqlite3.IntegrityError:\\n        return jsonify({'error': 'Username or email already exists'}), 400\\n\\n@app.route('/api/login', methods=['POST'])\\ndef login():\\n    data = request.json\\n    username = data.get('username')\\n    password = data.get('password')\\n    \\n    if not username or not password:\\n        return jsonify({'error': 'Missing credentials'}), 400\\n    \\n    password_hash = hashlib.sha256(password.encode()).hexdigest()\\n    \\n    db = get_db()\\n    user = db.execute(\\n        'SELECT * FROM users WHERE username = ? AND password_hash = ?',\\n        (username, password_hash)\\n    ).fetchone()\\n    db.close()\\n    \\n    if user:\\n        token = create_access_token(identity=username)\\n        return jsonify({'success': True, 'token': token, 'username': username})\\n    else:\\n        return jsonify({'error': 'Invalid credentials'}), 401\\n\\nif __name__ == '__main__':\\n    app.run(debug=True, port=5000)",
    
    "frontend_html": "<!DOCTYPE html>\\n<html lang='th'>\\n<head>\\n    <meta charset='UTF-8'>\\n    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\\n    <title>{{APP_NAME}}</title>\\n    <script src='https://cdn.tailwindcss.com'></script>\\n    <script src='https://unpkg.com/react@18/umd/react.production.min.js'></script>\\n    <script src='https://unpkg.com/react-dom@18/umd/react-dom.production.min.js'></script>\\n    <script src='https://unpkg.com/@babel/standalone/babel.min.js'></script>\\n    <link href='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' rel='stylesheet'>\\n</head>\\n<body class='font-inter bg-gray-50 min-h-screen'>\\n    <div id='root'></div>\\n    <script type='text/babel' src='app.js'></script>\\n</body>\\n</html>",
    
    "frontend_js": "// Modern React App with Authentication\\nconst {{ useState, useEffect }} = React;\\n\\nconst API_BASE = 'http://localhost:5000';\\n\\n// API helpers\\nconst api = {{\\n    async call(endpoint, options = {{}}) {{\\n        const token = localStorage.getItem('token');\\n        const headers = {{\\n            'Content-Type': 'application/json',\\n            ...(token && {{ Authorization: `Bearer ${{token}}` }})\\n        }};\\n        \\n        const response = await fetch(`${{API_BASE}}${{endpoint}}`, {{\\n            ...options,\\n            headers: {{ ...headers, ...options.headers }}\\n        }});\\n        \\n        return response.json();\\n    }},\\n    \\n    async register(username, email, password) {{\\n        return this.call('/api/register', {{\\n            method: 'POST',\\n            body: JSON.stringify({{ username, email, password }})\\n        }});\\n    }},\\n    \\n    async login(username, password) {{\\n        return this.call('/api/login', {{\\n            method: 'POST',\\n            body: JSON.stringify({{ username, password }})\\n        }});\\n    }}\\n}};\\n\\n// Main App Component\\nconst App = () => {{\\n    const [user, setUser] = useState(null);\\n    const [loading, setLoading] = useState(true);\\n    \\n    useEffect(() => {{\\n        const token = localStorage.getItem('token');\\n        const username = localStorage.getItem('username');\\n        if (token && username) {{\\n            setUser({{ username }});\\n        }}\\n        setLoading(false);\\n    }}, []);\\n    \\n    const handleLogin = async (username, password) => {{\\n        const result = await api.login(username, password);\\n        if (result.success) {{\\n            localStorage.setItem('token', result.token);\\n            localStorage.setItem('username', result.username);\\n            setUser({{ username: result.username }});\\n        }}\\n        return result;\\n    }};\\n    \\n    const handleLogout = () => {{\\n        localStorage.removeItem('token');\\n        localStorage.removeItem('username');\\n        setUser(null);\\n    }};\\n    \\n    if (loading) {{\\n        return <div className='flex justify-center items-center min-h-screen'>\\n            <div className='animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500'></div>\\n        </div>;\\n    }}\\n    \\n    return (\\n        <div className='min-h-screen bg-gray-50'>\\n            {{user ? (\\n                <Dashboard user={{user}} onLogout={{handleLogout}} />\\n            ) : (\\n                <AuthPage onLogin={{handleLogin}} />\\n            )}}\\n        </div>\\n    );\\n}};\\n\\n// Render App\\nReactDOM.render(<App />, document.getElementById('root'));",
    
    "requirements": "flask\\nflask-cors\\nflask-jwt-extended\\nsqlite3\\nrequests\\npython-dotenv\\ngunicorn",
    
    "package_json": "{{\\n  \\\"name\\\": \\\"{{APP_SLUG}}\\\",\\n  \\\"version\\\": \\\"1.0.0\\\",\\n  \\\"scripts\\\": {{\\n    \\\"dev\\\": \\\"python main.py\\\",\\n    \\\"start\\\": \\\"gunicorn main:app\\\",\\n    \\\"test\\\": \\\"pytest\\\",\\n    \\\"init-db\\\": \\\"python database.py\\\"\\n  }},\\n  \\\"dependencies\\\": {{\\n    \\\"react\\\": \\\"^18.0.0\\\",\\n    \\\"react-dom\\\": \\\"^18.0.0\\\"\\n  }}\\n}}",
    
    "dockerfile": "FROM python:3.9-slim\\nWORKDIR /app\\nCOPY requirements.txt .\\nRUN pip install -r requirements.txt\\nCOPY . .\\nEXPOSE 5000\\nCMD [\\\"gunicorn\\\", \\\"main:app\\\", \\\"--host=0.0.0.0\\\", \\\"--port=5000\\\"]",
    
    "env_example": "# Environment Variables\\nSECRET_KEY=your-secret-key-here\\nJWT_SECRET_KEY=your-jwt-secret\\nDATABASE_URL=sqlite:///app.db\\nENVIRONMENT=development",
    
    "tests": "# Unit Tests\\nimport pytest\\nimport json\\nfrom main import app\\n\\n@pytest.fixture\\ndef client():\\n    app.config['TESTING'] = True\\n    with app.test_client() as client:\\n        yield client\\n\\ndef test_register(client):\\n    response = client.post('/api/register', \\n        json={{'username': 'test', 'email': 'test@test.com', 'password': 'test123'}})\\n    assert response.status_code == 200\\n    data = json.loads(response.data)\\n    assert data['success'] == True",
    
    "start_script": "echo 🚀 Starting Production App...\\necho Installing Python dependencies...\\npip install -r requirements.txt\\necho Initializing database...\\npython database.py\\necho Starting development server...\\nstart python main.py\\necho ✅ App running at http://localhost:5000\\necho 📱 Ready for production deployment!",
    
    "deploy_script": "echo 🚀 Production Deployment\\necho Building Docker image...\\ndocker build -t {{APP_SLUG}} .\\necho Pushing to registry...\\n# docker push your-registry/{{APP_SLUG}}\\necho ✅ Deployment ready!",
    
    "readme": "# {{APP_NAME}}\\n\\n## 🚀 Production-Ready Features\\n\\n- ✅ Authentication & Authorization\\n- ✅ Database with proper schema\\n- ✅ RESTful API endpoints\\n- ✅ Modern React frontend\\n- ✅ Responsive design\\n- ✅ Unit tests\\n- ✅ Docker support\\n- ✅ Environment configuration\\n\\n## 🛠 Tech Stack\\n\\n- Backend: Flask + SQLite + JWT\\n- Frontend: React + Tailwind CSS\\n- Testing: Pytest\\n- Deployment: Docker + Gunicorn\\n\\n## 🚀 Quick Start\\n\\n1. **Development:**\\n   ```bash\\n   # Start development server\\n   start_app.bat\\n   # Or manually:\\n   pip install -r requirements.txt\\n   python database.py\\n   python main.py\\n   ```\\n\\n2. **Production:**\\n   ```bash\\n   docker build -t {{APP_SLUG}} .\\n   docker run -p 5000:5000 {{APP_SLUG}}\\n   ```\\n\\n## 📚 API Endpoints\\n\\n- POST `/api/register` - User registration\\n- POST `/api/login` - User login\\n- GET `/api/profile` - Get user profile\\n\\n## 🧪 Testing\\n\\n```bash\\npytest\\n```\\n\\nสร้างด้วย Full-Privilege AI Agent 🤖"
}}

**CRITICAL**: สร้างแอปที่ใช้งานได้จริง ไม่ใช่ mockup!
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "คุณเป็น expert full-stack developer ที่สร้างแอปจริง ตอบเป็น JSON เท่านั้น"},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=4000,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        print(f"🤖 AI Response: {ai_response[:200]}...")
        
        # Clean JSON
        if ai_response.startswith('```json'):
            ai_response = ai_response[7:-3].strip()
        elif ai_response.startswith('```'):
            ai_response = ai_response[3:-3].strip()
            
        # Fix trailing commas
        ai_response = re.sub(r',(\s*[}\]])', r'\\1', ai_response)
        
        app_data = json.loads(ai_response)
        
        # สร้างโฟลเดอร์แอป - Full Privilege Mode
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        app_name = app_data.get('app_name', 'FullStackApp').replace(' ', '_')
        app_slug = re.sub(r'[^a-zA-Z0-9_-]', '', app_name.lower())
        app_dir = WORKSPACE / f"{app_name}_{timestamp}"
        app_dir.mkdir(parents=True, exist_ok=True)
        
        # Create full directory structure
        (app_dir / "templates").mkdir(exist_ok=True)
        (app_dir / "static").mkdir(exist_ok=True)
        (app_dir / "static/css").mkdir(exist_ok=True)
        (app_dir / "static/js").mkdir(exist_ok=True)
        (app_dir / "tests").mkdir(exist_ok=True)
        (app_dir / "config").mkdir(exist_ok=True)
        
        files_created = 0
        
        # 🗄️ สร้าง Database
        if app_data.get('database_init'):
            with open(app_dir / "database.py", 'w', encoding='utf-8') as f:
                f.write(app_data['database_init'])
            files_created += 1
            print("✅ Created database.py")
        
        # 🔧 สร้าง Backend
        if app_data.get('backend_main'):
            # สร้าง templates folder
            templates_dir = app_dir / "templates"
            templates_dir.mkdir(exist_ok=True)
            
            with open(app_dir / "main.py", 'w', encoding='utf-8') as f:
                f.write(app_data['backend_main'])
            files_created += 1
            print("✅ Created main.py")
        
        # 💻 สร้าง Frontend
        if app_data.get('frontend_html'):
            with open(app_dir / "templates" / "index.html", 'w', encoding='utf-8') as f:
                f.write(app_data['frontend_html'])
            files_created += 1
            print("✅ Created index.html")
        
        if app_data.get('frontend_css'):
            static_dir = app_dir / "static"
            static_dir.mkdir(exist_ok=True)
            with open(static_dir / "styles.css", 'w', encoding='utf-8') as f:
                f.write(app_data['frontend_css'])
            files_created += 1
            print("✅ Created styles.css")
        
        if app_data.get('frontend_js'):
            static_dir = app_dir / "static"
            static_dir.mkdir(exist_ok=True)
            with open(static_dir / "app.js", 'w', encoding='utf-8') as f:
                f.write(app_data['frontend_js'])
            files_created += 1
            print("✅ Created app.js")
        
        # 📦 สร้าง Requirements
        if app_data.get('requirements'):
            with open(app_dir / "requirements.txt", 'w', encoding='utf-8') as f:
                f.write(app_data['requirements'])
            files_created += 1
        
        # 🚀 สร้าง Start Script
        if app_data.get('start_script'):
            with open(app_dir / "start_app.bat", 'w', encoding='utf-8') as f:
                f.write(app_data['start_script'])
            files_created += 1
        
        # 📖 สร้าง README
        readme_content = f"""# {app_data.get('app_name', 'Full-Stack App')}

{app_data.get('description', 'แอปพลิเคชันที่สร้างด้วย AI')}

## 🚀 วิธีรัน

1. ดับเบิลคลิก `start_app.bat`
2. รอจนกว่าจะขึ้น "Running on http://localhost:5000"
3. เปิด browser ไปที่ http://localhost:5000
4. ใช้งานแอปได้เลย!

## 📁 ไฟล์ที่สำคัญ

- `database.py` - สร้าง SQLite database
- `main.py` - Flask backend server
- `templates/index.html` - หน้าเว็บหลัก
- `static/styles.css` - CSS สไตล์
- `static/app.js` - JavaScript functionality

## ✨ ฟีเจอร์

- ✅ Database จริง (SQLite)
- ✅ Backend API (Flask)
- ✅ Frontend (HTML/CSS/JS)
- ✅ Authentication System
- ✅ CRUD Operations

สร้างด้วย AI Full-Stack Generator 🤖
"""
        
        with open(app_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        files_created += 1
        
        print(f"🎉 Created {files_created} files in {app_dir}")
        
        return {
            'success': True,
            'app_name': app_data.get('app_name'),
            'description': app_data.get('description'),
            'app_path': str(app_dir),
            'app_url': f"/generated_apps/{app_dir.name}",
            'files_created': files_created,
            'code_preview': app_data.get('backend_main', '')[:400] + "...",
            'message': f"✅ สร้าง {app_data.get('app_name')} สำเร็จ! ({files_created} ไฟล์)\\n\\n🚀 วิธีใช้:\\n1. เปิดโฟลเดอร์ที่สร้าง\\n2. ดับเบิลคลิก start_app.bat\\n3. เปิด http://localhost:5000"
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'message': f"❌ เกิดข้อผิดพลาด: {str(e)}"
        }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "message": "🚀 Real Full-Stack Generator พร้อมทำงาน!",
        "timestamp": datetime.now().isoformat(),
        "workspace": str(WORKSPACE),
        "openai_available": bool(API_KEY)
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """🚀 สร้าง Full-Stack Application จริงๆ"""
    
    try:
        print(f"🎯 Request: {request.message}")
        
        # สร้าง Full-Stack App เสมอ (ไม่เป็น mobile mockup)
        print("🚀 Generating Full-Stack App...")
        result = await generate_fullstack_app(request.message)
        
        return ChatResponse(**result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return ChatResponse(
            success=False,
            message=f"❌ เกิดข้อผิดพลาด: {str(e)}",
            error=str(e)
        )


@app.get("/apps")
async def list_generated_apps():
    """List generated apps"""
    apps = []
    for app_dir in WORKSPACE.iterdir():
        if app_dir.is_dir():
            readme_file = app_dir / "README.md"
            if readme_file.exists():
                apps.append({
                    "name": app_dir.name,
                    "path": str(app_dir),
                    "url": f"/generated_apps/{app_dir.name}",
                    "created": datetime.fromtimestamp(app_dir.stat().st_mtime).isoformat()
                })
    return {"apps": apps}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Real Full-Stack Generator...")
    print("📍 Backend: http://localhost:8001")
    print("📁 Workspace:", WORKSPACE)
    uvicorn.run(app, host="0.0.0.0", port=8001)