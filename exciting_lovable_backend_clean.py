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

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, Request, HTTPException
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

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class RealAI:
    """Real OpenAI AI integration with fallback"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.use_real_ai = True
            print(f"🚀 Using REAL OpenAI API! (key: ...{self.api_key[-10:]})")
        else:
            self.use_real_ai = False
            print("🤖 Using demo mode - set OPENAI_API_KEY for real AI")
        self.conversation_count = 0

    def chat_decide(self, messages: List[Dict]) -> Dict[str, Any]:
        """ใช้ OpenAI จริง ตัดสินใจจะถามต่อหรือสร้างแอป"""
        self.conversation_count += 1
        
        # ลองใช้ OpenAI จริงก่อนเสมอ
        try:
            if self.use_real_ai:
                # ใช้ OpenAI จริง
                system_prompt = """คุณคือ AI ผู้เชี่ยวชาญในการสร้างแอปเว็บ เว็บไซต์ และ mobile app ให้ประเมินความต้องการของผู้ใช้อย่างอิสระ:

หน้าที่ของคุณ:
1. วิเคราะห์ว่าผู้ใช้ต้องการอะไรจากคำขอ (ทักทาย/คุยธรรมดา หรือ สร้างแอป/เว็บ)
2. ถ้าเป็นการสร้าง ให้ประเมินเองว่าควรเป็น:
   - Website (เว็บไซต์แสดงข้อมูล)
   - Web App (แอปเว็บที่มีการโต้ตอบ)  
   - Mobile App (แอปมือถือ)
   - Dashboard (หน้าจอควบคุม/รายงาน)
   - Portfolio (แฟ้มผลงาน)
   - Blog (บล็อก)
   - E-commerce (ร้านค้าออนไลน์)
   - Game (เกม)
   - Tool (เครื่องมือช่วยงาน)
   หรือประเภทอื่นๆ ตามความเหมาะสม

3. สร้างรายละเอียดและฟีเจอร์ที่สมเหตุสมผล

