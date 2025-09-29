#!/usr/bin/env python3
"""
🚀 Lovable Clone - Real AI App Generator
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
import shutil

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
# Real OpenAI Integration  
try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()  # โหลดค่าจาก .env file
    OPENAI_AVAILABLE = True
except ImportError as e:
    OPENAI_AVAILABLE = False
    print(f"⚠️ Missing dependencies: {e}")

# Optional Gemini (Google Generative AI)
GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai  # type: ignore
    GEMINI_AVAILABLE = True
except Exception as _ge:
    GEMINI_AVAILABLE = False

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class RealAI:
    """Real AI integration with provider toggle (OpenAI/Gemini) and fallback"""

    def __init__(self, api_key: str = None):
        self.provider = (os.getenv('AI_PROVIDER') or 'openai').strip().lower()
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_real_ai = False
        self.client = None
        if OPENAI_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.use_real_ai = True
                print(f"🚀 Using REAL OpenAI API! (key: ...{self.api_key[-10:]})")
            except Exception as oe:
                print(f"⚠️ OpenAI init failed: {oe}")
        else:
            print("🤖 OpenAI demo mode - set OPENAI_API_KEY for real AI")
        # Gemini
        self.gemini_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        self.gemini_ready = False
        self.gemini_model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        if GEMINI_AVAILABLE and self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)  # type: ignore
                self.gemini_ready = True
                print(f"🎨 Gemini ready (model={self.gemini_model_name})")
            except Exception as ge:
                print(f"⚠️ Gemini init failed: {ge}")

    def _gemini_generate_text(self, prompt: str):
        if not getattr(self, 'gemini_ready', False):
            return None
        try:
            model = genai.GenerativeModel(self.gemini_model_name)  # type: ignore
            resp = model.generate_content(prompt)
            text = getattr(resp, 'text', None)
            if not text and getattr(resp, 'candidates', None):
                try:
                    text = resp.candidates[0].content.parts[0].text
                except Exception:
                    text = None
            return text
        except Exception as e:
            print(f"⚠️ Gemini generate error: {e}")
            return None

    def generate_code(self, file_type: str, plan: Dict) -> str:
        """สร้างโค้ดด้วย AI จริงๆ (OpenAI/Gemini ตามงาน)"""
        if file_type != "frontend":
            return "# Backend/Database code would go here"
        app_name = plan.get('app_name', 'Amazing App')
        description = plan.get('description', 'แอปที่สร้างด้วย AI')
        app_type = plan.get('app_type', 'webapp')
        features = plan.get('features', [])
        ui_theme = plan.get('ui_theme', 'modern')
        # Try Gemini for frontend
        prefer_gemini = (self.provider in ["gemini", "hybrid"]) and getattr(self, 'gemini_ready', False)
        if prefer_gemini:
            prompt = f"ออกแบบหน้าเว็บ Single-Page HTML เต็มไฟล์:\nชื่อแอป: {app_name}\nประเภท: {app_type}\nคำอธิบาย: {description}\nฟีเจอร์: {', '.join(features)}\nธีม: {ui_theme}\nข้อกำหนด: ส่งกลับ HTML เต็ม (ห้ามมี ```), CSS สวย, JS ใช้งานได้"
            ai_code = (self._gemini_generate_text(prompt) or '').strip()
            if ai_code.startswith('```html'):
                ai_code = ai_code[len('```html'):].strip('`\n ')
            elif ai_code.startswith('```'):
                ai_code = ai_code.strip('`\n ')
            if '<html' in ai_code or '<!DOCTYPE html' in ai_code:
                return ai_code
        # ใช้ OpenAI ถ้ามี
        if self.use_real_ai and self.client:
            try:
                prompt = f"""สร้าง Single-Page Web Application ที่สมบูรณ์:

ชื่อแอป: {app_name}
ประเภท: {app_type}
คำอธิบาย: {description}
ฟีเจอร์: {', '.join(features)}
ธีม: {ui_theme}

สร้าง HTML5 ที่มี:
- CSS สวยงามในแบบ {ui_theme}
- JavaScript ที่ทำงานได้จริง
- ฟีเจอร์ครบตาม {features}
- ใช้ localStorage สำหรับเก็บข้อมูล
- ภาษาไทยและ emoji
- Responsive design
- Animation effects
- Error handling

ส่งกลับเฉพาะโค้ด HTML เต็ม ไม่ต้องคำอธิบาย:"""

                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",  # ใช้ model ที่เหมาะสมกว่า
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=4000
                )
                
                ai_code = response.choices[0].message.content.strip()
                
                # ทำความสะอาดโค้ดที่ AI ส่งมา
                if ai_code.startswith('```html'):
                    ai_code = ai_code.replace('```html', '').replace('```', '')
                elif ai_code.startswith('```'):
                    ai_code = ai_code.replace('```', '', 2)
                
                ai_code = ai_code.strip()
                
                print(f"🎨 OpenAI Generated {len(ai_code)} chars of code for {app_name}")
                return ai_code
                
            except Exception as e:
                print(f"⚠️ AI Code Generation Error: {e}")
                print("Falling back to template...")
                
                # ลบ markdown code block ถ้ามี
                try:
                    if '```html' in ai_code:
                        ai_code = ai_code.split('```html')[1].split('```')[0].strip()
                    elif '```' in ai_code:
                        ai_code = ai_code.split('```')[1].split('```')[0].strip()
                except Exception:
                    pass
                
                print(f"🤖 AI Generated {len(ai_code)} characters of code")
                
                # ตรวจสอบว่าเป็น HTML ที่ถูกต้อง
                if '<!DOCTYPE html>' in ai_code or '<html' in ai_code:
                    return ai_code
                else:
                    print("❌ AI code doesn't look like valid HTML, using template")
        
        # Fallback ใช้ template
        if file_type == "frontend":
            if app_type == 'shop_app':
                return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛍️ ร้านค้าออนไลน์ - สร้างด้วย AI</title>
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
        
        <div class="products-grid">
            <div class="product-card">
                <div class="product-title">กาแฟอเมริกาโน</div>
                <div class="product-description">กาแฟดำสไตล์อเมริกัน หอมกรุ่น</div>
                <div class="product-price">฿45</div>
                <button class="add-to-cart" onclick="addToCart('กาแฟอเมริกาโน', 45)">
                    เพิ่มลงตะกร้า 🛒
                </button>
            </div>
            
            <div class="product-card">
                <div class="product-title">ลาเต้</div>
                <div class="product-description">กาแฟนมสุดอร่อย หวานมัน</div>
                <div class="product-price">฿55</div>
                <button class="add-to-cart" onclick="addToCart('ลาเต้', 55)">
                    เพิ่มลงตะกร้า 🛒
                </button>
            </div>
            
            <div class="product-card">
                <div class="product-title">เค้กช็อกโกแลต</div>
                <div class="product-description">เค้กหวานมันเข้มข้น น่าลิ้มลอง</div>
                <div class="product-price">฿75</div>
                <button class="add-to-cart" onclick="addToCart('เค้กช็อกโกแลต', 75)">
                    เพิ่มลงตะกร้า 🛒
                </button>
            </div>
        </div>
    </div>

    <script>
        let cart = [];
        
        function addToCart(name, price) {
            cart.push({name, price});
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
        
        return "Default file content"

    def chat_decide(self, messages: List[Dict]) -> Dict[str, Any]:
        """Decide whether to ask a clarifying question or proceed to build.

        - Demo mode: simple heuristics
        - Real AI (OpenAI): ask for compact JSON decision
        """
        # Heuristic path first (works even without keys/models)
        try:
            user_msg = (messages[-1]['content'] if messages else '').lower()
        except Exception:
            user_msg = ''

        if not (self.use_real_ai and self.client):
            intent = 'webapp'
            features: List[str] = []
            if any(k in user_msg for k in ['instagram', 'social', 'ig']):
                intent = 'social'; features = ['โพสต์รูปภาพ', 'ฟีดข่าว', 'กดถูกใจ', 'คอมเมนต์']
            elif any(k in user_msg for k in ['shop', 'ร้าน', 'ecommerce', 'ขาย']):
                intent = 'website'; features = ['แคตตาล็อกสินค้า', 'ตะกร้าสินค้า', 'ติดต่อ']
            elif any(k in user_msg for k in ['todo', 'งาน', 'task']):
                intent = 'webapp'; features = ['เพิ่มงาน', 'ลบงาน', 'ทำเครื่องหมายเสร็จ']
            if len(user_msg.strip()) < 10:
                return {
                    "action": "ask_question",
                    "message": "อยากได้แอปแนวไหน (social/website/webapp)? ระบุฟีเจอร์หลัก 3-5 ข้อ และโทนสี/สไตล์ครับ",
                    "requirements": {}
                }
            return {
                "action": "build_app",
                "message": "เข้าใจแล้ว! เดี๋ยวจัดสรรแผนและเริ่มสร้างให้เลย 🚀",
                "requirements": {
                    "app_type": intent,
                    "features": features,
                    "ui_theme": "modern",
                }
            }

        # Real AI (OpenAI) decision
        try:
            system_prompt = (
                "คุณคือผู้ช่วยออกแบบระบบและเว็บแอป เก็บ requirement แบบกระชับและตัดสินใจ: "
                "หากข้อมูลไม่พอให้ถาม 1 ข้อที่ตรงประเด็น หากพอแล้วให้ action=build_app และสรุป requirements. "
                "ตอบเป็น JSON ที่มี action, message และ (ถ้ามี) requirements."
            )
            resp = self.client.chat.completions.create(
                model=os.getenv('OPENAI_DECISION_MODEL', 'gpt-4o-mini'),
                messages=[{"role": "system", "content": system_prompt}, *messages],
                temperature=0.2,
                max_tokens=500,
            )
            content = resp.choices[0].message.content or ""
            json_part = content
            if '```json' in content:
                json_part = content.split('```json', 1)[1].split('```', 1)[0]
            elif content.find('{') != -1 and content.rfind('}') != -1:
                json_part = content[content.find('{'):content.rfind('}')+1]
            try:
                data = json.loads(json_part)
                if 'action' not in data or 'message' not in data:
                    raise ValueError('missing keys')
                if data.get('requirements') is None:
                    data['requirements'] = {}
                return data
            except Exception:
                return {"action": "ask_question", "message": content, "requirements": {}}
        except Exception as e:
            print(f"⚠️ OpenAI decision error: {e}")
            return {"action": "ask_question", "message": "ช่วยบอกประเภทแอปและฟีเจอร์หลัก 3-5 ข้อครับ", "requirements": {}}

    def generate_plan(self, requirements: Dict) -> Dict:
        """Normalize requirements into a simple plan usable by generators."""
        req = requirements or {}
        app_type = (req.get('app_type') or 'webapp').lower()
        app_name = req.get('app_name') or (
            'Social App' if any(k in app_type for k in ['social','instagram','ig']) else
            'Website' if any(k in app_type for k in ['website','portfolio','blog']) else
            'AI Web App'
        )
        description = req.get('description') or 'แอปที่สร้างโดย AI พร้อมใช้งานจริง'
        features = req.get('features') or (
            ['โพสต์รูปภาพ', 'ฟีดข่าว', 'กดถูกใจ', 'คอมเมนต์'] if 'social' in app_type else
            ['หน้า Home', 'เกี่ยวกับ', 'บริการ', 'ราคา', 'ติดต่อเรา'] if any(k in app_type for k in ['website','portfolio','blog']) else
            ['เพิ่มข้อมูล', 'แก้ไข', 'ลบ', 'ค้นหา']
        )
        ui_theme = req.get('ui_theme') or 'modern'
        return {
            'app_name': app_name,
            'description': description,
            'app_type': app_type,
            'features': features,
            'ui_theme': ui_theme,
        }

    def generate_blueprint(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Produce a minimal blueprint (features + data models) for scaffolding."""
        app_type = (plan.get('app_type') or '').lower()
        features = plan.get('features') or []
        data_models: Dict[str, Dict[str, str]] = {}
        if 'social' in app_type:
            data_models = {
                'users': {'username': 'string', 'name': 'string', 'avatar': 'string'},
                'posts': {'user': 'string', 'img': 'string', 'caption': 'text', 'likes': 'integer', 'ts': 'integer'},
                'comments': {'post_id': 'integer', 'user': 'string', 'text': 'text'}
            }
        else:
            data_models = {
                'items': {'name': 'string', 'description': 'text', 'price': 'float'}
            }
        return {
            'name': plan.get('app_name', 'AI App'),
            'description': plan.get('description', ''),
            'features': features,
            'data_models': data_models,
        }

