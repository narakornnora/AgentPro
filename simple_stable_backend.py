#!/usr/bin/env python3
"""
🚀 Simple Stable Lovable Clone
ระบบสร้างแอป AI ที่เสถียรและใช้งานง่าย
"""
import os
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
import threading

# Configuration
ROOT_DIR = Path("C:/agent")
GENERATED_DIR = ROOT_DIR / "generated_apps"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

class MockAI:
    """Mock AI ที่ทำงานได้แน่นอน"""
    
    def __init__(self):
        self.conversation_count = 0
    
    def chat_decide(self, message: str) -> dict:
        """ตัดสินใจว่าจะสร้างแอปหรือถามต่อ"""
        self.conversation_count += 1
        
        if self.conversation_count >= 2 or len(message) > 50:
            return {
                "action": "build_app",
                "message": "🚀 ข้อมูลเพียงพอแล้ว! เริ่มสร้างแอปเลย",
                "requirements": {"description": message}
            }
        else:
            questions = [
                "อยากได้ฟีเจอร์อะไรเพิ่มเติมไหมครับ?",
                "จะให้มีระบบผู้ใช้งานด้วยไหมครับ?"
            ]
            return {
                "action": "ask_question",
                "message": questions[self.conversation_count - 1]
            }
    
    def generate_files(self, description: str) -> dict:
        """สร้างไฟล์ต่างๆ"""
        
        # Database code
        database_code = '''import sqlite3
import os

def init_database():
    """สร้างฐานข้อมูล"""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # สร้างตาราง users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # สร้างตาราง items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL DEFAULT 0.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # เพิ่มข้อมูลตัวอย่าง
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ("สมชาย ใจดี", "somchai@email.com"),
            ("สมหญิง สวยงาม", "somying@email.com")
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", sample_users)
        
        sample_items = [
            ("กาแฟอเมริกาโน", "กาแฟดำเข้มข้น", 45.0),
            ("ลาเต้", "กาแฟนมหอมมัน", 55.0),
            ("เค้กช็อกโกแลต", "เค้กหวานอร่อย", 75.0)
        ]
        cursor.executemany("INSERT INTO items (title, description, price) VALUES (?, ?, ?)", sample_items)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

if __name__ == "__main__":
    init_database()'''
    
        # Backend code
        backend_code = '''from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import json

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
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'ต้องระบุชื่อ'}), 400
    
    conn = get_db()
    conn.execute('INSERT INTO users (name, email) VALUES (?, ?)',
                (data['name'], data.get('email', '')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'เพิ่มผู้ใช้สำเร็จ'})

@app.route('/api/items')
def get_items():
    conn = get_db()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'ต้องระบุชื่อสินค้า'}), 400
    
    conn = get_db()
    conn.execute('INSERT INTO items (title, description, price) VALUES (?, ?, ?)',
                (data['title'], data.get('description', ''), data.get('price', 0)))
    conn.commit()
    conn.close()
    return jsonify({'message': 'เพิ่มสินค้าสำเร็จ'})

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("📍 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)'''
        
        # Frontend code
        frontend_code = '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Amazing App - สร้างด้วย AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 40px; }
        .header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
        .content { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .card h2 { color: #667eea; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input { width: 100%; padding: 10px; border: 2px solid #e9ecef; border-radius: 8px; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .btn:hover { transform: translateY(-2px); }
        .item { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #667eea; }
        .price { color: #28a745; font-weight: bold; font-size: 1.2em; }
        @media (max-width: 768px) { .content { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Amazing App</h1>
            <p>แอปสุดเจ๋งที่สร้างด้วย AI ใน 30 วินาที!</p>
        </div>
        
        <div class="content">
            <div class="card">
                <h2>👥 ผู้ใช้ในระบบ</h2>
                <div id="userList">กำลังโหลด...</div>
                <h3 style="margin-top: 20px;">เพิ่มผู้ใช้ใหม่</h3>
                <div class="form-group">
                    <label>ชื่อ:</label>
                    <input type="text" id="userName" placeholder="ชื่อผู้ใช้">
                </div>
                <div class="form-group">
                    <label>อีเมล:</label>
                    <input type="email" id="userEmail" placeholder="อีเมล">
                </div>
                <button class="btn" onclick="addUser()">เพิ่มผู้ใช้</button>
            </div>
            
            <div class="card">
                <h2>📦 สินค้าในระบบ</h2>
                <div id="itemList">กำลังโหลด...</div>
                <h3 style="margin-top: 20px;">เพิ่มสินค้าใหม่</h3>
                <div class="form-group">
                    <label>ชื่อสินค้า:</label>
                    <input type="text" id="itemTitle" placeholder="ชื่อสินค้า">
                </div>
                <div class="form-group">
                    <label>รายละเอียด:</label>
                    <input type="text" id="itemDescription" placeholder="รายละเอียด">
                </div>
                <div class="form-group">
                    <label>ราคา:</label>
                    <input type="number" id="itemPrice" placeholder="ราคา">
                </div>
                <button class="btn" onclick="addItem()">เพิ่มสินค้า</button>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            loadUsers();
            loadItems();
        });

        async function loadUsers() {
            try {
                const response = await fetch('/api/users');
                const users = await response.json();
                const userList = document.getElementById('userList');
                if (users.length === 0) {
                    userList.innerHTML = '<div class="item">ยังไม่มีผู้ใช้</div>';
                } else {
                    userList.innerHTML = users.map(user => 
                        `<div class="item"><strong>${user.name}</strong><br>📧 ${user.email}</div>`
                    ).join('');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        async function loadItems() {
            try {
                const response = await fetch('/api/items');
                const items = await response.json();
                const itemList = document.getElementById('itemList');
                if (items.length === 0) {
                    itemList.innerHTML = '<div class="item">ยังไม่มีสินค้า</div>';
                } else {
                    itemList.innerHTML = items.map(item => 
                        `<div class="item">
                            <strong>${item.title}</strong><br>
                            ${item.description}<br>
                            <span class="price">฿${item.price}</span>
                        </div>`
                    ).join('');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        async function addUser() {
            const name = document.getElementById('userName').value;
            const email = document.getElementById('userEmail').value;
            
            if (!name) {
                alert('กรุณากรอกชื่อ');
                return;
            }
            
            try {
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email })
                });
                
                if (response.ok) {
                    document.getElementById('userName').value = '';
                    document.getElementById('userEmail').value = '';
                    loadUsers();
                    alert('เพิ่มผู้ใช้สำเร็จ!');
                }
            } catch (error) {
                alert('เกิดข้อผิดพลาด');
            }
        }

        async function addItem() {
            const title = document.getElementById('itemTitle').value;
            const description = document.getElementById('itemDescription').value;
            const price = parseFloat(document.getElementById('itemPrice').value) || 0;
            
            if (!title) {
                alert('กรุณากรอกชื่อสินค้า');
                return;
            }
            
            try {
                const response = await fetch('/api/items', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, description, price })
                });
                
                if (response.ok) {
                    document.getElementById('itemTitle').value = '';
                    document.getElementById('itemDescription').value = '';
                    document.getElementById('itemPrice').value = '';
                    loadItems();
                    alert('เพิ่มสินค้าสำเร็จ!');
                }
            } catch (error) {
                alert('เกิดข้อผิดพลาด');
            }
        }
    </script>
</body>
</html>'''
        
        return {
            "database.py": database_code,
            "app.py": backend_code, 
            "templates/index.html": frontend_code,
            "requirements.txt": "flask\\nflask-cors\\n",
            "start.bat": "@echo off\\necho 🚀 Starting Amazing App...\\npython database.py\\npython app.py\\npause"
        }

class LovableHTTPHandler(SimpleHTTPRequestHandler):
    """HTTP Handler ที่รองรับ chat API"""
    
    def __init__(self, *args, **kwargs):
        self.mock_ai = MockAI()
        self.sessions = {}
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path.startswith('/?'):
            # Serve main interface
            interface_file = ROOT_DIR / "lovable_split_interface.html"
            if interface_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(interface_file, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_404()
        elif self.path == '/test':
            self.send_json_response({'message': '🚀 Simple Lovable Clone is working!', 'status': 'ready'})
        else:
            self.send_404()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '')
                session_id = data.get('session_id', f'session_{int(time.time())}')
                
                # Process with mock AI
                result = self.mock_ai.chat_decide(message)
                result['session_id'] = session_id
                
                self.send_json_response(result)
                
            except Exception as e:
                self.send_json_response({'type': 'error', 'message': str(e)}, 500)
        else:
            self.send_404()
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_404(self):
        """Send 404 response"""
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'404 Not Found')
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Threaded HTTP Server"""
    pass

def simulate_app_building(session_id: str):
    """จำลองการสร้างแอป"""
    time.sleep(2)  # รอให้ WebSocket เตรียมตัว
    
    # สร้างโฟลเดอร์แอป
    app_id = f"app_{int(time.time())}"
    app_dir = GENERATED_DIR / app_id
    app_dir.mkdir(exist_ok=True)
    
    # สร้างไฟล์ต่างๆ
    mock_ai = MockAI()
    files = mock_ai.generate_files("Sample app")
    
    for filename, content in files.items():
        if '/' in filename:
            # สร้าง directory
            file_path = app_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            file_path = app_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {filename}")
    
    print(f"🎉 App generated at: {app_dir}")
    return str(app_dir)

def start_server():
    """เริ่มเซิร์ฟเวอร์"""
    port = 8007
    server = ThreadedHTTPServer(('localhost', port), LovableHTTPHandler)
    
    print("🚀 Starting Simple Stable Lovable Clone...")
    print(f"📍 Server: http://localhost:{port}")
    print("✨ No dependencies required!")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    start_server()