ตอบเป็น JSON:
{
    "action": "ask_question" หรือ "build_app",
    "message": "ข้อความตอบกลับเป็นไทย สไตล์เป็นกันเองแต่เชี่ยวชาญ",
    "requirements": {
        "app_type": "ประเภทที่คุณประเมิน เช่น website, webapp, mobile_app, dashboard, portfolio, blog, ecommerce, game, tool",
        "platform": "web, mobile, desktop หรือ hybrid", 
        "description": "คำอธิบายละเอียดของแอป",
        "features": ["ฟีเจอร์หลัก", "ฟีเจอร์รอง", "ฟีเจอร์พิเศษ"],
        "ui_style": "modern, minimal, colorful, professional, creative",
        "target_users": "กลุ่มผู้ใช้เป้าหมาย"
    }
}"""
                
                # สร้าง conversation context
                conversation = [{"role": "system", "content": system_prompt}]
                conversation.extend(messages[-3:])  # เอาแค่ 3 ข้อความล่าสุดเพื่อประหยัด token
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=conversation,
                    temperature=0.7,
                    max_tokens=500
                )
                
                content = response.choices[0].message.content.strip()
                print(f"🤖 OpenAI Raw Response: {content}")
                
                # พยายาม parse JSON
                try:
                    # ลองหา JSON block
                    if '```json' in content:
                        json_part = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        json_part = content.split('```')[1].split('```')[0].strip()
                    elif '{' in content and '}' in content:
                        start = content.find('{')
                        end = content.rfind('}') + 1
                        json_part = content[start:end]
                    else:
                        json_part = content
                    
                    result = json.loads(json_part)
                    
                    # Validate required fields
                    if 'action' not in result:
                        result['action'] = 'ask_question'
                    if 'message' not in result:
                        result['message'] = content
                    
                    print(f"✅ Parsed JSON: {result}")
                    return result
                    
                except json.JSONDecodeError as je:
                    print(f"❌ JSON Parse Error: {je}")
                    print(f"Raw content: {content}")
                    # Fallback: สร้าง response เอง
                    user_msg = messages[-1]['content'].lower()
                    
                    if any(word in user_msg for word in ['สร้าง', 'ทำ', 'build', 'create']):
                        if any(word in user_msg for word in ['todo', 'งาน', 'รายการ']):
                            app_type = "todo_app"
                        elif any(word in user_msg for word in ['ร้าน', 'shop', 'ขาย']):
                            app_type = "shop_app"
                        else:
                            app_type = "todo_app"
                        
                        return {
                            "action": "build_app",
                            "message": f"เข้าใจแล้ว! จะสร้างแอป {app_type} ให้เลย 🚀\n\n{content}",
                            "requirements": {
                                "app_type": app_type,
                                "description": content,
                                "features": ["ฟีเจอร์หลัก", "การจัดการข้อมูล"]
                            }
                        }
                    else:
                        return {
                            "action": "ask_question",
                            "message": content
                        }
            else:
                raise Exception("No OpenAI API key")
                
        except Exception as e:
            print(f"🔄 OpenAI Error, using fallback: {e}")
            
            # Fallback mode - ใช้ตรรกะแบบเดิม
            user_msg = messages[-1]['content'].lower()
            
            if any(word in user_msg for word in ['todo', 'task', 'งาน', 'ทำ', 'รายการ']):
                return {
                    "action": "build_app",
                    "message": "เข้าใจแล้ว! จะสร้างแอป Todo List ให้เลย 🚀 (Fallback Mode)",
                    "requirements": {
                        "app_type": "todo_app",
                        "description": "แอปจัดการรายการงาน",
                        "features": ["เพิ่มงาน", "ลบงาน", "เช็คเสร็จ"]
                    }
                }
            elif any(word in user_msg for word in ['shop', 'ร้าน', 'ขาย', 'สินค้า']):
                return {
                    "action": "build_app", 
                    "message": "เยิ่ม! จะสร้างแอปร้านค้าออนไลน์ให้ 🛍️ (Fallback Mode)",
                    "requirements": {
                        "app_type": "shop_app",
                        "description": "แอปร้านค้าออนไลน์",
                        "features": ["แสดงสินค้า", "เพิ่มลงตะกร้า", "จัดการคำสั่งซื้อ"]
                    }
                }
            else:
                return {
                    "action": "ask_question",
                    "message": f"สวัสดี! อยากให้ฉันสร้างแอปอะไรให้คะ? เช่น Todo List, ร้านค้า, หรือแอปอื่นๆ 😊\n\n(Mode: {'Real AI' if self.use_real_ai else 'Fallback'})"
                }

    def generate_plan(self, requirements: Dict) -> Dict:
        """สร้างแผนการพัฒนา ให้ AI ประเมินเอง"""
        if self.use_real_ai:
            try:
                prompt = f"""วิเคราะห์และสร้างแผนการพัฒนาแอป:

ความต้องการ: {requirements}