# เซิร์ฟเวอร์
# Ensure generated apps directory exists before mounting static files
BASE_GENERATED_DIR = Path("generated_apps")
BASE_GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="🚀 Lovable Clone - AI App Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base HTTP URL for linking generated apps (configurable)
BASE_HTTP_URL = os.getenv("BASE_HTTP_URL", "http://localhost:8001")

# Serve generated apps over HTTP at /apps
generated_dir = Path("generated_apps")
generated_dir.mkdir(exist_ok=True)
app.mount("/apps", StaticFiles(directory=str(generated_dir)), name="generated_apps")

# Serve generated apps over HTTP for easy preview
app.mount("/generated_apps", StaticFiles(directory=str(BASE_GENERATED_DIR)), name="generated_apps")

# Additional simple site output for builder flow
SITES_WEBROOT = Path("generated_sites")
SITES_WEBROOT.mkdir(parents=True, exist_ok=True)
app.mount("/sites", StaticFiles(directory=str(SITES_WEBROOT), html=True), name="sites")
# Mount /data if exists
if Path('data').exists():
    app.mount("/data", StaticFiles(directory='data'), name="data")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"❌ Validation Error: {exc}")
    print(f"📨 Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid request format",
            "details": str(exc.errors()),
            "message": "กรุณาตรวจสอบรูปแบบข้อมูลที่ส่งมา"
        }
    )

# แล้ว AI
real_ai = RealAI()

# เก็บ session
sessions = {}

# ------------------- Simple builder endpoint -------------------
class PlanBuildReq(BaseModel):
    prompt: str
    slug: Optional[str] = None

@app.post("/plan_build")
async def plan_build(req: PlanBuildReq):
    """รับ requirement แล้วสร้างไฟล์ HTML แบบง่าย และคืน URL สำหรับเปิดดูทันที"""
    try:
        slug = req.slug or f"site_{int(time.time())}"
        site_dir = SITES_WEBROOT / slug
        site_dir.mkdir(parents=True, exist_ok=True)

        html = f"""<!doctype html>
<html lang=\"th\"><meta charset=\"utf-8\">
<title>{req.prompt}</title>
<style>body{{font-family:system-ui;background:#0f1220;color:#e9eef5;padding:24px}} .card{{background:#151925;border:1px solid #23283b;border-radius:12px;padding:16px;max-width:820px}}</style>
<div class=\"card\">
<h1>✅ สร้างจาก: {req.prompt}</h1>
<p>นี่คือหน้าเว็บที่ระบบสร้างขึ้นอัตโนมัติ (AgentPro)</p>
<p>เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
</html>"""
        (site_dir / "index.html").write_text(html, encoding="utf-8")

        web_url = f"{BASE_HTTP_URL}/sites/{slug}/index.html"
        return {"success": True, "web_url": web_url, "slug": slug}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

class ExcitingLovableAI:
    """AI ที่สร้างแอปแบบ Exciting พร้อม Realtime Effects!"""
    
    def __init__(self):
        self.app_counter = 0
        self.workspace_dir = Path("generated_apps")
        self.workspace_dir.mkdir(exist_ok=True)

    # ---------- Utility helpers ----------
    def _safe_write(self, base_dir: Path, rel_path: str, content: str):
        file_path = base_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path

    def _zip_app(self, app_dir: Path) -> Path:
        zip_base = app_dir.with_suffix('')  # remove trailing slash
        archive_path = shutil.make_archive(str(zip_base), 'zip', root_dir=str(app_dir))
        return Path(archive_path)

    def _validate_python(self, file_path: Path) -> bool:
        try:
            compile(open(file_path, 'r', encoding='utf-8').read(), str(file_path), 'exec')
            return True
        except Exception as e:
            print(f"⚠️ Python syntax check failed for {file_path}: {e}")
            return False

    # ---------- Project generators ----------
    def _gen_static_site(self, app_dir: Path, plan: Dict) -> Dict[str, str]:
                app_name = plan.get('app_name', 'Amazing App')
                desc = plan.get('description', 'แอปสุดเจ๋งที่สร้างด้วย AI')
                theme = plan.get('ui_theme', 'modern')
                primary = '#667eea'
                secondary = '#764ba2'

                # Shared styles and scripts
                styles_header = f":root{{--primary:{primary};--secondary:{secondary}}}\n"
                styles_rest = """*{box-sizing:border-box}body{margin:0;font-family:Segoe UI,system-ui,-apple-system}
.topbar{display:flex;gap:16px;align-items:center;padding:12px 16px;background:#111;color:#fff;position:sticky;top:0}
.topbar a{color:#61dafb;text-decoration:none;padding:6px 10px;border-radius:6px}
.topbar a.active{background:#094771;color:#fff}
.container{max-width:1080px;margin:0 auto;padding:16px}
.hero{padding:64px;text-align:center;background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff}
.btn{display:inline-block;margin-top:16px;background:#fff;color:#333;padding:10px 16px;border-radius:8px;text-decoration:none}
.section{max-width:960px;margin:40px auto;padding:0 16px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.card{background:#fff;border-radius:12px;padding:16px;box-shadow:0 8px 20px rgba(0,0,0,.15)}
ul{line-height:1.8}
textarea,input,button{font:inherit}
footer{padding:24px;text-align:center;color:#777}
table{width:100%;border-collapse:collapse}
th,td{border:1px solid #eee;padding:10px}
h1,h2,h3{margin:10px 0}
"""
                styles_css = styles_header + styles_rest

                script_js = """document.addEventListener('DOMContentLoaded',()=>{
    // Highlight active nav
    const page=(location.pathname.split('/').pop())||'index.html';
    document.querySelectorAll('.nav a').forEach(a=>{ if(a.getAttribute('href')===page){ a.classList.add('active'); }});

    // Index features injection
    if(page==='index.html'){
        const feats=(window.__PLAN__?.features)||['ใช้งานง่าย','สวยงาม','รวดเร็ว'];
        const ul=document.getElementById('featuresList');
        if(ul){ feats.forEach(f=>{ const li=document.createElement('li'); li.textContent='• '+f; ul.appendChild(li); }); }
    }
});
"""

                year = datetime.now().strftime('%Y')
                nav = '''<div class="topbar nav"><strong>🏷️ {app}</strong>
    <a href="index.html">Home</a>
    <a href="about.html">About</a>
    <a href="services.html">Services</a>
    <a href="pricing.html">Pricing</a>
    <a href="blog.html">Blog</a>
    <a href="contact.html">Contact</a>
</div>'''.replace('{app}', app_name)

                # Pages
                index_html = f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{app_name} - Home</title>
    <link rel="stylesheet" href="styles.css" />
    <script>window.__PLAN__ = {json.dumps(plan, ensure_ascii=False)};</script>
    <script defer src="assets.js"></script>
    <script defer src="script.js"></script>
    <meta name="description" content="{desc}" />
    <meta name="theme-color" content="{primary}" />
