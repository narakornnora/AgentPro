#!/usr/bin/env python3
"""
🚀 Lovable Clone - Exciting AI App Generator
สร้างแอปจริงจาก Chat พร้อม Effects น่าตื่นเต้น!
"""
import os
import json
import asyncio
import uuid
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Real OpenAI Integration  
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class RealAI:
    """Real OpenAI AI integration with fallback"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.use_real_ai = True
        else:
            self.use_real_ai = False
            print("🤖 Using demo mode - set OPENAI_API_KEY for real AI")
        self.conversation_count = 0
    
    def chat_decide(self, messages: List[Dict]) -> Dict[str, Any]:
        """ใช้ OpenAI จริง ตัดสินใจจะถามต่อหรือสร้างแอป"""
        self.conversation_count += 1
        
        if not self.use_real_ai:
            # Demo mode
            user_msg = messages[-1]['content'].lower()
            
            if any(word in user_msg for word in ['todo', 'task', 'งาน', 'ทำ']):
                return {
                    "action": "build_app",
                    "message": "เข้าใจแล้ว! จะสร้างแอป Todo List ให้เลย 🚀",
                    "requirements": {
                        "app_type": "todo_app",
                        "features": ["เพิ่มงาน", "ลบงาน", "เช็คเสร็จ"],
                        "ui": "modern"
                    }
                }
            elif any(word in user_msg for word in ['shop', 'ร้าน', 'ขาย', 'สินค้า']):
                return {
                    "action": "build_app", 
                    "message": "เยิ่ม! จะสร้างแอปร้านค้าออนไลน์ให้ 🛍️",
                    "requirements": {
                        "app_type": "shop_app",
                        "features": ["แสดงสินค้า", "เพิ่มลงตะกร้า", "จัดการคำสั่งซื้อ"],
                        "ui": "ecommerce"
                    }
                }
            else:
                return {
                    "action": "ask_question",
                    "message": "สวัสดี! อยากให้ฉันสร้างแอปอะไรให้คะ? เช่น Todo List, ร้านค้า, หรือแอปอื่นๆ 😊"
                }
        
        try:
            # ใช้ OpenAI จริง
            system_prompt = """คุณคือผู้ช่วย AI สร้างแอป วิเคราะห์คำขอและตัดสินใจ:
1. ถ้าต้องการข้อมูลเพิ่ม ให้ถามคำถามเฉพาะเจาะจง 1 คำถาม
2. ถ้าข้อมูลพอแล้ว ตอบด้วย action: "build_app" และส่งข้อกำหนดแอป

