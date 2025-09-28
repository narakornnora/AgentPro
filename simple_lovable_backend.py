#!/usr/bin/env python3
"""
🚀 Lovable Clone - Simple & Working Version
"""
import os
import json
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

# Simple Configuration
ROOT_DIR = Path("C:/agent")
GENERATED_DIR = ROOT_DIR / "generated_apps"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI App
app = FastAPI(title="Lovable Clone Simple", description="🚀 Working AI App Generator")

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

# Active sessions
active_sessions = {}

class SimpleLovableAI:
    """Simple AI Engine that always works"""
    
    def __init__(self):
        self.sessions = {}
    
    async def chat(self, message: str, session_id: str) -> Dict[str, Any]:
        """Simple chat logic"""
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'messages': [],
                'message_count': 0
            }
        
        session = self.sessions[session_id]
        session['messages'].append(message)
        session['message_count'] += 1
        
        # Simple logic: always build after first message
        if session['message_count'] >= 1:
            return {
                'type': 'start_building',
                'message': 'เริ่มสร้างแอปเลย! 🚀',
                'requirements': {
                    'app_name': 'Generated App',
                    'description': message,
                    'app_type': 'web_app'
                }
            }
        else:
            return {
                'type': 'question',
                'message': 'อยากได้ฟีเจอร์อะไรเพิ่มเติมไหม?'
            }
    
    async def build_app(self, requirements: Dict[str, Any], session_id: str, websocket: WebSocket = None) -> Dict[str, Any]:
        """Build a simple working app"""
        
        app_id = f"app_{uuid.uuid4().hex[:8]}"
        app_dir = GENERATED_DIR / app_id
        app_dir.mkdir(exist_ok=True)
        
        files_created = []
        
        try:
            # Send status updates
            await self._send_update(websocket, "🎯 กำลังวิเคราะห์...")
            await asyncio.sleep(0.5)
            
            # 1. Create database.py
            await self._send_update(websocket, "🗄️ สร้างฐานข้อมูล...")
            database_code = """import sqlite3
import os

def init_db():
    # Initialize database with sample data
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Insert sample data
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", 
                   ("John Doe", "john@example.com"))
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", 
                   ("Jane Smith", "jane@example.com"))
    
    conn.commit()
    conn.close()
    print("Database initialized!")

if __name__ == "__main__":
    init_db()
"""
            
            db_file = app_dir / "database.py"
            with open(db_file, 'w', encoding='utf-8') as f:
                f.write(database_code)
            files_created.append('database.py')
            
            # Send file creation update
            await self._send_file_update(websocket, "database.py", database_code)
            await asyncio.sleep(1)
            
            # 2. Create app.py
            await self._send_update(websocket, "🔧 สร้าง Backend...")
            backend_code = """from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import database

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users')
def get_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)',
                   (data['name'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    database.init_db()
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
'''
            
            backend_file = app_dir / "app.py"
            with open(backend_file, 'w', encoding='utf-8') as f:
                f.write(backend_code)
            files_created.append('app.py')
            
            await self._send_file_update(websocket, "app.py", backend_code)
            await asyncio.sleep(1)
            
            # 3. Create templates/index.html
            await self._send_update(websocket, "🎨 สร้าง Frontend...")
            templates_dir = app_dir / "templates"
            templates_dir.mkdir(exist_ok=True)
            
            html_code = '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Web App</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-center mb-8 text-blue-600">
            🚀 Generated Web App
        </h1>
        
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 class="text-2xl font-semibold mb-4">Add New User</h2>
            <div class="flex gap-4">
                <input type="text" id="userName" placeholder="Name" 
                       class="flex-1 p-2 border rounded">
                <input type="email" id="userEmail" placeholder="Email" 
                       class="flex-1 p-2 border rounded">
                <button onclick="addUser()" 
                        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                    Add User
                </button>
            </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-semibold mb-4">Users List</h2>
            <div id="usersList" class="space-y-2">
                Loading...
            </div>
        </div>
    </div>

    <script>
        async function loadUsers() {
            try {
                const response = await fetch('/api/users');
                const users = await response.json();
                
                const usersList = document.getElementById('usersList');
                usersList.innerHTML = users.map(user => 
                    `<div class="p-3 bg-gray-50 rounded border">
                        <strong>${user.name}</strong> - ${user.email}
                        <small class="text-gray-500 block">ID: ${user.id}</small>
                    </div>`
                ).join('');
            } catch (error) {
                document.getElementById('usersList').innerHTML = 
                    '<p class="text-red-500">Error loading users</p>';
            }
        }
        
        async function addUser() {
            const name = document.getElementById('userName').value;
            const email = document.getElementById('userEmail').value;
            
            if (!name || !email) {
                alert('Please fill in all fields');
                return;
            }
            
            try {
                await fetch('/api/users', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, email})
                });
                
                document.getElementById('userName').value = '';
                document.getElementById('userEmail').value = '';
                loadUsers();
            } catch (error) {
                alert('Error adding user');
            }
        }
        
        // Load users on page load
        loadUsers();
    </script>
</body>
</html>'''
            
            html_file = templates_dir / "index.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_code)
            files_created.append('templates/index.html')
            
            await self._send_file_update(websocket, "index.html", html_code)
            await asyncio.sleep(1)
            
            # 4. Create requirements.txt and start.bat
            await self._send_update(websocket, "📦 สร้างไฟล์เสริม...")
            
            requirements = "flask\nflask-cors\n"
            req_file = app_dir / "requirements.txt"
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(requirements)
            files_created.append('requirements.txt')
            
            start_script = '''@echo off
echo Installing dependencies...
pip install flask flask-cors
echo Starting the app...
python database.py
python app.py
'''
            start_file = app_dir / "start.bat"
            with open(start_file, 'w', encoding='utf-8') as f:
                f.write(start_script)
            files_created.append('start.bat')
            
            await self._send_update(websocket, "✅ แอปสร้างเสร็จแล้ว!")
            
            return {
                'app_id': app_id,
                'app_path': str(app_dir),
                'files_created': files_created,
                'html_content': html_code,
                'status': 'completed'
            }
            
        except Exception as e:
            await self._send_update(websocket, f"❌ เกิดข้อผิดพลาด: {str(e)}")
            raise
    
    async def _send_update(self, websocket: WebSocket, message: str):
        """Send status update"""
        if websocket:
            try:
                await websocket.send_json({
                    'type': 'status_update',
                    'status': message,
                    'timestamp': datetime.now().isoformat()
                })
            except:
                pass
    
    async def _send_file_update(self, websocket: WebSocket, filename: str, content: str):
        """Send file creation update"""
        if websocket:
            try:
                await websocket.send_json({
                    'type': 'file_created',
                    'filename': filename,
                    'content': content[:3000],  # Limit content size
                    'timestamp': datetime.now().isoformat()
                })
            except:
                pass

# Global AI instance
simple_ai = SimpleLovableAI()

@app.get("/")
async def root():
    """Serve the main interface"""
    interface_file = ROOT_DIR / "lovable_split_interface.html"
    if interface_file.exists():
        return FileResponse(str(interface_file))
    return {"message": "🚀 Simple Lovable Clone", "status": "ready"}

@app.post("/chat")
async def chat_endpoint(message_request: ChatMessage):
    """Chat with AI - Simple version"""
    
    session_id = message_request.session_id or f"session_{uuid.uuid4().hex[:8]}"
    
    try:
        result = await simple_ai.chat(message_request.message, session_id)
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
    
    try:
        while True:
            # Wait for build request
            data = await websocket.receive_json()
            
            if data.get('action') == 'build_app':
                requirements = data.get('requirements', {})
                
                # Build app with real-time updates
                result = await simple_ai.build_app(requirements, session_id, websocket)
                
                # Send completion
                await websocket.send_json({
                    'type': 'app_completed',
                    'result': result
                })
    
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Lovable Clone...")
    print("💬 Working version without complex dependencies")
    print("📍 Server: http://localhost:8005")
    uvicorn.run(app, host="0.0.0.0", port=8005)