</head>
<body>
    {nav}
    <header class="hero">
        <h1>🎉 {app_name}</h1>
        <p>{desc}</p>
        <a class="btn" href="#features">ดูฟีเจอร์</a>
    </header>
    <main class="container">
        <section id="features" class="section">
            <h2>ฟีเจอร์เด่น</h2>
            <ul id="featuresList"></ul>
        </section>
        <section class="section">
            <h2>ไฮไลต์</h2>
            <div class="cards">
                <div class="card"><h3>⚡ เร็ว</h3><p>โครงสร้างพร้อมใช้งานทันที</p></div>
                <div class="card"><h3>🎨 สวย</h3><p>ดีไซน์ทันสมัย รองรับทุกหน้าจอ</p></div>
                <div class="card"><h3>🧩 ขยายง่าย</h3><p>พร้อมต่อยอดเป็นระบบใหญ่</p></div>
            </div>
        </section>
    </main>
    <footer>สร้างด้วย AI · {year}</footer>
    </body>
</html>'''

                about_html = f'''<!DOCTYPE html>
<html lang="th"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - About</title>
    <link rel="stylesheet" href="styles.css"><script defer src="script.js"></script>
</head><body>
    {nav}
    <main class="container">
        <h1>เกี่ยวกับเรา</h1>
        <p>{desc}</p>
        <div class="cards">
            <div class="card"><h3>วิสัยทัศน์</h3><p>ยกระดับการสร้างระบบด้วย AI</p></div>
            <div class="card"><h3>พันธกิจ</h3><p>สร้างผลงานที่ใช้งานได้จริง และน่าประทับใจ</p></div>
            <div class="card"><h3>ทีมงาน</h3><p>ผู้เชี่ยวชาญด้านระบบและ UX</p></div>
        </div>
    </main>
    <footer>สร้างด้วย AI · {year}</footer>
</body></html>'''

                # Services maps from features or defaults
                features = plan.get('features') or ['ออกแบบ UI/UX', 'พัฒนาเว็บแอป', 'วิเคราะห์ระบบ', 'อินทิเกรต API', 'ทดสอบและดูแลระบบ']
                services_items = ''.join([f'<li>• {f}</li>' for f in features])
                services_html = f'''<!DOCTYPE html>
<html lang="th"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Services</title>
    <link rel="stylesheet" href="styles.css"><script defer src="script.js"></script>
</head><body>
    {nav}
    <main class="container">
        <h1>บริการของเรา</h1>
        <ul>{services_items}</ul>
    </main>
    <footer>สร้างด้วย AI · {year}</footer>
</body></html>'''

                pricing_html = f'''<!DOCTYPE html>
<html lang="th"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Pricing</title>
    <link rel="stylesheet" href="styles.css"><script defer src="script.js"></script>
</head><body>
    {nav}
    <main class="container">
        <h1>แพ็กเกจราคา</h1>
        <div class="cards">
            <div class="card"><h3>Starter</h3><p>เริ่มต้นโครงการ</p><h2>฿9,900</h2></div>
            <div class="card"><h3>Pro</h3><p>ระบบพร้อมใช้งาน</p><h2>฿29,900</h2></div>
            <div class="card"><h3>Enterprise</h3><p>ปรับแต่งเต็มรูปแบบ</p><h2>ติดต่อเรา</h2></div>
        </div>
    </main>
    <footer>สร้างด้วย AI · {year}</footer>
</body></html>'''

                blog_html = f'''<!DOCTYPE html>
<html lang="th"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Blog</title>
    <link rel="stylesheet" href="styles.css"><script defer src="script.js"></script>
</head><body>
    {nav}
    <main class="container">
        <h1>บล็อก</h1>
        <div class="cards">
            <div class="card"><h3>เริ่มต้นกับ {app_name}</h3><p>ทิปส์การใช้งานและโครงสร้างโปรเจค</p></div>
            <div class="card"><h3>แนวทางออกแบบ UI</h3><p>หลักคิดเรื่องสี ฟอนต์ และสเปซ</p></div>
            <div class="card"><h3>ขยายเป็น Enterprise</h3><p>โมดูล หน้าจอ และเวิร์กโฟลว์</p></div>
        </div>
    </main>
    <footer>สร้างด้วย AI · {year}</footer>
</body></html>'''

                contact_html = f'''<!DOCTYPE html>
<html lang="th"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Contact</title>
    <link rel="stylesheet" href="styles.css"><script defer src="script.js"></script>
</head><body>
    {nav}
    <main class="container">
        <h1>ติดต่อเรา</h1>
        <p>กรอกข้อมูลเพื่อให้เราติดต่อกลับ</p>
        <div class="card">
            <form onsubmit="alert('ขอบคุณครับ!'); return false;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                    <input placeholder="ชื่อ" required>
                    <input placeholder="อีเมล" type="email" required>
                </div>
                <textarea style="width:100%;margin-top:12px;height:120px" placeholder="รายละเอียด"></textarea>
                <button class="btn" style="margin-top:12px">ส่งข้อความ</button>
            </form>
        </div>
    </main>
    <footer>สร้างด้วย AI · {year}</footer>
</body></html>'''

                # Discover local images under /data/**/raw and expose via assets.js
                try:
                    assets = self._discover_local_images()
                except Exception:
                    assets = []
                files: Dict[str, str] = {
                        'index.html': index_html,
                        'about.html': about_html,
                        'services.html': services_html,
                        'pricing.html': pricing_html,
                        'blog.html': blog_html,
                        'contact.html': contact_html,
                        'styles.css': styles_css,
                        'script.js': script_js,
                        'assets.js': 'window.__ASSETS__ = ' + json.dumps(assets, ensure_ascii=False) + ';',
                        'plan.json': json.dumps(plan, ensure_ascii=False, indent=2)
                }

                for rel, content in files.items():
                        self._safe_write(app_dir, rel, content)
                return files

    def _gen_spa(self, app_dir: Path, plan: Dict) -> Dict[str, str]:
        app_name = plan.get('app_name', 'AI Web App')
        index_html = f'''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{app_name}</title>
  <link rel="stylesheet" href="styles.css"><script defer src="app.js"></script>
</head>
<body>
  <nav class="topbar"><span>{app_name}</span><a href="#/">หน้าแรก</a><a href="#/todos">งาน</a></nav>
  <main id="app"></main>
