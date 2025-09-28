#!/usr/bin/env python3
"""
🚀 Stable Exciting Backend - ทำงานได้แน่นอน!
เวอร์ชั่นที่สมบูรณ์แบบกับ exciting effects
"""
import json
import asyncio
from pathlib import Path
from datetime import datetime
import uuid

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, JSONResponse
    from pydantic import BaseModel
except ImportError:
    import subprocess
    import sys
    print("📦 Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "websockets", "--quiet"])
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, JSONResponse
    from pydantic import BaseModel

app = FastAPI(title="🚀 Stable Exciting Lovable Clone")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"

# Simple storage
sessions = {}
connections = {}
app_counter = 0

@app.get("/")
async def root():
    """Serve the exciting interface"""
    try:
        interface_file = Path("C:/agent/lovable_split_interface.html")
        if interface_file.exists():
            return FileResponse(str(interface_file))
    except:
        pass
    return {
        "message": "🚀 Stable Exciting Lovable Clone",
        "status": "ready",
        "version": "stable-exciting",
        "features": ["split_screen", "exciting_effects", "realtime_building"]
    }

@app.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "✅ healthy", "server": "stable-exciting"}

@app.post("/chat")
async def chat(message: ChatMessage):
    """Chat endpoint with simple logic"""
    try:
        session_id = message.session_id or str(uuid.uuid4())[:8]
        user_message = message.message.lower().strip()
        
        # Initialize session
        if session_id not in sessions:
            sessions[session_id] = []
        
        sessions[session_id].append(user_message)
        message_count = len(sessions[session_id])
        
        # Build triggers
        build_keywords = ['สร้าง', 'เว็บ', 'แอป', 'ทำ', 'app', 'web', 'site', 'build', 'create']
        should_build = (
            message_count >= 2 or 
            any(keyword in user_message for keyword in build_keywords) or
            len(user_message) > 50
        )
        
        if should_build:
            return {
                "type": "start_building",
                "message": "🚀 เริ่มสร้างแอปเลยครับ! กำลังเตรียมระบบ AI...",
                "session_id": session_id,
                "requirements": {
                    "app_name": f"Amazing App #{session_id}",
                    "description": message.message[:200],
                    "user_input": message.message
                }
            }
        else:
            responses = [
                "🤔 เข้าใจแล้วครับ! อยากได้ฟีเจอร์อะไรเพิ่มเติมไหม?",
                "✨ ไอเดียเจ๋ง! มีความต้องการพิเศษอะไรอีกไหมครับ?",
                "💡 สนใจมากเลย! เล่าเพิ่มเติมหน่อยได้ไหมครับ?"
            ]
            return {
                "type": "question",
                "message": responses[message_count % len(responses)],
                "session_id": session_id
            }
            
    except Exception as e:
        return JSONResponse(
            {"error": f"Chat error: {str(e)}", "type": "error"},
            status_code=500
        )

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket for exciting real-time building"""
    await websocket.accept()
    connections[session_id] = websocket
    
    try:
        await websocket.send_json({
            "type": "connection_established",
            "session_id": session_id,
            "message": "✅ เชื่อมต่อสำเร็จ! พร้อมสร้างแอปแล้ว"
        })
        
        while True:
            data = await websocket.receive_json()
            
            if data.get("action") == "build_app":
                await build_exciting_app(websocket, session_id, data.get("requirements", {}))
            elif data.get("action") == "ping":
                await websocket.send_json({"type": "pong", "timestamp": datetime.now().isoformat()})
                
    except WebSocketDisconnect:
        if session_id in connections:
            del connections[session_id]
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"Connection error: {str(e)}"
            })
        except:
            pass

async def build_exciting_app(websocket: WebSocket, session_id: str, requirements: dict):
    """สร้างแอปพร้อม exciting effects"""
    global app_counter
    app_counter += 1
    
    app_name = requirements.get("app_name", f"Amazing App #{app_counter}")
    description = requirements.get("description", "แอปสุดเจ๋งที่สร้างด้วย AI")
    
    # Exciting build steps
    build_steps = [
        ("🎯", "วิเคราะห์ความต้องการด้วย AI", 1.5),
        ("🧠", "AI ออกแบบสถาปัตยกรรม", 2.0),
        ("🗄️", "สร้างระบบฐานข้อมูล", 2.5),
        ("⚡", "เขียน Backend API", 3.0),
        ("🎨", "ออกแบบ UI/UX", 2.5),
        ("📱", "สร้าง Frontend", 3.0),
        ("🔧", "ปรับแต่งและทดสอบ", 1.5),
        ("📦", "เตรียมไฟล์พร้อมใช้งาน", 1.0),
        ("✅", "แอปสร้างเสร็จแล้ว!", 0.5)
    ]
    
    try:
        # Send build start
        await websocket.send_json({
            "type": "build_started",
            "app_name": app_name,
            "session_id": session_id,
            "estimated_time": "30 วินาที"
        })
        
        # Execute exciting steps
        for step_num, (icon, status, delay) in enumerate(build_steps, 1):
            progress = (step_num - 1) / len(build_steps)
            
            await websocket.send_json({
                "type": "exciting_status",
                "icon": icon,
                "status": status,
                "progress": progress,
                "step": step_num,
                "total_steps": len(build_steps)
            })
            
            # Special actions for certain steps
            if "ฐานข้อมูล" in status:
                await create_file_with_typing(websocket, "database.py", get_database_code())
            elif "Backend" in status:
                await create_file_with_typing(websocket, "app.py", get_backend_code(app_name))
            elif "Frontend" in status:
                await create_file_with_typing(websocket, "index.html", get_frontend_code(app_name))
            elif "เตรียมไฟล์" in status:
                await websocket.send_json({
                    "type": "file_structure",
                    "files": [
                        "📄 app.py - Backend API",
                        "📄 database.py - ฐานข้อมูล",
                        "📄 index.html - Frontend",
                        "📄 requirements.txt - Dependencies",
                        "📄 README.md - คู่มือใช้งาน"
                    ]
                })
            
            await asyncio.sleep(delay)
        
        # Send completion
        await websocket.send_json({
            "type": "app_completed",
            "session_id": session_id,
            "result": {
                "app_id": f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_id}",
                "app_name": app_name,
                "description": description,
                "features": [
                    "📊 ระบบจัดการข้อมูล",
                    "👥 จัดการผู้ใช้",
                    "🛍️ จัดการสินค้า",
                    "📱 Responsive Design",
                    "⚡ Real-time Updates",
                    "🎨 Beautiful UI"
                ],
                "technologies": ["Python Flask", "SQLite", "HTML5", "CSS3", "JavaScript"],
                "deployment_ready": True,
                "status": "completed",
                "build_time": f"{sum(step[2] for step in build_steps):.1f} วินาที"
            }
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "build_error",
            "error": str(e),
            "message": "❌ เกิดข้อผิดพลาดในการสร้างแอป"
        })

async def create_file_with_typing(websocket: WebSocket, filename: str, content: str):
    """สร้างไฟล์พร้อม typing effect"""
    
    await websocket.send_json({
        "type": "file_typing_start",
        "filename": filename,
        "total_chars": len(content)
    })
    
    # ส่งเนื้อหาทีละส่วน
    chunk_size = 50
    for i in range(0, len(content), chunk_size):
        chunk = content[i:i + chunk_size]
        progress = min((i + chunk_size) / len(content), 1.0)
        
        await websocket.send_json({
            "type": "file_typing_chunk",
            "filename": filename,
            "chunk": chunk,
            "progress": progress
        })
        
        await asyncio.sleep(0.03)  # 30ms สำหรับ typing effect
    
    await websocket.send_json({
        "type": "file_typing_complete",
        "filename": filename
    })

def get_database_code():
    return '''import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='app.db'):
        self.conn = sqlite3.connect(db_path)
        self.setup_tables()
    
    def setup_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL DEFAULT 0,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        print("✅ Database initialized successfully!")

if __name__ == "__main__":
    db = Database()
'''

def get_backend_code(app_name):
    return f'''from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/users')
def get_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)',
                    (data['name'], data['email']))
        conn.commit()
        return jsonify({{'success': True}})
    except Exception as e:
        return jsonify({{'error': str(e)}}), 400
    finally:
        conn.close()

@app.route('/api/products')
def get_products():
    conn = get_db()
    products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(product) for product in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    conn = get_db()
    try:
        conn.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
                    (data['name'], data.get('price', 0), data.get('description', '')))
        conn.commit()
        return jsonify({{'success': True}})
    except Exception as e:
        return jsonify({{'error': str(e)}}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    print("🚀 Starting {app_name}...")
    print("📍 Server: http://localhost:5000")
    app.run(debug=True, port=5000)
'''

def get_frontend_code(app_name):
    return f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 {app_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .btn {{
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 5px;
        }}
        
        input {{
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 {app_name}</h1>
            <p>สร้างด้วย AI ใน 30 วินาที!</p>
        </div>
        
        <div class="content">
            <div class="card">
                <h2>👥 ผู้ใช้</h2>
                <div id="userList">กำลังโหลด...</div>
                <input type="text" id="userName" placeholder="ชื่อ">
                <input type="email" id="userEmail" placeholder="อีเมล">
                <button class="btn" onclick="addUser()">เพิ่มผู้ใช้</button>
            </div>
            
            <div class="card">
                <h2>🛍️ สินค้า</h2>
                <div id="productList">กำลังโหลด...</div>
                <input type="text" id="productName" placeholder="ชื่อสินค้า">
                <input type="number" id="productPrice" placeholder="ราคา">
                <button class="btn" onclick="addProduct()">เพิ่มสินค้า</button>
            </div>
        </div>
    </div>

    <script>
        // Load data on page load
        document.addEventListener('DOMContentLoaded', function() {{
            loadUsers();
            loadProducts();
        }});

        function loadUsers() {{
            fetch('/api/users')
                .then(response => response.json())
                .then(users => {{
                    document.getElementById('userList').innerHTML = 
                        users.length ? users.map(u => `<p>👤 ${{u.name}} - ${{u.email}}</p>`).join('') : 'ยังไม่มีผู้ใช้';
                }});
        }}

        function loadProducts() {{
            fetch('/api/products')
                .then(response => response.json())
                .then(products => {{
                    document.getElementById('productList').innerHTML = 
                        products.length ? products.map(p => `<p>🛍️ ${{p.name}} - ฿${{p.price}}</p>`).join('') : 'ยังไม่มีสินค้า';
                }});
        }}

        function addUser() {{
            const name = document.getElementById('userName').value;
            const email = document.getElementById('userEmail').value;
            
            if (name && email) {{
                fetch('/api/users', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{name, email}})
                }})
                .then(() => {{
                    document.getElementById('userName').value = '';
                    document.getElementById('userEmail').value = '';
                    loadUsers();
                }});
            }}
        }}

        function addProduct() {{
            const name = document.getElementById('productName').value;
            const price = document.getElementById('productPrice').value || 0;
            
            if (name) {{
                fetch('/api/products', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{name, price}})
                }})
                .then(() => {{
                    document.getElementById('productName').value = '';
                    document.getElementById('productPrice').value = '';
                    loadProducts();
                }});
            }}
        }}
    </script>
</body>
</html>'''

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Stable Exciting Lovable Clone...")
    print("✨ Version: Stable with Exciting Effects")
    print("🔧 Features: Split Screen + Real-time Building")
    print("📍 Server: http://localhost:8008")
    print("🏥 Health: http://localhost:8008/health")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8008,
            log_level="warning"  # Reduce log noise
        )
    except Exception as e:
        print(f"❌ Server error: {e}")