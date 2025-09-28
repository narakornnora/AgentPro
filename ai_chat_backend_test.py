#!/usr/bin/env python3
"""
🚀 Lovable Clone - Simple Test Version
สร้างแอปจริงจาก Chat (Test Mode)
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
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel

# Configuration
ROOT_DIR = Path("C:/agent")
GENERATED_DIR = ROOT_DIR / "generated_apps"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI App
app = FastAPI(title="Lovable Clone Test", description="🚀 AI App Generator (Test Mode)")

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

class TestLovableAI:
    """AI Engine สำหรับทดสอบ (ไม่ใช้ OpenAI API)"""
    
    def __init__(self):
        self.sessions = {}
        self.demo_files = {
            "database.py": '''import sqlite3
import os

def create_database():
    """สร้างฐานข้อมูล SQLite"""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # สร้างตาราง users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # สร้างตาราง products
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # เพิ่มข้อมูลตัวอย่าง
    cursor.execute("INSERT OR IGNORE INTO products (name, price, description) VALUES (?, ?, ?)",
                   ("Coffee Americano", 45.00, "กาแฟอเมริกาโน่"))
    cursor.execute("INSERT OR IGNORE INTO products (name, price, description) VALUES (?, ?, ?)",
                   ("Cappuccino", 55.00, "กาแฟคาปูชิโน่"))
    cursor.execute("INSERT OR IGNORE INTO products (name, price, description) VALUES (?, ?, ?)",
                   ("Latte", 60.00, "กาแฟลาเต้"))
    
    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

if __name__ == "__main__":
    create_database()
''',
            "app.py": '''from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """เชื่อมต่อฐานข้อมูล"""
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """หน้าแรก"""
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    """API ดึงรายการสินค้า"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    return jsonify([dict(product) for product in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    """API เพิ่มสินค้าใหม่"""
    data = request.get_json()
    
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
                 (data['name'], data['price'], data.get('description', '')))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Product added successfully!'})

@app.route('/api/users')
def get_users():
    """API ดึงรายการผู้ใช้"""
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

if __name__ == '__main__':
    # สร้างฐานข้อมูลก่อนรันแอป
    import database
    database.create_database()
    
    print("🚀 Starting Flask app...")
    print("📍 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
''',
            "index.html": '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Test App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Test Web App</h1>
            <p>สร้างด้วย Lovable Clone AI</p>
        </header>

        <main>
            <section class="products-section">
                <h2>📋 รายการสินค้า</h2>
                <div id="products-list" class="products-grid">
                    <div class="loading">กำลังโหลด...</div>
                </div>
                
                <button class="btn-primary" onclick="showAddForm()">➕ เพิ่มสินค้า</button>
            </section>

            <section class="add-form" id="addForm" style="display: none;">
                <h3>เพิ่มสินค้าใหม่</h3>
                <div class="form-group">
                    <label>ชื่อสินค้า:</label>
                    <input type="text" id="productName" placeholder="ชื่อสินค้า">
                </div>
                <div class="form-group">
                    <label>ราคา:</label>
                    <input type="number" id="productPrice" placeholder="0.00" step="0.01">
                </div>
                <div class="form-group">
                    <label>คำอธิบาย:</label>
                    <textarea id="productDesc" placeholder="คำอธิบายสินค้า"></textarea>
                </div>
                <div class="form-actions">
                    <button class="btn-success" onclick="addProduct()">💾 บันทึก</button>
                    <button class="btn-secondary" onclick="hideAddForm()">❌ ยกเลิก</button>
                </div>
            </section>
        </main>
    </div>
    
    <script src="{{ url_for('static', filename='app.js') }}"></script>
</body>
</html>''',
            "style.css": '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

header p {
    font-size: 1.1em;
    opacity: 0.7;
}

main {
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

h2, h3 {
    margin-bottom: 20px;
    color: #667eea;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.product-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    transition: transform 0.3s ease;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
}

.product-name {
    font-size: 1.3em;
    font-weight: bold;
    margin-bottom: 10px;
    color: #333;
}

.product-price {
    font-size: 1.5em;
    color: #28a745;
    font-weight: bold;
    margin-bottom: 10px;
}

.product-desc {
    color: #666;
    line-height: 1.5;
}

.btn-primary, .btn-success, .btn-secondary {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: all 0.3s ease;
    margin: 5px;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-success {
    background: #28a745;
    color: white;
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-primary:hover, .btn-success:hover, .btn-secondary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.add-form {
    background: #f8f9fa;
    padding: 25px;
    border-radius: 10px;
    margin-top: 30px;
    border: 2px solid #667eea;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
}

.form-actions {
    text-align: center;
    margin-top: 25px;
}

.loading {
    text-align: center;
    color: #666;
    font-style: italic;
}

@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    header h1 {
        font-size: 2em;
    }
    
    .products-grid {
        grid-template-columns: 1fr;
    }
}''',
            "app.js": '''// Global variables
let products = [];

// Load products when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
});

// Load products from API
async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        products = await response.json();
        displayProducts();
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('products-list').innerHTML = 
            '<div class="error">❌ ไม่สามารถโหลดข้อมูลได้</div>';
    }
}

// Display products in grid
function displayProducts() {
    const container = document.getElementById('products-list');
    
    if (products.length === 0) {
        container.innerHTML = '<div class="no-products">ยังไม่มีสินค้า</div>';
        return;
    }
    
    const html = products.map(product => `
        <div class="product-card">
            <div class="product-name">${product.name}</div>
            <div class="product-price">฿${parseFloat(product.price).toFixed(2)}</div>
            <div class="product-desc">${product.description || ''}</div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// Show add product form
function showAddForm() {
    document.getElementById('addForm').style.display = 'block';
    document.getElementById('productName').focus();
}

// Hide add product form
function hideAddForm() {
    document.getElementById('addForm').style.display = 'none';
    clearForm();
}

// Clear form inputs
function clearForm() {
    document.getElementById('productName').value = '';
    document.getElementById('productPrice').value = '';
    document.getElementById('productDesc').value = '';
}

// Add new product
async function addProduct() {
    const name = document.getElementById('productName').value.trim();
    const price = parseFloat(document.getElementById('productPrice').value);
    const description = document.getElementById('productDesc').value.trim();
    
    // Validation
    if (!name) {
        alert('กรุณากรอกชื่อสินค้า');
        return;
    }
    
    if (!price || price <= 0) {
        alert('กรุณากรอกราคาที่ถูกต้อง');
        return;
    }
    
    try {
        const response = await fetch('/api/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                price: price,
                description: description
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ เพิ่มสินค้าเรียบร้อย!');
            hideAddForm();
            loadProducts(); // Reload products
        } else {
            alert('❌ เกิดข้อผิดพลาด: ' + result.message);
        }
        
    } catch (error) {
        console.error('Error adding product:', error);
        alert('❌ ไม่สามารถเพิ่มสินค้าได้');
    }
}

// Handle Enter key in form
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && document.getElementById('addForm').style.display !== 'none') {
        addProduct();
    }
});'''
        }
    
    async def chat(self, message: str, session_id: str) -> Dict[str, Any]:
        """แชทกับ AI (Test Mode)"""
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'messages': [],
                'requirements': {},
                'status': 'chatting'
            }
        
        session = self.sessions[session_id]
        session['messages'].append({"role": "user", "content": message})
        
        # Simple decision logic
        message_count = len(session['messages'])
        user_message = message.lower()
        
        # If user mentioned specific app type, start building
        if any(word in user_message for word in ['เว็บ', 'แอป', 'ระบบ', 'ร้าน', 'โรงแรม', 'สร้าง', 'ทำ']):
            session['status'] = 'building'
            return {
                'type': 'start_building',
                'message': 'เริ่มสร้างแอปทดสอบเลย! 🚀',
                'requirements': {
                    "app_type": "test_web_app",
                    "features": ["database", "api", "frontend"],
                    "description": message,
                    "app_name": "Test Web App"
                }
            }
        
        # Ask a simple question
        if message_count <= 2:
            ai_response = "อยากได้ฟีเจอร์อะไรเพิ่มเติมไหมครับ? (หรือพิมพ์ 'สร้างเลย' เพื่อเริ่มทันที)"
        else:
            ai_response = "เริ่มสร้างแอปทดสอบเลยไหมครับ? 🚀"
        
        session['messages'].append({"role": "assistant", "content": ai_response})
        return {
            'type': 'question',
            'message': ai_response,
            'confidence': 0.8
        }
    
    async def build_app(self, requirements: Dict[str, Any], session_id: str, websocket: WebSocket = None) -> Dict[str, Any]:
        """สร้างแอปทดสอบ"""
        
        app_id = f"test_{uuid.uuid4().hex[:8]}"
        app_dir = GENERATED_DIR / app_id
        app_dir.mkdir(exist_ok=True)
        
        try:
            await self._send_status(websocket, "🎯 เตรียมโปรเจคทดสอบ...")
            await asyncio.sleep(1)
            
            # Create directories
            templates_dir = app_dir / "templates"
            static_dir = app_dir / "static"
            templates_dir.mkdir(exist_ok=True)
            static_dir.mkdir(exist_ok=True)
            
            files_created = []
            
            # สร้างไฟล์ทีละไฟล์พร้อม animation
            for filename, content in self.demo_files.items():
                await self._send_status(websocket, f"📄 กำลังสร้าง {filename}...")
                
                if filename == "index.html":
                    file_path = templates_dir / filename
                elif filename in ["style.css", "app.js"]:
                    file_path = static_dir / filename  
                else:
                    file_path = app_dir / filename
                
                # Write file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                files_created.append(filename)
                
                # Send file creation notification
                await self._send_file_created(websocket, filename, content, str(file_path))
                await asyncio.sleep(0.5)  # Small delay for demo effect
            
            # Create requirements.txt
            requirements_content = "flask\nflask-cors\n"
            req_file = app_dir / "requirements.txt"
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(requirements_content)
            files_created.append('requirements.txt')
            
            # Create start.bat
            start_content = f"""@echo off