</body>
</html>'''
        styles = ".topbar{display:flex;gap:16px;padding:12px;background:#222;color:#fff}a{color:#61dafb;text-decoration:none}body{margin:0;font-family:Segoe UI}#app{padding:16px}"
        app_js = """const routes={\n  '/': ()=>'<h1>สวัสดี 👋</h1><p>นี่คือแอปแบบ Single Page</p>',\n  '/todos': ()=>window.renderTodos()\n};\nfunction router(){const hash=location.hash.replace('#','')||'/';const view=routes[hash]||(()=>'<h1>ไม่พบหน้า</h1>');document.getElementById('app').innerHTML=view()}\nwindow.addEventListener('hashchange',router);window.addEventListener('load',router);\nwindow.renderTodos=()=>{\n  let todos=JSON.parse(localStorage.getItem('todos')||'[]');\n  const el=document.createElement('div');\n  el.innerHTML=`<h2>Todo List</h2><input id=t placeholder='เพิ่มงาน...'><button id=b>เพิ่ม</button><ul id=list></ul>`;\n  function paint(){list.innerHTML='';todos.forEach((t,i)=>{const li=document.createElement('li');li.textContent=t;li.onclick=()=>{todos.splice(i,1);save()};list.appendChild(li)})}\n  function save(){localStorage.setItem('todos',JSON.stringify(todos));paint()}\n  el.querySelector('#b').onclick=()=>{const v=el.querySelector('#t').value.trim();if(v){todos.push(v);save();el.querySelector('#t').value=''}}\n  document.getElementById('app').innerHTML='';document.getElementById('app').appendChild(el);paint();\n};\n"""
        files = {'index.html': index_html, 'styles.css': styles, 'app.js': app_js, 'plan.json': json.dumps(plan, ensure_ascii=False, indent=2)}
        for rel, content in files.items():
            self._safe_write(app_dir, rel, content)
        return files

    def _gen_social_spa(self, app_dir: Path, plan: Dict) -> Dict[str, str]:
        app_name = plan.get('app_name', 'AI Social App')
        # HTML with top bar and bottom nav
        index_html = f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name}</title>
    <link rel="stylesheet" href="styles.css"><script defer src="assets.js"></script><script defer src="app.js"></script>
    <meta name="theme-color" content="#000" />
    <style>body{{margin:0}}</style>
</head>
<body>
    <header class="topbar"><div class="brand">📸 {app_name}</div><input class="search" placeholder="ค้นหา" /></header>
    <main id="app" class="viewport"></main>
    <nav class="bottombar">
        <a href="#/feed">🏠</a>
        <a href="#/explore">🔎</a>
        <a href="#/create">➕</a>
        <a href="#/inbox">✉️</a>
        <a href="#/notifications">🔔</a>
        <a href="#/profile">👤</a>
    </nav>
</body>
</html>'''
        styles = """
body{font-family:Segoe UI,system-ui,-apple-system;background:#000;color:#fff}
.topbar{position:sticky;top:0;background:#111;color:#fff;display:flex;gap:12px;align-items:center;padding:10px 12px;border-bottom:1px solid #222;z-index:10}
.topbar .brand{font-weight:700}
.topbar .search{flex:1;background:#222;border:1px solid #333;color:#ddd;padding:8px 10px;border-radius:8px}
.viewport{padding-bottom:56px}
.bottombar{position:fixed;bottom:0;left:0;right:0;background:#111;border-top:1px solid #222;display:flex;justify-content:space-around;padding:8px 0}
.bottombar a{color:#bbb;text-decoration:none;font-size:20px}
.feed{max-width:600px;margin:0 auto;padding:8px}
.post{background:#111;border:1px solid #222;border-radius:12px;margin:12px 0;overflow:hidden}
.post .head{display:flex;gap:8px;align-items:center;padding:10px}
.post .avatar{width:32px;height:32px;border-radius:50%;background:#333}
.post .img{width:100%;background:#000;display:block}
.post .actions{display:flex;gap:12px;padding:8px 10px}
.post .meta{color:#bbb;padding:0 10px 10px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}
.grid img{width:100%;height:100%;object-fit:cover;display:block}
.composer{max-width:600px;margin:0 auto;padding:12px}
.composer .card{background:#111;border:1px solid #222;border-radius:12px;padding:12px}
.list{max-width:600px;margin:0 auto}
.item{display:flex;justify-content:space-between;padding:12px;border-bottom:1px solid #222}
button{background:#222;border:1px solid #444;color:#eee;padding:6px 10px;border-radius:8px;cursor:pointer}
input,textarea{background:#000;border:1px solid #333;color:#eee;border-radius:8px;padding:8px}
"""
        app_js = """
// Simple SPA router and mock data
const state = JSON.parse(localStorage.getItem('social_state')||'{}');
if(!state.currentUser){ state.currentUser={username:'you', name:'คุณ', avatar:''}; }
if(!state.users){ state.users=[state.currentUser,{username:'alice',name:'Alice'},{username:'bob',name:'Bob'}]; }
if(!state.posts){
    state.posts=[
        {id: 1, user: "alice", img: "https://picsum.photos/seed/a/600/600", caption: "เช้าๆ", likes: 3, liked: false, comments: [{user: "bob", text: "สวย!"}], ts: Date.now() - 86400000},
        {id: 2, user: "bob", img: "https://picsum.photos/seed/b/600/600", caption: "คาเฟ่", likes: 1, liked: false, comments: [], ts: Date.now() - 3600000}
    ];
}
if(!state.notifications){ state.notifications=[{id:1,text:'alice ติดตามคุณ'},{id:2,text:'bob ถูกใจโพสต์ของคุณ'}]; }
if(!state.messages){ state.messages=[{id:1,with:'alice',last:'เจอกันพรุ่งนี้นะ'},{id:2,with:'bob',last:'ส่งรูปมาให้ดูหน่อย'}]; }
save();

function save(){ localStorage.setItem('social_state', JSON.stringify(state)); }
function h(html){ const d=document.createElement('div'); d.innerHTML=html.trim(); return d.firstChild; }
function timeAgo(ts){ const d=(Date.now()-ts)/1000; if(d<60) return 'เมื่อครู่'; if(d<3600) return Math.floor(d/60)+' นาที'; if(d<86400) return Math.floor(d/3600)+' ชม.'; return Math.floor(d/86400)+' วัน'; }

const routes={
    '/feed': renderFeed,
    '/explore': renderExplore,
    '/create': renderCreate,
    '/inbox': renderInbox,
    '/notifications': renderNotifications,
    '/profile': renderProfile
};

function router(){ const hash=(location.hash||'#/feed').replace('#',''); const view=routes[hash]||renderFeed; view(); }
window.addEventListener('hashchange',router); window.addEventListener('load',router);

function renderRoute(r){ const app=document.getElementById('app'); app.innerHTML=''; const cont=h('<div class="container"></div>');
    (r.components||[]).forEach(c=> cont.appendChild(renderComponent(c)) );
    app.appendChild(cont);
}

function renderComponent(c){ const t=(c.type||'text').toLowerCase();
    if(t==='text'){ return h(`<div class="card">${escapeHtml(c.value||'')}</div>`); }
    if(t==='image'){ const el=h('<div class="card"></div>'); const im=new Image(); im.src=c.src||''; el.appendChild(im); return el; }
    if(t==='link'){ const el=h(`<a href="${c.to||'#/'}" class="card">${escapeHtml(c.label||'ลิงก์')}</a>`); el.onclick=(e)=>{ if(el.getAttribute('href').startsWith('#')){ e.preventDefault(); navigate(c.to||'#/'); } }; return el; }
    if(t==='button'){ const el=h(`<button>${escapeHtml(c.label||'ปุ่ม')}</button>`); el.onclick=()=>handleAction(c.action||'navigate', c); return el; }
    if(t==='list'){ const el=h('<ul class="card"></ul>'); const items = bindItems(c); items.forEach(it=> el.appendChild(h(`<li>${escapeHtml(String(it))}</li>`))); return el; }
    if(t==='table'){ return renderTable(c); }
    if(t==='grid'){ const el=h('<div class="grid"></div>'); const imgs=(state.posts||[]).map(p=>p.img).filter(Boolean); imgs.forEach(src=>{ const im=new Image(); im.src=src; el.appendChild(im); }); return el; }
    if(t==='form'){ return renderForm(c); }
    if(t==='composer'){ return renderComposer(c); }
    if(t==='inbox'){ return renderInbox(); }
    if(t==='notifications'){ return renderNotifications(); }
    if(t==='profile'){ return renderProfile(); }
    if(t==='feed'){ return renderFeed(); }
    if(t==='todo'){ return renderTodo(); }
    return h(`<div class="card">[${t}]</div>`);
}

function navigate(path){ location.hash = path; }
function escapeHtml(s){ return (s||'').replace(/[&<>"]+/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }

async function handleAction(action, cfg){
    if(action==='navigate'){ navigate(cfg.to||'#/'); return; }
    if(action==='submit'){
        const formId = cfg.formId||'__active_form';
        const form = document.getElementById(formId) || cfg.__formEl;
        if(!form){ return; }
        const data={}; [...form.querySelectorAll('input,textarea,select')].forEach(el=> data[el.name||el.id||el.placeholder||'field'] = el.type==='file'? (el.files&&el.files[0]) : el.value);
        const coll = cfg.collection || 'posts';
        // Try API first
        if(await ensureApi()){
            try{
                const resp = await fetch(`${API_BASE}/api/${coll}`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)});
                if(resp.ok){ await tryLoadCollectionsFromAPI(); if(cfg.redirect){ navigate(cfg.redirect); } else { router(); } return; }
            }catch(e){}
        }
        // Fallback to local
        state.collections[coll] = state.collections[coll]||[]; state.collections[coll].push({...data, id: Date.now()}); save(); if(cfg.redirect){ navigate(cfg.redirect); } else { router(); }
        return;
    }
}

function bindItems(c){
    if(c.items){ return c.items; }
    if(c.collection){
        const coll = state.collections[c.collection] || [];
        const field=c.field||'name';
        return coll.map(x=>x[field]??JSON.stringify(x));
    }
    return [];
}

function renderTable(c){ const cols = c.columns||[]; const rows = c.rows || (c.collection? (state.collections[c.collection]||[]) : []);
    const el=h('<div class="card"><div class="table-wrap"></div></div>');
    const wrap = el.querySelector('.table-wrap');
    const thead = `<thead><tr>${cols.map(col=>`<th>${escapeHtml(col.header||col.field||'')}</th>`).join('')}</tr></thead>`;
    const tbody = `<tbody>${rows.map(r=>`<tr>${cols.map(col=>`<td>${escapeHtml(String(r[col.field]??''))}</td>`).join('')}</tr>`).join('')}</tbody>`;
    wrap.innerHTML = `<table>${thead}${tbody}</table>`;
    return el;
}

function renderFeed(){ const wrap=h('<div></div>'); (state.posts||[]).sort((a,b)=>b.ts-a.ts).forEach(p=> wrap.appendChild(renderPost(p)) ); return wrap; }
function renderPost(p){ const el=h(`<article class=\"card\">
        <div class=\"head\"><strong>@${p.user}</strong></div>
        ${p.img?`<img src=\"${p.img}\" alt=\"post\"/>`:''}
        <div class=\"actions\">\n        <button data-like>❤ ${p.liked?'เลิกถูกใจ':'ถูกใจ'}</button>\n        <button data-cmt>💬 คอมเมนต์</button>\n        <button data-share>↗️ แชร์</button>\n    </div>
        <div class=\"meta\">${p.likes||0} likes</div>
        <div class=\"meta\">${escapeHtml(p.caption||'')}</div>
        <div class=\"meta\">${(p.comments||[]).length} ความคิดเห็น</div>
`);
    el.querySelector('[data-like]').onclick=()=>{ p.liked=!p.liked; p.likes=(p.likes||0)+(p.liked?1:-1); save(); router(); };
    el.querySelector('[data-cmt]').onclick=()=>{ const text=prompt('คอมเมนต์'); if(text){ p.comments=p.comments||[]; p.comments.push({user:state.currentUser.username,text}); save(); router(); } };
    return el;
}

function renderComposer(){ const el=h(`<div class=\"card\">\n    <h3>สร้างโพสต์ใหม่</h3>\n    <input type=\"file\" accept=\"image/*\" id=\"file\"/>\n    <textarea id=\"cap\" placeholder=\"คำบรรยาย\" style=\"width:100%;margin-top:8px\"></textarea>\n    <div style=\\\"margin-top:8px\\\"><button id=\\\"btn\\\">โพสต์</button></div>\n</div>`);
    el.querySelector('#btn').onclick=()=>{
        const f=el.querySelector('#file').files[0]; const cap=el.querySelector('#cap').value;
        if(!f){ alert('เลือกรูปก่อน'); return; }
        const r=new FileReader(); r.onload=()=>{ state.posts=state.posts||[]; state.posts.push({id:Date.now(), user: state.currentUser.username, img:r.result, caption:cap, likes:0, liked:false, comments:[], ts:Date.now()}); save(); navigate('#/feed'); };
        r.readAsDataURL(f);
    };
    return el;
}

function renderForm(cfg){
    const el=h('<div class="card"></div>');
    const form=h('<form></form>');
    (cfg.fields||[]).forEach(f=>{
        const row=h('<div style="margin:6px 0"></div>');
        const label=h(`<div style="margin-bottom:4px">${escapeHtml(f.label||f.name)}</div>`);
        let input; const t=(f.type||'text').toLowerCase();
        if(t==='textarea'){ input=h('<textarea style="width:100%"></textarea>'); }
        else { input=h('<input style="width:100%"/>'); input.type=t; }
        input.name=f.name||f.id||'field';
        row.appendChild(label); row.appendChild(input);
        form.appendChild(row);
    });
    const btn=h('<button type="submit">ส่ง</button>'); form.appendChild(btn);
    form.onsubmit=(e)=>{
        e.preventDefault();
        handleAction('submit', { __formEl: form, collection: (cfg.collection || (cfg.submit&&cfg.submit.collection) || 'forms'), redirect: (cfg.redirect || (cfg.submit&&cfg.submit.to) || null) });
    };
    el.appendChild(form);
    return el;
}

function renderInbox(){ const list=h('<div class="card"></div>'); (state.messages||[]).forEach(m=> list.appendChild(h(`<div>${m.with}: ${m.last}</div>`)) ); return list; }
function renderNotifications(){ const list=h('<div class="card"></div>'); (state.notifications||[]).forEach(n=> list.appendChild(h(`<div>${n.text}</div>`)) ); return list; }
function renderProfile(){ const el=h('<div></div>'); const head=h(`<div class="card"><h3>@${state.currentUser.username}</h3><p>${state.currentUser.name||''}</p></div>`); el.appendChild(head); const grid=h('<div class="grid"></div>'); (state.posts||[]).filter(p=>p.user===state.currentUser.username).forEach(p=>{ const im=new Image(); im.src=p.img; grid.appendChild(im); }); el.appendChild(grid); return el; }

function renderTodo(){ const root=h('<div class="card"></div>'); root.innerHTML='<h3>Todo</h3><input id=t placeholder="เพิ่มงาน.."><button id=b>เพิ่ม</button><ul id=list></ul>'; let todos=JSON.parse(localStorage.getItem('todos')||'[]'); function paint(){ list.innerHTML=''; todos.forEach((t,i)=>{ const li=h(`<li>${t}</li>`); li.onclick=()=>{ todos.splice(i,1); saveTodos(); }; list.appendChild(li); }); } function saveTodos(){ localStorage.setItem('todos', JSON.stringify(todos)); paint(); } root.querySelector('#b').onclick=()=>{ const v=root.querySelector('#t').value.trim(); if(v){ todos.push(v); saveTodos(); root.querySelector('#t').value=''; } }; const list=root.querySelector('#list'); paint(); return root; }
"""

        # Create a blueprint and discover local assets
        blueprint = real_ai.generate_blueprint({**plan, "intent": "social"})
        try:
            assets = self._discover_local_images()
        except Exception:
            assets = []
        files = {
            'index.html': index_html,
            'styles.css': styles,
            'app.js': app_js,
            'assets.js': 'window.__ASSETS__ = ' + json.dumps(assets, ensure_ascii=False) + ';',
            'blueprint.json': json.dumps(blueprint, ensure_ascii=False, indent=2)
        }
        for rel, content in files.items():
            self._safe_write(app_dir, rel, content)
        return files

    # ---------- Backend from blueprint (SQLite + SQLAlchemy) ----------
    def _infer_models_from_sample(self, sample: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Infer simple data_models from sample_data keys.
        Returns mapping: ModelName -> { field_name: type }
        Types: string, integer, float, boolean, text
        """
        models: Dict[str, Dict[str, str]] = {}
        if not isinstance(sample, dict):
            return models
        for key, items in sample.items():
            if not isinstance(items, list) or not items:
                continue
            first = items[0]
            if not isinstance(first, dict):
                continue
            model = {}
            for f, v in first.items():
                t = 'string'
                if isinstance(v, bool): t = 'boolean'
                elif isinstance(v, int): t = 'integer'
                elif isinstance(v, float): t = 'float'
                elif isinstance(v, (list, dict)): t = 'text'
                else: t = 'string'
                model[f] = t
            name = key[:-1].capitalize() if key.endswith('s') else key.capitalize()
            models[name] = model
        return models

    def _gen_backend_from_blueprint(self, app_dir: Path, blueprint: Dict[str, Any]) -> Dict[str, str]:
        """Generate a FastAPI + SQLAlchemy backend with SQLite from blueprint data_models.
        Creates CRUD endpoints /api/<plural> for each model.
        """
        files: Dict[str, str] = {}
        backend_dir = app_dir / 'backend'
        backend_dir.mkdir(parents=True, exist_ok=True)

        data_models = blueprint.get('data_models') or {}
        if not data_models:
            data_models = self._infer_models_from_sample(blueprint.get('sample_data') or {})
        if not data_models:
            return files  # nothing to generate

        # models.py
        model_lines = [
            'from sqlalchemy import Column, Integer, String, Text, Float, Boolean',
            'from sqlalchemy.orm import declarative_base',
            '',
            'Base = declarative_base()',
            '',
        ]
        type_map = {
            'integer': 'Integer',
            'float': 'Float',
            'boolean': 'Boolean',
            'text': 'Text',
            'string': 'String(255)'
        }
        schemas_lines = [
            'from pydantic import BaseModel',
            'from typing import Optional',
            ''
        ]
        endpoints_blocks: List[str] = []

        for name, fields in data_models.items():
            class_name = ''.join([p.capitalize() for p in name.split('_')])
            table_name = name.lower() + ('' if name.lower().endswith('s') else 's')
            # SQLAlchemy model
            model_lines.append(f'class {class_name}(Base):')
            model_lines.append(f'    __tablename__ = "{table_name}"')
            model_lines.append('    id = Column(Integer, primary_key=True, index=True)')
            if isinstance(fields, dict):
                for f, t in fields.items():
                    if f == 'id':
                        continue
                    col = type_map.get((t or 'string').lower(), 'String(255)')
                    model_lines.append(f'    {f} = Column({col}, nullable=True)')
            model_lines.append('')

            # Pydantic schemas
            schemas_lines.append(f'class {class_name}In(BaseModel):')
            if isinstance(fields, dict):
                for f, t in fields.items():
                    if f == 'id':
                        continue
                    py_t = 'str'
                    if (t or '').lower() == 'integer': py_t = 'int'
                    elif (t or '').lower() == 'float': py_t = 'float'
                    elif (t or '').lower() == 'boolean': py_t = 'bool'
                    elif (t or '').lower() == 'text': py_t = 'str'
                    schemas_lines.append(f'    {f}: Optional[{py_t}] = None')
            else:
                schemas_lines.append('    name: Optional[str] = None')
            schemas_lines.append('')

            schemas_lines.append(f'class {class_name}Out({class_name}In):')
            schemas_lines.append('    id: int')
            schemas_lines.append('')

            # Endpoints block
            endpoints_blocks.append('\n'.join([
                f'# CRUD for {class_name}',
                f'@app.get("/api/{table_name}")',
                f'def list_{table_name}(db: Session = Depends(get_db)):',
                f'    return db.query(models.{class_name}).all()',
                '',
                f'@app.post("/api/{table_name}")',
                f'def create_{name}(item: schemas.{class_name}In, db: Session = Depends(get_db)):',
                f'    obj = models.{class_name}(**item.model_dump(exclude_unset=True))',
                f'    db.add(obj); db.commit(); db.refresh(obj); return obj',
                '',
                f'@app.get("/api/{table_name}/{{item_id}}")',
                f'def get_{name}(item_id: int, db: Session = Depends(get_db)):',
                f'    return db.query(models.{class_name}).get(item_id)',
                '',
                f'@app.put("/api/{table_name}/{{item_id}}")',
                f'def update_{name}(item_id: int, item: schemas.{class_name}In, db: Session = Depends(get_db)):',
                f'    obj = db.query(models.{class_name}).get(item_id)',
                f'    if not obj: return {{"error":"not found"}}',
                f'    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)',
                f'    db.commit(); db.refresh(obj); return obj',
                '',
                f'@app.delete("/api/{table_name}/{{item_id}}")',
                f'def delete_{name}(item_id: int, db: Session = Depends(get_db)):',
                f'    obj = db.query(models.{class_name}).get(item_id)',
                f'    if not obj: return {{"ok": False}}',
                f'    db.delete(obj); db.commit(); return {{"ok": True}}',
            ]))

        models_py = '\n'.join(model_lines)
        schemas_py = '\n'.join(schemas_lines)

        main_py = '''from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import models, schemas

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="AI Blueprint API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

@app.get('/health')
def health():
    return {"status":"ok"}

'''
        main_py += '\n\n'.join(endpoints_blocks) + '\n'

        reqs = 'fastapi\nuvicorn\nsqlalchemy\npydantic\n'

        self._safe_write(backend_dir, 'models.py', models_py)
        self._safe_write(backend_dir, 'schemas.py', schemas_py)
        self._safe_write(backend_dir, 'main.py', main_py)
        self._safe_write(backend_dir, 'requirements.txt', reqs)

        # Windows helper
        start_bat = """@echo off
cd /d %~dp0
python -m uvicorn backend.main:app --host 0.0.0.0 --port 9000 --log-level info
pause
"""
        self._safe_write(app_dir, 'start_backend.bat', start_bat)

        # Frontend with offline fallback hint
        front_html = '''<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Enterprise App</title><style>body{font-family:Segoe UI;margin:0}header{background:#0d6efd;color:#fff;padding:12px}main{padding:16px}input,button{font:inherit}</style><script defer src="frontend/app.js"></script></head><body><header><h1>Enterprise UI</h1></header><main><div><input id=n placeholder="เพิ่มงาน.."><button id=a>เพิ่ม</button></div><ul id=list></ul><p id="hint" style="color:#666;margin-top:10px"></p></main></body></html>'''
        front_js = """// Robust API base and offline fallback
const API = `${location.protocol}//${location.hostname}:9000`;
let useMock = false;
async function list(){
  if(useMock){
    return JSON.parse(localStorage.getItem('items')||'[{"id":1,"name":"ตัวอย่าง (ออฟไลน์)","done":false}]');
  }
  try{
    const r = await fetch(API + '/api/items');
    if(!r.ok) throw new Error('bad status');
    return await r.json();
  }catch(e){
    useMock = true;
    const hint = document.getElementById('hint');
    if(hint) hint.textContent = 'โหมดออฟไลน์: ยังไม่ได้รัน Backend ที่พอร์ต 9000 (ดับเบิลคลิก start_backend.bat)';
    return await list();
  }
}
async function add(name){
  if(useMock){
    const items = await list();
    const id = Math.floor(Math.random()*1e6);
    items.push({id,name,done:false});
    localStorage.setItem('items', JSON.stringify(items));
    return;
  }
  await fetch(API + '/api/items', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({id:Math.floor(Math.random()*1e6), name, done:false})});
}
async function paint(){
  const items = await list();
  const ul = document.getElementById('list');
  ul.innerHTML = '';
  items.forEach(it=>{ const li=document.createElement('li'); li.textContent=it.name; ul.appendChild(li); });
}
window.addEventListener('load', ()=>{
  document.getElementById('a').onclick = async ()=>{
    const v = document.getElementById('n').value.trim();
    if(v){ await add(v); document.getElementById('n').value=''; await paint(); }
  };
  paint();
});
"""
        self._safe_write(app_dir, 'index.html', front_html)
        self._safe_write(app_dir, 'frontend/app.js', front_js)
        files['index.html'] = front_html
        files['frontend/app.js'] = front_js

        # README
        readme = """# AI Enterprise App

