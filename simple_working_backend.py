#!/usr/bin/env python3
"""
Simple Working Lovable Clone
"""
import os
import json
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Config
ROOT_DIR = Path("C:/agent")
GENERATED_DIR = ROOT_DIR / "generated_apps"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Simple Lovable Clone")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatMessage(BaseModel):
    message: str
    session_id: str = None

class SimpleAI:
    def __init__(self):
        self.sessions = {}
    
    async def chat(self, message: str, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = {'count': 0}
        
        self.sessions[session_id]['count'] += 1
        
        if self.sessions[session_id]['count'] >= 1:
            return {
                'type': 'start_building',
                'message': 'เริ่มสร้างแอปเลย! 🚀',
                'requirements': {'app_name': 'Generated App', 'description': message}
            }
        else:
            return {'type': 'question', 'message': 'อยากได้ฟีเจอร์อะไรเพิ่มเติม?'}
    
    async def build_app(self, requirements: Dict[str, Any], session_id: str, websocket: WebSocket = None):
        app_id = f"app_{uuid.uuid4().hex[:8]}"
        app_dir = GENERATED_DIR / app_id
        app_dir.mkdir(exist_ok=True)
        
        # Send exciting updates
        updates = [
            "🎯 เริ่มต้นการสร้าง...",
            "🗄️ สร้างฐานข้อมูล...",
            "🔧 สร้าง Backend API...", 
            "🎨 สร้าง Frontend UI...",
            "📦 สร้างไฟล์เสริม...",
            "✅ แอปสร้างเสร็จแล้ว!"
        ]
        
        files = {}
        
        for i, update in enumerate(updates):
            if websocket:
                try:
                    await websocket.send_json({'type': 'status_update', 'status': update})
                except:
                    pass
            
            await asyncio.sleep(1)
            
            # Create files based on step
            if i == 1:  # Database
                db_code = """import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )''')
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", ("John Doe", "john@example.com"))
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", ("Jane Smith", "jane@example.com"))
    conn.commit()
    conn.close()
    print("Database ready!")

if __name__ == "__main__":
    init_db()"""
                
                files['database.py'] = db_code
                with open(app_dir / "database.py", 'w', encoding='utf-8') as f:
                    f.write(db_code)
                
                if websocket:
                    try:
                        await websocket.send_json({
                            'type': 'file_created',
                            'filename': 'database.py',
                            'content': db_code
                        })
                    except:
                        pass
            
            elif i == 2:  # Backend
                backend_code = """from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import database

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users')
def get_users():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (data['name'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    database.init_db()
    print("App running at http://localhost:5000")
    app.run(debug=True, port=5000)"""
                
                files['app.py'] = backend_code
                with open(app_dir / "app.py", 'w', encoding='utf-8') as f:
                    f.write(backend_code)
                
                if websocket:
                    try:
                        await websocket.send_json({
                            'type': 'file_created',
                            'filename': 'app.py',
                            'content': backend_code
                        })
                    except:
                        pass
            
            elif i == 3:  # Frontend
                templates_dir = app_dir / "templates"
                templates_dir.mkdir(exist_ok=True)
                
                html_code = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Web App</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <div class="text-center mb-8">
            <h1 class="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
                🚀 Generated Web App
            </h1>
            <p class="text-gray-600 text-lg">สร้างด้วย AI ใน Lovable Clone</p>
        </div>
        
        <div class="max-w-4xl mx-auto">
            <div class="bg-white rounded-2xl shadow-xl p-8 mb-8">
                <h2 class="text-3xl font-semibold mb-6 text-gray-800">✨ Add New User</h2>
                <div class="grid md:grid-cols-3 gap-4">
                    <input type="text" id="userName" placeholder="Enter name" 
                           class="px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-colors">
                    <input type="email" id="userEmail" placeholder="Enter email" 
                           class="px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-colors">
                    <button onclick="addUser()" 
                            class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all transform hover:scale-105 font-semibold">
                        ➕ Add User
                    </button>
                </div>
            </div>
            
            <div class="bg-white rounded-2xl shadow-xl p-8">
                <h2 class="text-3xl font-semibold mb-6 text-gray-800">👥 Users List</h2>
                <div id="usersList" class="grid gap-4">
                    <div class="animate-pulse bg-gray-200 h-16 rounded-xl"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function loadUsers() {
            try {
                const response = await fetch('/api/users');
                const users = await response.json();
                
                const usersList = document.getElementById('usersList');
                usersList.innerHTML = users.map(user => `
                    <div class="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-xl border-l-4 border-blue-500 hover:shadow-md transition-all">
                        <div class="flex justify-between items-center">
                            <div>
                                <h3 class="text-xl font-semibold text-gray-800">${user.name}</h3>
                                <p class="text-blue-600">${user.email}</p>
                            </div>
                            <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                                ID: ${user.id}
                            </div>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                document.getElementById('usersList').innerHTML = 
                    '<div class="text-red-500 text-center py-8">❌ Error loading users</div>';
            }
        }
        
        async function addUser() {
            const name = document.getElementById('userName').value.trim();
            const email = document.getElementById('userEmail').value.trim();
            
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
                
                // Success animation
                const button = event.target;
                const originalText = button.innerHTML;
                button.innerHTML = '✅ Added!';
                button.classList.add('bg-green-500');
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.classList.remove('bg-green-500');
                }, 2000);
                
            } catch (error) {
                alert('Error adding user');
            }
        }
        
        loadUsers();
    </script>
</body>
</html>"""
                
                files['index.html'] = html_code
                with open(templates_dir / "index.html", 'w', encoding='utf-8') as f:
                    f.write(html_code)
                
                if websocket:
                    try:
                        await websocket.send_json({
                            'type': 'file_created',
                            'filename': 'index.html',
                            'content': html_code
                        })
                    except:
                        pass
        
        # Create requirements and start script
        with open(app_dir / "requirements.txt", 'w') as f:
            f.write("flask\nflask-cors\n")
        
        with open(app_dir / "start.bat", 'w') as f:
            f.write("@echo off\necho Installing dependencies...\npip install flask flask-cors\necho Starting app...\npython database.py\npython app.py\n")
        
        return {
            'app_id': app_id,
            'app_path': str(app_dir),
            'files_created': list(files.keys()) + ['requirements.txt', 'start.bat'],
            'html_content': files.get('index.html', ''),
            'status': 'completed'
        }

ai = SimpleAI()

@app.get("/")
async def root():
    interface_file = ROOT_DIR / "lovable_split_interface.html"
    if interface_file.exists():
        return FileResponse(str(interface_file))
    return {"message": "Simple Lovable Clone Ready"}

@app.post("/chat")
async def chat_endpoint(message_request: ChatMessage):
    session_id = message_request.session_id or f"session_{uuid.uuid4().hex[:8]}"
    try:
        result = await ai.chat(message_request.message, session_id)
        result['session_id'] = session_id
        return result
    except Exception as e:
        return {'type': 'error', 'message': f"Error: {str(e)}", 'session_id': session_id}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('action') == 'build_app':
                requirements = data.get('requirements', {})
                result = await ai.build_app(requirements, session_id, websocket)
                await websocket.send_json({'type': 'app_completed', 'result': result})
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Lovable Clone...")
    print("📍 Server: http://localhost:8005")
    uvicorn.run(app, host="0.0.0.0", port=8005)