ตอบในรูปแบบ JSON:
{
    "action": "ask_question" หรือ "build_app", 
    "message": "คำตอบเป็นภาษาไทย",
    "requirements": {...} (เฉพาะตอนสร้างแอป)
}"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *messages
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                # ลองแยก JSON จากข้อความ
                if '```json' in content:
                    json_part = content.split('```json')[1].split('```')[0]
                elif '{' in content:
                    json_part = content[content.find('{'):content.rfind('}')+1]
                else:
                    json_part = content
                    
                result = json.loads(json_part)
                return result
            except:
                # ถ้า parse JSON ไม่ได้ ให้ตอบแบบปกติ
                return {
                    "action": "ask_question",
                    "message": content
                }
                
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return {
                "action": "ask_question", 
                "message": "ขออภัย มีปัญหาเทคนิค อยากให้สร้างแอปอะไรคะ?"
            }
    
    def generate_plan(self, requirements: Dict) -> Dict:
        """สร้างแผนการพัฒนา"""
        return {
            "app_name": "Amazing App",
            "description": "แอปสุดเจ๋งที่สร้างด้วย AI",
            "database_schema": [
                {
                    "table": "users",
                    "fields": [
                        {"name": "id", "type": "INTEGER PRIMARY KEY"},
                        {"name": "name", "type": "TEXT NOT NULL"},
                        {"name": "email", "type": "TEXT UNIQUE"}
                    ]
                },
                {
                    "table": "items", 
                    "fields": [
                        {"name": "id", "type": "INTEGER PRIMARY KEY"},
                        {"name": "title", "type": "TEXT NOT NULL"},
                        {"name": "price", "type": "REAL"}
                    ]
                }
            ],
            "api_endpoints": [
                {"method": "GET", "path": "/api/users", "description": "ดึงรายการผู้ใช้"},
                {"method": "POST", "path": "/api/users", "description": "เพิ่มผู้ใช้ใหม่"},
                {"method": "GET", "path": "/api/items", "description": "ดึงรายการสินค้า"}
            ]
        }
    
    def generate_code(self, file_type: str, plan: Dict) -> str:
        """สร้างโค้ด"""
        if file_type == "database":
            return '''import sqlite3
import os

class Database:
    def __init__(self, db_name="app.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """สร้างตารางในฐานข้อมูล"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # สร้างตาราง users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
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
                ("สมหญิง สวยงาม", "somying@email.com"),
                ("บอบ นักพัฒนา", "bob@email.com")
            ]
            cursor.executemany(
                "INSERT INTO users (name, email) VALUES (?, ?)", 
                sample_users
            )
            
        cursor.execute("SELECT COUNT(*) FROM items")
        if cursor.fetchone()[0] == 0:
            sample_items = [
                ("กาแฟอเมริกาโน", "กาแฟดำสไตล์อเมริกัน", 45.0),
                ("ลาเต้", "กาแฟนมสุดอร่อย", 55.0),
                ("เค้กช็อกโกแลต", "เค้กหวานมันเข้มข้น", 75.0)
            ]
            cursor.executemany(
                "INSERT INTO items (title, description, price) VALUES (?, ?, ?)",
                sample_items
            )
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")

if __name__ == "__main__":
    db = Database()
    print("🗄️ Database setup complete!")'''
            
        elif file_type == "backend":
            return '''from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """เชื่อมต่อฐานข้อมูล"""
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    """หน้าแรก"""
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    """ดึงรายการผู้ใช้ทั้งหมด"""
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def add_user():
    """เพิ่มผู้ใช้ใหม่"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'ต้องระบุชื่อและอีเมล'}), 400
    
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (data['name'], data['email'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'เพิ่มผู้ใช้สำเร็จ'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'อีเมลนี้มีอยู่แล้ว'}), 400

@app.route('/api/items', methods=['GET'])
def get_items():
    """ดึงรายการสินค้าทั้งหมด"""
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return jsonify([dict(item) for item in items])

@app.route('/api/items', methods=['POST'])
def add_item():
    """เพิ่มสินค้าใหม่"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'ต้องระบุชื่อสินค้า'}), 400
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO items (title, description, price) VALUES (?, ?, ?)',
        (data['title'], data.get('description', ''), data.get('price', 0.0))
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'เพิ่มสินค้าสำเร็จ'}), 201

@app.route('/api/health')
def health_check():
    """ตรวจสอบสถานะระบบ"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'API ทำงานปกติ'
    })

if __name__ == '__main__':
    print("🚀 Starting Flask API server...")
    print("📍 Server: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)'''
        
        elif file_type == "frontend":
            app_type = plan.get('app_type', 'todo_app')
            
            if app_type == 'shop_app':
                return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>�️ ร้านค้าออนไลน์ - สร้างด้วย AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header h1 { font-size: 3em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .product-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .product-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .product-title {
            font-size: 1.5em;
            color: #667eea;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .product-description {
            color: #666;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        
        .product-price {
            font-size: 1.8em;
            color: #e74c3c;
            font-weight: bold;
            margin-bottom: 15px;
        }
        
        .add-to-cart {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .add-to-cart:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .cart-info {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2ecc71;
            color: white;
            padding: 15px 20px;
            border-radius: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            font-weight: bold;
        }
        
        .loading {
            text-align: center;
            color: white;
            font-size: 1.2em;
            margin: 40px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛍️ ร้านค้าออนไลน์</h1>
            <p>สร้างด้วย AI - ใช้งานได้จริง!</p>
        </div>
        
        <div class="cart-info">
            🛒 ตะกร้า: <span id="cart-count">0</span> รายการ
        </div>
        
        <div id="loading" class="loading">
            กำลังโหลดสินค้า... ⏳
        </div>
        
        <div id="products-container" class="products-grid" style="display:none;">
        </div>
    </div>

    <script>
        let cart = [];
        
        async function loadProducts() {
            try {
                const response = await fetch('/api/items');
                const products = await response.json();
                
                const container = document.getElementById('products-container');
                const loading = document.getElementById('loading');
                
                if (products && products.length > 0) {
                    container.innerHTML = products.map(product => `
                        <div class="product-card">
                            <div class="product-title">${product.title}</div>
                            <div class="product-description">${product.description || 'สินค้าคุณภาพดี'}</div>
                            <div class="product-price">฿${product.price}</div>
                            <button class="add-to-cart" onclick="addToCart(${product.id}, '${product.title}', ${product.price})">
                                เพิ่มลงตะกร้า 🛒
                            </button>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = `
                        <div style="grid-column: 1/-1; text-align: center; color: white;">
                            <h2>ยังไม่มีสินค้า</h2>
                            <p>กำลังเตรียมสินค้าให้ลูกค้า...</p>
                        </div>
                    `;
                }
                
                loading.style.display = 'none';
                container.style.display = 'grid';
                
            } catch (error) {
                console.error('Error loading products:', error);
                document.getElementById('loading').innerHTML = '❌ ไม่สามารถโหลดสินค้าได้';
            }
        }
        
        function addToCart(id, title, price) {
            cart.push({id, title, price});
            updateCartDisplay();
            
            // แสดงแอนิเมชันสำเร็จ
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = '✅ เพิ่มแล้ว!';
            button.style.background = '#2ecc71';
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }, 1000);
        }
        
        function updateCartDisplay() {
            document.getElementById('cart-count').textContent = cart.length;
        }
        
        // โหลดสินค้าเมื่อหน้าเว็บพร้อม
        document.addEventListener('DOMContentLoaded', loadProducts);
    </script>
</body>
</html>'''
            else:
                # Default: Todo App
                return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✅ Todo List - สร้างด้วย AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header h1 { font-size: 3em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        
        .todo-form {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .todo-input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
        }
        
        .add-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .add-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .todos-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .todo-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            border-bottom: 1px solid #eee;
            transition: all 0.3s ease;
        }
        
        .todo-item:hover {
            background: #f8f9fa;
        }
        
        .todo-text {
            flex: 1;
            font-size: 1.1em;
        }
        
        .todo-actions {
            display: flex;
            gap: 10px;
        }
        
        .complete-btn, .delete-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .complete-btn {
            background: #2ecc71;
            color: white;
        }
        
        .delete-btn {
            background: #e74c3c;
            color: white;
        }
        
        .complete-btn:hover, .delete-btn:hover {
            transform: scale(1.1);
        }
        
        .completed {
            text-decoration: line-through;
            opacity: 0.6;
        }
        
        .empty-state {
            text-align: center;
            color: #666;
            padding: 40px;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Todo List</h1>
            <p>สร้างด้วย AI - ใช้งานได้จริง!</p>
        </div>
        
        <div class="todo-form">
            <div class="input-group">
                <input type="text" id="todoInput" class="todo-input" placeholder="เพิ่มงานใหม่...">
                <button onclick="addTodo()" class="add-btn">เพิ่มงาน ➕</button>
            </div>
        </div>
        
        <div class="todos-container">
            <div id="todosContainer">
                <div class="empty-state">
                    ยังไม่มีงาน - เพิ่มงานแรกของคุณ! 🚀
                </div>
            </div>
        </div>
    </div>

    <script>
        let todos = [];
        let nextId = 1;
        
        function addTodo() {
            const input = document.getElementById('todoInput');
            const text = input.value.trim();
            
            if (text) {
                todos.push({
                    id: nextId++,
                    text: text,
                    completed: false
                });
                
                input.value = '';
                renderTodos();
                
                // แสดงแอนิเมชันสำเร็จ
                input.style.background = '#d4edda';
                setTimeout(() => {
                    input.style.background = '';
                }, 500);
            }
        }
        
        function toggleTodo(id) {
            const todo = todos.find(t => t.id === id);
            if (todo) {
                todo.completed = !todo.completed;
                renderTodos();
            }
        }
        
        function deleteTodo(id) {
            todos = todos.filter(t => t.id !== id);
            renderTodos();
        }
        
        function renderTodos() {
            const container = document.getElementById('todosContainer');
            
            if (todos.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        ยังไม่มีงาน - เพิ่มงานแรกของคุณ! 🚀
                    </div>
                `;
                return;
            }
            
            container.innerHTML = todos.map(todo => `
                <div class="todo-item">
                    <div class="todo-text ${todo.completed ? 'completed' : ''}">${todo.text}</div>
                    <div class="todo-actions">
                        <button class="complete-btn" onclick="toggleTodo(${todo.id})">
                            ${todo.completed ? '↩️ เลิกทำ' : '✅ เสร็จ'}
                        </button>
                        <button class="delete-btn" onclick="deleteTodo(${todo.id})">
                            🗑️ ลบ
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        // เพิ่มงานเมื่อกด Enter
        document.getElementById('todoInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addTodo();
            }
        });
        
        // เพิ่มงานตัวอย่าง
        setTimeout(() => {
            todos.push(
                {id: nextId++, text: 'เรียน HTML, CSS, JavaScript', completed: false},
                {id: nextId++, text: 'สร้างโปรเจ็คแรก', completed: true},
                {id: nextId++, text: 'เผยแพร่งานสู่โลก', completed: false}
            );
            renderTodos();
        }, 1000);
    </script>
</body>
</html>'''
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .user-list, .item-list {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .user-item, .item-card {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        .form-group input {
            width: 100%;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .price {
            color: #28a745;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
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
                <div id="userList" class="user-list">
                    <div class="user-item">กำลังโหลด...</div>
                </div>
                
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
                <div id="itemList" class="item-list">
                    <div class="item-card">กำลังโหลด...</div>
                </div>
                
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
        
        <div class="footer">
            <p>✨ สร้างด้วย Lovable Clone AI - ระบบสร้างแอปอัตโนมัติ</p>
            <p>🕐 เวลาในการสร้าง: 30 วินาที | 📊 Database + API + Frontend พร้อมใช้งาน</p>
        </div>
    </div>

    <script>
        // โหลดข้อมูลเมื่อเริ่มต้น
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
                    userList.innerHTML = '<div class="user-item">ยังไม่มีผู้ใช้ในระบบ</div>';
                } else {
                    userList.innerHTML = users.map(user => 
                        `<div class="user-item">
                            <strong>${user.name}</strong><br>
                            📧 ${user.email}<br>
                            <small>เข้าร่วม: ${new Date(user.created_at).toLocaleDateString('th-TH')}</small>
                        </div>`
                    ).join('');
                }
            } catch (error) {
                console.error('Error loading users:', error);
            }
        }

        async function loadItems() {
            try {
                const response = await fetch('/api/items');
                const items = await response.json();
                
                const itemList = document.getElementById('itemList');
                if (items.length === 0) {
                    itemList.innerHTML = '<div class="item-card">ยังไม่มีสินค้าในระบบ</div>';
                } else {
                    itemList.innerHTML = items.map(item => 
                        `<div class="item-card">
                            <strong>${item.title}</strong><br>
                            ${item.description}<br>
                            <span class="price">฿${item.price}</span>
                        </div>`
                    ).join('');
                }
            } catch (error) {
                console.error('Error loading items:', error);
            }
        }

        async function addUser() {
            const name = document.getElementById('userName').value;
            const email = document.getElementById('userEmail').value;
            
            if (!name || !email) {
                alert('กรุณากรอกชื่อและอีเมล');
                return;
            }
            
            try {
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name, email })
                });
                
                if (response.ok) {
                    document.getElementById('userName').value = '';
                    document.getElementById('userEmail').value = '';
                    loadUsers();
                    alert('เพิ่มผู้ใช้สำเร็จ!');
                } else {
                    const error = await response.json();
                    alert(error.error);
                }
            } catch (error) {
                console.error('Error adding user:', error);
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
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ title, description, price })
                });
                
                if (response.ok) {
                    document.getElementById('itemTitle').value = '';
                    document.getElementById('itemDescription').value = '';
                    document.getElementById('itemPrice').value = '';
                    loadItems();
                    alert('เพิ่มสินค้าสำเร็จ!');
                } else {
                    alert('เกิดข้อผิดพลาด');
                }
            } catch (error) {
                console.error('Error adding item:', error);
                alert('เกิดข้อผิดพลาด');
            }
        }
    </script>
</body>
</html>'''
        
        return "# Mock code generated"

# Configuration
ROOT_DIR = Path("C:/agent")
GENERATED_DIR = ROOT_DIR / "generated_apps"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI App
app = FastAPI(title="Lovable Clone - Exciting Edition", description="🚀 AI App Generator with Exciting Effects!")

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

# Global instances
real_ai = RealAI()
active_sessions = {}
websocket_connections = {}

class ExcitingLovableAI:
    """AI Engine ที่น่าตื่นเต้น!"""
    
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
        
        # ใช้ Mock AI ตัดสินใจ
        decision = real_ai.chat_decide(session['messages'])
        
        if decision['action'] == 'build_app':
            # เริ่มสร้างแอป
            session['status'] = 'building'
            session['requirements'] = decision['requirements']
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
    
    async def build_app(self, requirements: Dict[str, Any], session_id: str, websocket: WebSocket = None) -> Dict[str, Any]:
        """สร้างแอปจริงพร้อม exciting effects"""
        
        app_id = f"app_{uuid.uuid4().hex[:8]}"
        app_dir = GENERATED_DIR / app_id
        app_dir.mkdir(exist_ok=True)
        
        try:
            # ส่งสถานะ exciting
            await self._send_exciting_status(websocket, "🎯", "กำลังวิเคราะห์ความต้องการ...")
            await asyncio.sleep(1)
            
            # 1. AI วิเคราะห์และวางแผน
            plan = real_ai.generate_plan(requirements)
            
            await self._send_exciting_status(websocket, "🧠", "AI กำลังออกแบบสถาปัตยกรรม...")
            await asyncio.sleep(1)
            
            # 2. สร้างฐานข้อมูล
            await self._send_exciting_status(websocket, "🗄️", "สร้างฐานข้อมูลแบบ real-time...")
            database_code = real_ai.generate_code("database", plan)
            await self._create_file_with_typing(websocket, "database.py", database_code, app_dir)
            
            # 3. สร้าง Backend
            await self._send_exciting_status(websocket, "🔧", "เขียน API Backend ด้วย Flask...")
            backend_code = real_ai.generate_code("backend", plan)
            await self._create_file_with_typing(websocket, "app.py", backend_code, app_dir)
            
            # 4. สร้าง Frontend
            await self._send_exciting_status(websocket, "🎨", "ออกแบบ Frontend สุดสวย...")
            frontend_code = real_ai.generate_code("frontend", plan)
            
            # สร้าง templates directory
            templates_dir = app_dir / "templates"
            templates_dir.mkdir(exist_ok=True)
            await self._create_file_with_typing(websocket, "index.html", frontend_code, templates_dir)
            
            # 5. สร้างไฟล์เสริม
            await self._send_exciting_status(websocket, "📦", "เตรียมไฟล์พร้อมใช้งาน...")
            await self._create_extras(app_dir, plan)
            
            await self._send_exciting_status(websocket, "✅", "แอปสร้างเสร็จแล้ว! 🎉")
            
            return {
                'app_id': app_id,
                'app_path': str(app_dir),
                'plan': plan,
                'files_created': ['database.py', 'app.py', 'templates/index.html', 'requirements.txt', 'start.bat'],
                'status': 'completed'
            }
            
        except Exception as e:
            await self._send_exciting_status(websocket, "❌", f"เกิดข้อผิดพลาด: {str(e)}")
            raise
    
    async def _send_exciting_status(self, websocket: WebSocket, icon: str, status: str):
        """ส่งสถานะแบบ exciting"""
        if websocket:
            try:
                await websocket.send_json({
                    'type': 'exciting_status',
                    'icon': icon,
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                })
            except:
                pass
    
    async def _create_file_with_typing(self, websocket: WebSocket, filename: str, content: str, directory: Path):
        """สร้างไฟล์พร้อม typing effect"""
        if websocket:
            try:
                await websocket.send_json({
                    'type': 'file_typing_start',
                    'filename': filename,
                    'total_chars': len(content)
                })
                
                # ส่งโค้ดทีละส่วน
                chunk_size = 50
                for i in range(0, len(content), chunk_size):
                    chunk = content[i:i + chunk_size]
                    await websocket.send_json({
                        'type': 'file_typing_chunk',
                        'filename': filename,
                        'chunk': chunk,
                        'progress': (i + chunk_size) / len(content)
                    })
                    await asyncio.sleep(0.03)  # 30ms delay สำหรับ typing effect
                
                await websocket.send_json({
                    'type': 'file_typing_complete',
                    'filename': filename,
                    'content': content
                })
                
            except:
                pass
        
        # บันทึกไฟล์จริง
        file_path = directory / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    async def _create_extras(self, app_dir: Path, plan: Dict):
        """สร้างไฟล์เสริม"""
        
        # requirements.txt
        requirements_content = """flask
flask-cors
"""
        req_file = app_dir / "requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        
        # start.bat
        start_content = f"""@echo off
echo 🚀 Starting {plan.get('app_name', 'Amazing App')}...
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🗄️ Setting up database...
python database.py

echo 🌟 Starting web server...
echo 📍 Open: http://localhost:5000
python app.py
"""
        start_file = app_dir / "start.bat"
        with open(start_file, 'w', encoding='utf-8') as f:
            f.write(start_content)
        
        # README.md
        readme_content = f"""# 🚀 {plan.get('app_name', 'Amazing App')}

{plan.get('description', 'แอปสุดเจ๋งที่สร้างด้วย AI')}

## ✨ Features
- 🗄️ SQLite Database
- 🔧 Flask REST API  
- 🎨 Beautiful Frontend
- 📱 Responsive Design

## 🚀 วิธีรัน

### วิธีที่ 1: ใช้ start.bat (ง่ายสุด)
```
ดับเบิลคลิก start.bat
```

### วิธีที่ 2: รันเอง
```bash
# 1. ติดตั้ง dependencies
pip install -r requirements.txt

# 2. ตั้งค่าฐานข้อมูล
python database.py

# 3. รันเซิร์ฟเวอร์
python app.py
```

### 🌐 เปิดเบราเซอร์
http://localhost:5000

## 🎯 API Endpoints
- `GET /api/users` - ดึงรายการผู้ใช้
- `POST /api/users` - เพิ่มผู้ใช้
- `GET /api/items` - ดึงรายการสินค้า
- `POST /api/items` - เพิ่มสินค้า

## 🔧 Tech Stack
- **Backend:** Flask + SQLite
- **Frontend:** HTML + CSS + JavaScript
- **Database:** SQLite
- **Style:** Responsive CSS Grid

---
## ⚡ สร้างด้วย Lovable Clone AI
🕐 เวลาสร้าง: 30 วินาที | 🤖 AI-Powered | ✨ Ready to Use
"""
        readme_file = app_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

# Global AI instance
exciting_ai = ExcitingLovableAI()

@app.get("/")
async def root():
    """Serve the exciting interface"""
    interface_file = ROOT_DIR / "lovable_split_interface.html"
    if interface_file.exists():
        return FileResponse(str(interface_file))
    return {"message": "🚀 Lovable Clone - Exciting Edition!", "status": "ready"}

@app.post("/chat")
async def chat_endpoint(message_request: ChatMessage):
    """Chat with exciting AI"""
    
    session_id = message_request.session_id or f"session_{uuid.uuid4().hex[:8]}"
    
    try:
        result = await exciting_ai.chat(message_request.message, session_id)
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
    """WebSocket for exciting real-time updates"""
    await websocket.accept()
    websocket_connections[session_id] = websocket
    
    try:
        while True:
            # รอรับ build request
            data = await websocket.receive_json()
            
            if data.get('action') == 'build_app':
                requirements = data.get('requirements', {})
                
                # สร้างแอปพร้อม exciting effects
                result = await exciting_ai.build_app(requirements, session_id, websocket)
                
                # ส่งผลลัพธ์สุดท้าย
                await websocket.send_json({
                    'type': 'app_completed',
                    'result': result
                })
    
    except WebSocketDisconnect:
        if session_id in websocket_connections:
            del websocket_connections[session_id]

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

@app.get("/test")
async def test():
    """ทดสอบระบบ"""
    return {"message": "🚀 Exciting Lovable Clone is working!", "status": "ready"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Exciting Lovable Clone AI...")
    print("✨ With amazing visual effects!")
    print("📍 Server: http://localhost:8006")
    uvicorn.run(app, host="0.0.0.0", port=8006)