## วิธีรัน Backend
ทางเลือก A) Windows: ดับเบิลคลิก start_backend.bat

ทางเลือก B) คำสั่งด้วยตัวเอง
1. ติดตั้งไลบรารี
   pip install -r backend/requirements.txt
2. รันเซิร์ฟเวอร์
   uvicorn backend.main:app --host 0.0.0.0 --port 9000

## วิธีเปิด Frontend
- เปิดไฟล์ index.html ด้วยเบราว์เซอร์ (จะเรียก API ที่พอร์ต 9000)
- ถ้ายังไม่รัน Backend ระบบจะทำงานโหมดออฟไลน์ชั่วคราว และแสดงคำแนะนำในหน้าเว็บ
"""
        self._safe_write(app_dir, 'README.md', readme)
        files['README.md'] = readme
        return files

    def build_project(self, app_dir: Path, plan: Dict) -> Dict[str, Any]:
        app_type = (plan.get('app_type') or '').lower()
        desc_text = (plan.get('description') or '').lower() + ' ' + (plan.get('app_name') or '').lower()
        created_files: Dict[str, str] = {}
        http_entry: Optional[str] = None
        if ('instagram' in app_type or 'social' in app_type) or ('instagram' in desc_text or 'social' in desc_text or 'ig' in desc_text):
            # Use social SPA + optional backend
            created_files = self._gen_social_spa(app_dir, plan)
            blueprint = real_ai.generate_blueprint({**plan, "intent": "social"})
            backend_files = self._gen_backend_from_blueprint(app_dir, blueprint)
            created_files.update(backend_files)
            self._safe_write(app_dir, 'blueprint.json', json.dumps(blueprint, ensure_ascii=False, indent=2))
            http_entry = 'index.html'
        elif any(k in app_type for k in ['website', 'portfolio', 'blog']):
            created_files = self._gen_static_site(app_dir, plan)
            http_entry = 'index.html'
        elif any(k in app_type for k in ['webapp', 'dashboard', 'tool', 'enterprise', 'ecommerce', 'backend', 'mobile']):
            # Generic SPA + backend from blueprint
            created_files = self._gen_spa(app_dir, plan)
            blueprint = real_ai.generate_blueprint({**plan, "intent": "webapp"})
            backend_files = self._gen_backend_from_blueprint(app_dir, blueprint)
            created_files.update(backend_files)
            self._safe_write(app_dir, 'blueprint.json', json.dumps(blueprint, ensure_ascii=False, indent=2))
            http_entry = 'index.html'
        else:
            # default to SPA for richer UX
            created_files = self._gen_spa(app_dir, plan)
            blueprint = real_ai.generate_blueprint({**plan, "intent": "default"})
            backend_files = self._gen_backend_from_blueprint(app_dir, blueprint)
            created_files.update(backend_files)
            self._safe_write(app_dir, 'blueprint.json', json.dumps(blueprint, ensure_ascii=False, indent=2))
            http_entry = 'index.html'
        # zip
        zip_path = self._zip_app(app_dir)
        return {"files": list(created_files.keys()), "http_entry": http_entry, "zip_path": str(zip_path)}

    def _discover_local_images(self, limit: int = 40) -> List[str]:
        """Return list of served /data/* image URLs if data directory exists.
        Looks for data/**/raw/*.(png|jpg|jpeg|gif|webp)
        """
        root = Path('data')
        if not root.exists():
            return []
        exts = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        results: List[str] = []
        try:
            for p in root.rglob('*'):
                if p.is_file() and p.suffix.lower() in exts and ('/raw/' in str(p).replace('\\','/') or str(p).lower().endswith('/raw')):
                    web_path = '/' + str(p).replace('\\', '/').lstrip('/')
                    if not web_path.startswith('/data/'):
                        web_path = '/data/' + str(p).replace('\\','/')
                    results.append(web_path)
                    if len(results) >= limit:
                        break
        except Exception:
            pass
        return results

    async def _create_file_with_typing(self, websocket: WebSocket, file_path: str, content: str, description: str):
        """สร้างไฟล์พร้อม typing effect"""
        try:
            # แสดงสถานะเริ่มสร้างไฟล์
            await websocket.send_json({
                "type": "file_start",
                "file": file_path,
                "description": description
            })
            
            # สร้างไฟล์จริง
            full_path = self.workspace_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # เขียนไฟล์ทีละบรรทัด พร้อม delay
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                # เขียนไฟล์
                mode = 'w' if i == 0 else 'a'
                with open(full_path, mode, encoding='utf-8') as f:
                    f.write(line + '\n')
                
                # ส่งข้อมูลแบบ realtime
                await websocket.send_json({
                    "type": "typing_line",
                    "file": file_path,
                    "line": line,
                    "progress": (i + 1) / len(lines) * 100
                })
                
                # Delay เพื่อให้ดู exciting
                await asyncio.sleep(0.01)  # เร็วกว่าเดิมเพื่อ UX ที่ดี
            
            # ส่งสัญญาณเสร็จสิ้น
            await websocket.send_json({
                "type": "file_complete",
                "file": file_path,
                "message": f"✅ {description} สร้างเสร็จแล้ว!"
            })
            
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "message": f"❌ Error creating {file_path}: {str(e)}"
            })

    async def generate_app_exciting(self, websocket: WebSocket, requirements: Dict):
        """สร้างแอป พร้อม exciting effects แบบ realtime!"""
        
        self.app_counter += 1
        app_name = f"app_{self.app_counter}"
        
        try:
            # 🎯 ขั้นที่ 1: วิเคราะห์ความต้องการ
            await websocket.send_json({
                "type": "status",
                "message": "🧠 AI กำลังวิเคราะห์ความต้องการ...",
                "progress": 10
            })
            await asyncio.sleep(1)

            plan = real_ai.generate_plan(requirements)

            # 🎯 ขั้นที่ 2: สร้างโครงสร้าง
            await websocket.send_json({
                "type": "status",
                "message": "📁 กำลังสร้างโครงสร้างโปรเจ็ค...",
                "progress": 20
            })
            await asyncio.sleep(0.5)

            # 🎯 ขั้นที่ 3: สร้าง Frontend
            await websocket.send_json({
                "type": "status",
                "message": "🎨 AI กำลังออกแบบ User Interface...",
                "progress": 40
            })

            # สร้างโปรเจ็คหลายไฟล์ตามประเภท
            app_dir = self.workspace_dir / app_name
            app_dir.mkdir(parents=True, exist_ok=True)
            build_info = self.build_project(app_dir, plan)
            # สตรีมโค้ดทีละไฟล์เพื่อ UX
            for rel in build_info['files']:
                full = app_dir / rel
                with open(full, 'r', encoding='utf-8') as f:
                    content = f.read()
                await self._create_file_with_typing(websocket, f"{app_name}/{rel}", content, f"สร้างไฟล์ {rel}")
                await asyncio.sleep(0.05)
            # ส่ง preview ถ้ามีหน้า index.html
            if build_info.get('http_entry'):
                index_file = app_dir / build_info['http_entry']
                try:
                    html_content = index_file.read_text(encoding='utf-8')
                except Exception:
                    html_content = ""
                await websocket.send_json({
                    "type": "preview_ready",
                    "html_content": html_content,
                    "app_name": plan.get("app_name", app_name),
                    "progress": 80
                })

            await asyncio.sleep(1)

            # 🎯 ขั้นที่ 5: เสร็จสิ้น!
            entry = build_info.get('http_entry')
            http_url = f"{BASE_HTTP_URL}/apps/{app_name}/{entry}" if entry else None
            zip_rel = Path(build_info['zip_path'])
            # Copy zip to static /apps for HTTP download
            try:
                if zip_rel.exists():
                    shutil.copy2(str(zip_rel), str(generated_dir / zip_rel.name))
            except Exception as e:
                print(f"⚠️ Copy zip failed (ws flow): {e}")
            download_url = f"{BASE_HTTP_URL}/apps/{zip_rel.name}" if (generated_dir / zip_rel.name).exists() else None
            await websocket.send_json({
                "type": "build_complete",
                "message": f"🎉 สร้าง {plan['app_name']} สำเร็จ! ใช้งานได้เลย",
                "app_path": f"generated_apps/{app_name}",
                "http_url": http_url,
                "download_url": download_url,
                "progress": 100
            })

        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "message": f"❌ เกิดข้อผิดพลาด: {str(e)}"
            })

# สร้าง AI instance
exciting_ai = ExcitingLovableAI()

@app.get("/")
async def home():
    return {"message": "🚀 Lovable Clone AI Server - Ready!", "status": "online"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat หลัก - รองรับทั้งคุยธรรมดาและสร้างแอป"""
    
    print(f"📨 Received request: {request}")
    
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "created_at": datetime.now()
        }
    
    session = sessions[session_id]
    
    # เพิ่มข้อความของ user
    session['messages'].append({
        "role": "user", 
        "content": request.message
    })
    
    # ---- helpers for clarity and merging ----
    def _deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(a, dict):
            a = {}
        if not isinstance(b, dict):
            return a
        out = dict(a)
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(out.get(k), dict):
                out[k] = _deep_merge(out[k], v)
            elif isinstance(v, list) and isinstance(out.get(k), list):
                # union while preserving order
                seen = set()
                merged = []
                for item in (out[k] + v):
                    key = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, (dict, list)) else item
                    if key not in seen:
                        merged.append(item)
                        seen.add(key)
                out[k] = merged
            else:
                if v not in [None, "", []]:
                    out[k] = v
        return out

    def _missing_essentials(req: Dict[str, Any]) -> List[str]:
        missing = []
        desc = (req or {}).get('description') or ''
        features = (req or {}).get('features') or []
        app_type = ((req or {}).get('app_type') or '').lower()
        pages = (req or {}).get('pages') or []
        if len(desc.strip()) < 20:
            missing.append('คำอธิบายรายละเอียดของระบบ (อย่างน้อย 20 ตัวอักษร)')
        if len(features) < 3:
            missing.append('รายการฟีเจอร์หลักอย่างน้อย 3 ข้อ')
        if any(k in app_type for k in ['website', 'portfolio', 'blog']):
            if len(pages) < 5:
                missing.append('รายการเพจ (อย่างน้อย 5 หน้า เช่น Home, About, Services, Pricing, Blog, Contact)')
        elif any(k in app_type for k in ['webapp', 'dashboard', 'tool']):
            if not (req.get('entities') or req.get('data_models')):
                missing.append('โมเดลข้อมูล/เอนทิตีหลัก (เช่น Users, Orders, Items)')
            if not req.get('workflows'):
                missing.append('workflow หลักของผู้ใช้ (เช่น เพิ่มเมนู → ใส่ตะกร้า → ชำระเงิน)')
        elif any(k in app_type for k in ['enterprise', 'ecommerce', 'backend']):
            modules = (req or {}).get('modules') or []
            if not modules:
                missing.append('รายชื่อโมดูล/หน้าจอหลัก (เช่น เมนู, คิดเงิน POS, ออเดอร์, ชำระเงิน, รายงาน)')
            roles = (req or {}).get('roles') or []
            if not roles:
                missing.append('บทบาทผู้ใช้ (เช่น แคชเชียร์, ผู้จัดการ, แอดมิน)')
        elif 'mobile' in app_type:
            if not req.get('platform'):
                missing.append('แพลตฟอร์มเป้าหมาย (iOS, Android หรือทั้งสอง)')
        return missing

    def _clarifying_message(req: Dict[str, Any], missing: List[str]) -> str:
        """สร้างข้อความถามต่อแบบชี้เป้า พร้อมตัวอย่าง เพื่อหลีกเลี่ยงการถามซ้ำ"""
        app_type = ((req or {}).get('app_type') or '').lower()
        hints: List[str] = []
        if 'website' in app_type:
            hints = [
                'Home, About, Services, Pricing, Blog, Contact',
                'ธีม/โทนสี (modern/minimal/professional)',
                'กลุ่มเป้าหมาย'
            ]
        elif ('enterprise' in app_type) or ('ecommerce' in app_type):
            hints = [
                'โมดูล: เมนู, POS, ออเดอร์, ชำระเงิน, รายงาน',
                'บทบาท: แคชเชียร์/ผู้จัดการ',
                'รูปแบบใบเสร็จ/ภาษี',
                'สกุลเงิน/ภาษี'
            ]
        elif ('webapp' in app_type) or ('dashboard' in app_type) or ('tool' in app_type):
            hints = [
                'เอนทิตี/โมเดลข้อมูลหลัก (เช่น Users, Orders, Items)',
                'workflow ผู้ใช้ (เช่น เพิ่มเมนู → ใส่ตะกร้า → ชำระเงิน)',
                'ฟีเจอร์สำคัญ',
                'บทบาทผู้ใช้'
            ]
        elif 'mobile' in app_type:
            hints = [
                'แพลตฟอร์มเป้าหมาย (iOS/Android)',
                'ฟีเจอร์หลัก',
                'การใช้งานออฟไลน์/ออนไลน์'
            ]

        msg = 'ขอรายละเอียดเพิ่มเติมเพื่อสร้างแอปให้ตรงใจครับ:\n'
        msg += '\n'.join([f'- {m}' for m in missing])
        if hints:
            msg += '\n\nตัวอย่างที่ช่วยตัดสินใจเร็วขึ้น:\n' + '\n'.join([f'• {h}' for h in hints])
        msg += '\n\nพิมพ์ตอบเป็นข้อ ๆ ได้เลยครับ (หรือจะให้ฉันเสนอชุดดีฟอลต์ก็ได้)'
        return msg

    # Slot-filling from user's latest message to avoid repeated asks
    def _infer_from_text(text: str) -> Dict[str, Any]:
        t = (text or '').strip()
        tl = t.lower()
        result: Dict[str, Any] = {}
        # App type inference (Thai/English)
        if any(k in tl for k in ['เว็บไซต์', 'เว็บ', 'website', 'เพจ', 'หน้า', 'ร้าน', 'ร้านอาหาร', 'รีสตอรองต์', 'restaurant']):
            result['app_type'] = 'website'
        elif any(k in tl for k in ['โซเชียล', 'social', 'instagram', 'ig']):
            result['app_type'] = 'social'
        # Pages list extraction (comma or newline separated)
        # Trigger only if looks like a list of words/titles
        if (',' in t) or ('\n' in t):
            raw = [p.strip() for p in t.replace('\n', ',').split(',') if p.strip()]
            # Filter likely page names (very permissive, keep words without spaces threshold)
            # Accept common page names in EN/TH
            common = {'home','about','services','pricing','blog','contact','portfolio','menu','gallery','reviews','team','faq','booking','reservation','cart','shop'}
            th_common = {'หน้าแรก','เกี่ยวกับ','บริการ','ราคา','บล็อก','ติดต่อ','เมนู','แกลเลอรี่','รีวิว','จองโต๊ะ','สั่งซื้อ','ตะกร้า'}
            pages: List[str] = []
            for item in raw:
                s = item.strip().strip('-•').strip()
                if not s:
                    continue
                low = s.lower()
                if low in common or s in th_common or len(s) <= 20:
                    pages.append(s)
            if pages:
                result['pages'] = pages
                result.setdefault('app_type', 'website')
        # Restaurant heuristics → sensible defaults
        if any(k in tl for k in ['restaurant','ร้านอาหาร','cafe','คาเฟ่']):
            result.setdefault('app_type', 'website')
            result.setdefault('features', ['เมนูอาหาร','แกลเลอรี่','จองโต๊ะ','รีวิวลูกค้า'])
        # Features extraction (rough): look for bullets separated by commas when words like 'ฟีเจอร์' present
        if any(k in tl for k in ['ฟีเจอร์', 'ความสามารถ', 'features']):
            parts = [p.strip() for p in t.replace('\n', ',').split(',') if p.strip()]
            if parts:
                result['features'] = parts[:10]
        # Description: if long sentence Thai, use as description
        if len(t) >= 20:
            result.setdefault('description', t)
        return result

    try:
        # Infer from user's latest message first (slot filling)
        latest_text = request.message
        inferred = _infer_from_text(latest_text)

        # ให้ AI ตัดสินใจ
        decision = real_ai.chat_decide(session['messages'])

        # รวม requirements สะสมในเซสชัน (infer first, then AI)
        agg_req = _deep_merge(session.get('requirements', {}), inferred)
        agg_req = _deep_merge(agg_req, decision.get('requirements') or {})
        session['requirements'] = agg_req

        # ถ้าไม่ชัด ให้ถามต่ออย่างมีเป้าหมาย
        missing = _missing_essentials(agg_req)
        if missing and decision.get('action') == 'build_app':
            # If the user likely provided pages/features in this turn, re-check to avoid repeating asks
            # After inference and merge, recompute missing; if still missing, ask once with targeted message
            decision['action'] = 'ask_question'
            decision['message'] = _clarifying_message(agg_req, missing)
        elif not missing and decision.get('action') != 'build_app':
            # We have enough info now — proceed to build to avoid looping questions
            decision['action'] = 'build_app'
            decision['message'] = 'ข้อมูลครบแล้วครับ กำลังเริ่มสร้างแอปให้ทันที 🚀'

        # บันทึกข้อความตอบกลับ (อาจเป็นคำถามชี้นำ)
        session['messages'].append({
            "role": "assistant",
            "content": decision['message']
        })
        
        return {
            "response": decision['message'],
            "action": decision['action'],
            "session_id": session_id,
            "requirements": session.get('requirements'),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Chat error: {str(e)}"}
        )

@app.post("/build_app")
async def build_app_endpoint(requirements: Dict[str, Any], request: Request):
    """สร้างแอปจริงๆ และคืน URL"""
    try:
        exciting_ai.app_counter += 1
        app_name = f"app_{exciting_ai.app_counter}"
        app_dir = exciting_ai.workspace_dir / app_name
        app_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🚀 Building app: {app_name}")
        print(f"📋 Requirements: {requirements}")
        
        # สร้างแผน
        plan = real_ai.generate_plan(requirements)
        print(f"🎯 Generated plan: {plan}")
        
        # สร้างโปรเจ็คหลายไฟล์ตามประเภท
        build_info = exciting_ai.build_project(app_dir, plan)
        entry = build_info.get('http_entry')
        index_file = app_dir / (entry or 'index.html')
        # คืน URL ที่เปิดได้จริง (HTTP และ file URL)
        app_url = f"file:///{str(index_file).replace('\\', '/')}" if index_file.exists() else None
        http_url = f"{BASE_HTTP_URL}/apps/{app_name}/{entry}" if entry else None
        # เตรียมดาวน์โหลด zip (ย้ายไฟล์ zip มาที่โฟลเดอร์ static /apps)
        zip_path = Path(build_info['zip_path'])
        if zip_path.exists():
            try:
                shutil.copy2(str(zip_path), str(generated_dir / zip_path.name))
            except Exception as e:
                print(f"⚠️ Copy zip failed: {e}")
        download_url = f"{BASE_HTTP_URL}/apps/{zip_path.name}" if (generated_dir / zip_path.name).exists() else None
        
        print(f"✅ App created at: {app_url}")
        
        return {
            "success": True,
            "app_url": app_url,
            "app_name": plan.get("app_name", app_name),
            "description": plan.get("description", "แอปที่สร้างด้วย AI"),
            "http_url": http_url,
            "download_url": download_url
        }

    except Exception as e:
        print(f"❌ Build error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Build error: {str(e)}"}
        )
    
@app.post("/revise")
async def revise_endpoint(data: Dict[str, Any]):
    """Refine an existing session's requirements with deltas and rebuild a fresh app.

    Request JSON:
    {
      "session_id": "optional-session-id",
      "delta": { ... }   # fields to merge into current requirements
    }

    Response JSON: same shape as /build_app (http_url, download_url, app_name, ...)
    """
    try:
        session_id = (data or {}).get("session_id") or str(uuid.uuid4())
        delta = (data or {}).get("delta") or {}

        sess = sessions.setdefault(session_id, {"messages": [], "created_at": datetime.now(), "requirements": {}})

        # Deep merge helper (same as WS)
        def _deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
            if not isinstance(a, dict):
                a = {}
            if not isinstance(b, dict):
                return a
            out = dict(a)
            for k, v in b.items():
                if isinstance(v, dict) and isinstance(out.get(k), dict):
                    out[k] = _deep_merge(out[k], v)
                elif isinstance(v, list) and isinstance(out.get(k), list):
                    seen = set(); merged = []
                    for item in (out[k] + v):
                        key = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, (dict, list)) else item
                        if key not in seen:
                            merged.append(item); seen.add(key)
                    out[k] = merged
                else:
                    if v not in [None, "", []]:
                        out[k] = v
            return out

        sess['requirements'] = _deep_merge(sess.get('requirements', {}), delta)

        # Build a new app based on updated requirements
        exciting_ai.app_counter += 1
        app_name = f"app_{exciting_ai.app_counter}"
        app_dir = exciting_ai.workspace_dir / app_name
        app_dir.mkdir(parents=True, exist_ok=True)

        plan = real_ai.generate_plan(sess['requirements'])
        build_info = exciting_ai.build_project(app_dir, plan)

        entry = build_info.get('http_entry')
        index_file = app_dir / (entry or 'index.html')
        app_url = f"file:///{str(index_file).replace('\\', '/')}" if index_file.exists() else None
        http_url = f"{BASE_HTTP_URL}/apps/{app_name}/{entry}" if entry else None

        zip_path = Path(build_info['zip_path'])
        if zip_path.exists():
            try:
                shutil.copy2(str(zip_path), str(generated_dir / zip_path.name))
            except Exception as e:
                print(f"⚠️ Copy zip failed (revise): {e}")
        download_url = f"{BASE_HTTP_URL}/apps/{zip_path.name}" if (generated_dir / zip_path.name).exists() else None

        return {
            "success": True,
            "session_id": session_id,
            "app_url": app_url,
            "app_name": plan.get("app_name", app_name),
            "description": plan.get("description", "แอปที่สร้างด้วย AI"),
            "http_url": http_url,
            "download_url": download_url
        }

    except Exception as e:
        print(f"❌ Revise error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Revise error: {str(e)}"}
        )


async def _ws_handler_core(websocket: WebSocket, initial_notice: str = None):
    """แกนหลักของ WS: accept + heartbeat + วนรับข้อความ + จัดการ action"""
    await websocket.accept()

    # Heartbeat
    async def _heartbeat():
        try:
            while True:
                await asyncio.sleep(20)
                try:
                    await websocket.send_json({"type": "ping"})
                except Exception:
                    break
        except Exception:
            pass

    hb_task = asyncio.create_task(_heartbeat())

    # แจ้งเตือนครั้งแรก (กรณี path เก่า)
    if initial_notice:
        try:
            await websocket.send_json({"type": "status", "message": initial_notice, "progress": 0})
        except Exception:
            pass

    try:
        while True:
            try:
                data = await websocket.receive_json()
            except WebSocketDisconnect as e:
                code = getattr(e, "code", None)
                print(f"WebSocket disconnected by client, code={code}")
                break
            except Exception as e:
                print(f"WebSocket receive error: {e}")
                break

            action = (data or {}).get("action")
            if action == "build_app":
                requirements = data.get("requirements", {})
                await exciting_ai.generate_app_exciting(websocket, requirements)
            elif action == "revise":
                session_id = data.get("session_id") or str(uuid.uuid4())
                delta = data.get("delta", {}) or {}
                sess = sessions.setdefault(session_id, {"messages": [], "created_at": datetime.now(), "requirements": {}})
                def _deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
                    if not isinstance(a, dict):
                        a = {}
                    if not isinstance(b, dict):
                        return a
                    out = dict(a)
                    for k, v in b.items():
                        if isinstance(v, dict) and isinstance(out.get(k), dict):
                            out[k] = _deep_merge(out[k], v)
                        elif isinstance(v, list) and isinstance(out.get(k), list):
                            seen = set(); merged = []
                            for item in (out[k] + v):
                                key = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, (dict, list)) else item
                                if key not in seen:
                                    merged.append(item); seen.add(key)
                            out[k] = merged
                        else:
                            if v not in [None, "", []]:
                                out[k] = v
                    return out
                sess['requirements'] = _deep_merge(sess.get('requirements', {}), delta)
                await exciting_ai.generate_app_exciting(websocket, sess['requirements'])
            else:
                try:
                    await websocket.send_json({"type": "status", "message": "unknown action", "progress": 0})
                except Exception:
                    break
    finally:
        try:
            hb_task.cancel()
        except Exception:
            pass
        try:
            await websocket.close()
        except Exception:
            pass
        print("WebSocket handler finished")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket สำหรับ realtime app building (path ใหม่)"""
    await _ws_handler_core(websocket)

@app.websocket("/ws/chat")
async def websocket_compat(websocket: WebSocket):
    """รองรับ client เก่าที่เชื่อม /ws/chat โดยพยายามให้บริการเหมือน /ws และแจ้งเตือนให้ย้าย path"""
    await _ws_handler_core(websocket, initial_notice="โปรดเชื่อมต่อที่เส้นทางใหม่: ws://<host>/ws")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_mode": "real" if real_ai.use_real_ai else "demo",
        "provider": getattr(real_ai, 'provider', 'openai'),
        "gemini_ready": getattr(real_ai, 'gemini_ready', False),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Exciting Lovable Backend...")
    if getattr(real_ai, 'use_real_ai', False):
        print("🤖 Real AI mode active (provider: {} | gemini_ready: {})".format(
            getattr(real_ai, 'provider', 'openai'), getattr(real_ai, 'gemini_ready', False)))
    else:
        print("🤖 Using demo mode - set OPENAI_API_KEY for real AI")
    print("📍 Server: http://localhost:8001")
    print("🔌 WebSocket: ws://localhost:8001/ws")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")