สร้าง JSON plan ที่ครบถ้วน:
{{
    "app_name": "ชื่อแอปที่เหมาะสม", 
    "description": "คำอธิบายแอปอย่างละเอียด",
    "app_type": "ประเภทแอป",
    "platform": "แพลตฟอร์ม",
    "features": ["ฟีเจอร์1", "ฟีเจอร์2"],
    "ui_theme": "ธีม UI ที่เหมาะสม",
    "color_scheme": "โทนสี",
    "target_audience": "กลุ่มเป้าหมาย"
}}"""

                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=400
                )
                
                content = response.choices[0].message.content.strip()
                
                # Parse JSON response
                try:
                    if '```json' in content:
                        json_part = content.split('```json')[1].split('```')[0]
                    elif '{' in content:
                        json_part = content[content.find('{'):content.rfind('}')+1]
                    else:
                        json_part = content
                        
                    plan = json.loads(json_part)
                    print(f"🎯 AI Generated Plan: {plan}")
                    return plan
                except:
                    print("⚠️ Failed to parse AI plan, using fallback")
                    
            except Exception as e:
                print(f"⚠️ AI Plan Error: {e}")
        
        # Fallback plan
        return {
            "app_name": "Amazing App",
            "description": requirements.get("description", "แอปสุดเจ๋งที่สร้างด้วย AI"),
            "app_type": requirements.get("app_type", "webapp"),
            "features": requirements.get("features", ["ใช้งานง่าย", "สวยงาม"])
        }

    def generate_code(self, file_type: str, plan: Dict) -> str:
        """สร้างโค้ดด้วย AI จริงๆ"""
        if file_type != "frontend":
            return "# Backend/Database code would go here"
            
        app_name = plan.get('app_name', 'Amazing App')
        description = plan.get('description', 'แอปที่สร้างด้วย AI')
        app_type = plan.get('app_type', 'webapp')
        features = plan.get('features', [])
        ui_theme = plan.get('ui_theme', 'modern')
        
        # ใช้ AI สร้างโค้ดจริงๆ
        if self.use_real_ai:
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
                
                print(f"🎨 AI Generated {len(ai_code)} chars of code for {app_name}")
                return ai_code
                
            except Exception as e:
                print(f"⚠️ AI Code Generation Error: {e}")
                print("Falling back to template...")
                
                # ลบ markdown code block ถ้ามี
                if '```html' in ai_code:
                    ai_code = ai_code.split('```html')[1].split('```')[0].strip()
                elif '```' in ai_code:
                    ai_code = ai_code.split('```')[1].split('```')[0].strip()
                
                print(f"🤖 AI Generated {len(ai_code)} characters of code")
                
                # ตรวจสอบว่าเป็น HTML ที่ถูกต้อง
                if '<!DOCTYPE html>' in ai_code or '<html' in ai_code:
                    return ai_code
                else:
                    print("❌ AI code doesn't look like valid HTML, using template")
                    
            except Exception as e:
                print(f"❌ AI Code Generation Error: {e}")
        
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

# เซิร์ฟเวอร์
app = FastAPI(title="🚀 Lovable Clone - AI App Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class ExcitingLovableAI:
    """AI ที่สร้างแอปแบบ Exciting พร้อม Realtime Effects!"""
    
    def __init__(self):
        self.app_counter = 0
        self.workspace_dir = Path("generated_apps")
        self.workspace_dir.mkdir(exist_ok=True)

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
            
            frontend_code = real_ai.generate_code("frontend", plan)
            await self._create_file_with_typing(
                websocket,
                f"{app_name}/index.html",
                frontend_code,
                "หน้าเว็บหลัก (Frontend)"
            )
            
            # 🎯 ขั้นที่ 4: ส่ง preview
            await websocket.send_json({
                "type": "preview_ready",
                "html_content": frontend_code,
                "app_name": plan["app_name"],
                "progress": 80
            })
            
            await asyncio.sleep(1)
            
            # 🎯 ขั้นที่ 5: เสร็จสิ้น!
            await websocket.send_json({
                "type": "build_complete",
                "message": f"🎉 สร้าง {plan['app_name']} สำเร็จ! ใช้งานได้เลย",
                "app_path": f"generated_apps/{app_name}",
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
    
    try:
        # ให้ AI ตัดสินใจ
        decision = real_ai.chat_decide(session['messages'])
        
        # เพิ่มข้อความตอบกลับ
        session['messages'].append({
            "role": "assistant",
            "content": decision['message']
        })
        
        return {
            "response": decision['message'],
            "action": decision['action'],
            "session_id": session_id,
            "requirements": decision.get('requirements'),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Chat error: {str(e)}"}
        )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket สำหรับ realtime app building"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("action") == "build_app":
                requirements = data.get("requirements", {})
                await exciting_ai.generate_app_exciting(websocket, requirements)
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_mode": "real" if real_ai.use_real_ai else "demo",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Exciting Lovable Backend...")
    print("🤖 Using demo mode - set OPENAI_API_KEY for real AI")
    print("📍 Server: http://localhost:8006")
    print("🔌 WebSocket: ws://localhost:8006/ws")
    uvicorn.run(app, host="0.0.0.0", port=8006, log_level="info")