echo Starting Test Web App...
python database.py
python app.py
"""
            start_file = app_dir / "start.bat"
            with open(start_file, 'w', encoding='utf-8') as f:
                f.write(start_content)
            files_created.append('start.bat')
            
            await self._send_status(websocket, "✅ แอปทดสอบสร้างเสร็จแล้ว!")
            
            return {
                'app_id': app_id,
                'app_path': str(app_dir),
                'plan': {
                    'app_name': 'Test Web App',
                    'description': 'แอปทดสอบที่สร้างด้วย AI'
                },
                'files_created': files_created,
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
                    'content': content[:2000],  # ส่งแค่ 2000 ตัวอักษรแรก
                    'filePath': file_path,
                    'timestamp': datetime.now().isoformat()
                })
            except:
                pass


# Global AI instance
test_ai = TestLovableAI()


@app.get("/")
async def root():
    """Serve the main interface"""
    interface_file = ROOT_DIR / "lovable_split_interface.html"
    if interface_file.exists():
        return FileResponse(str(interface_file))
    return {"message": "🚀 Lovable Clone Test", "status": "ready"}


@app.post("/chat")
async def chat_endpoint(message_request: ChatMessage):
    """Chat with Test AI"""
    
    session_id = message_request.session_id or f"test_{uuid.uuid4().hex[:8]}"
    
    try:
        result = await test_ai.chat(message_request.message, session_id)
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
                result = await test_ai.build_app(requirements, session_id, websocket)
                
                # ส่งผลลัพธ์สุดท้าย
                await websocket.send_json({
                    'type': 'app_completed',
                    'result': result
                })
    
    except WebSocketDisconnect:
        if session_id in websocket_connections:
            del websocket_connections[session_id]


@app.get("/preview/{app_id}")
async def preview_app(app_id: str):
    """Preview generated app"""
    app_dir = GENERATED_DIR / app_id
    index_file = app_dir / "templates" / "index.html"
    
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Simple static preview (replace Flask template syntax)
        html_content = html_content.replace(
            "{{ url_for('static', filename='style.css') }}", 
            f"/static/{app_id}/style.css"
        )
        html_content = html_content.replace(
            "{{ url_for('static', filename='app.js') }}", 
            f"/static/{app_id}/app.js"
        )
        
        return HTMLResponse(html_content)
    
    return HTMLResponse("<h1>App not found</h1>")


@app.get("/static/{app_id}/{filename}")
async def serve_static(app_id: str, filename: str):
    """Serve static files for preview"""
    static_file = GENERATED_DIR / app_id / "static" / filename
    if static_file.exists():
        return FileResponse(str(static_file))
    return JSONResponse({"error": "File not found"}, status_code=404)


@app.get("/apps")
async def list_apps():
    """List generated apps"""
    apps = []
    for app_dir in GENERATED_DIR.iterdir():
        if app_dir.is_dir():
            apps.append({
                'id': app_dir.name,
                'path': str(app_dir),
                'preview_url': f"/preview/{app_dir.name}",
                'created': datetime.fromtimestamp(app_dir.stat().st_mtime).isoformat()
            })
    
    return {"apps": apps}


if __name__ == "__main__":
    import uvicorn
    print("🧪 Starting Lovable Clone TEST MODE...")
    print("💡 This version works without OpenAI API")
    print("📍 Server: http://localhost:8004")
    uvicorn.run(app, host="0.0.0.0", port=8004)