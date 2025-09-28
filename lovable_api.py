from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os
from datetime import datetime
from pathlib import Path
import uvicorn

# Import the main orchestrator
import sys
sys.path.append(str(Path(__file__).parent / "orchestrator"))
from main import _ask_ai_to_plan, _write_files, WEBROOT, client

app = FastAPI(title="Lovable Clone API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/generated", StaticFiles(directory=str(WEBROOT)), name="generated")

class ChatMessage(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    response: str
    preview_url: str = None
    code: str = None
    status: str = "success"

# Store conversations
conversations = {}

@app.get("/", response_class=HTMLResponse)
async def serve_landing():
    """Serve the Lovable landing page"""
    with open("lovable_landing.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/chat", response_class=HTMLResponse)
async def serve_chat():
    """Serve the Lovable chat interface"""
    with open("lovable_chat.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatMessage):
    """Main chat endpoint that processes user messages and generates code"""
    try:
        user_message = request.message.strip()
        conversation_id = request.conversation_id or f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize conversation if new
        if conversation_id not in conversations:
            conversations[conversation_id] = {
                "messages": [],
                "created_at": datetime.now().isoformat(),
                "last_preview": None
            }
        
        # Add user message to conversation
        conversations[conversation_id]["messages"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate AI response based on message type
        ai_response = generate_ai_response(user_message)
        
        # Add AI response to conversation
        conversations[conversation_id]["messages"].append({
            "role": "assistant", 
            "content": ai_response["response"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate code if needed
        preview_url = None
        generated_code = None
        
        if should_generate_code(user_message):
            try:
                # Use the orchestrator to generate the app
                plan = _ask_ai_to_plan(user_message)
                files = _write_files(plan)
                
                slug = plan["slug"]
                preview_url = f"/generated/{slug}/index.html"
                
                # Get the main HTML file content
                index_file = WEBROOT / slug / "index.html"
                if index_file.exists():
                    generated_code = index_file.read_text(encoding="utf-8")
                
                conversations[conversation_id]["last_preview"] = preview_url
                
            except Exception as e:
                print(f"Code generation error: {e}")
                ai_response["response"] += f"\n\n❌ เกิดข้อผิดพลาดในการสร้างโค้ด: {str(e)}"
        
        return ChatResponse(
            response=ai_response["response"],
            preview_url=preview_url,
            code=generated_code,
            status="success"
        )
        
    except Exception as e:
        print(f"Chat API error: {e}")
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาด: {str(e)}")

def should_generate_code(message: str) -> bool:
    """Determine if we should generate code based on the message"""
    code_keywords = [
        "สร้าง", "ทำ", "build", "create", "make", 
        "landing", "website", "web", "app", "page",
        "dashboard", "form", "shop", "store", "blog"
    ]
    
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in code_keywords)

def generate_ai_response(message: str) -> dict:
    """Generate AI response based on user message"""
    message_lower = message.lower()
    
    # Landing page responses
    if any(word in message_lower for word in ["landing", "หน้าแรก", "โฮมเพจ"]):
        return {
            "response": """🎨 เยี่ยมเลย! ผมจะสร้าง Landing Page สุดสวยให้คุณครับ

กำลังสร้าง:
✨ Hero section พร้อม gradient แบบ modern
📝 Call-to-action ที่ดึงดูดใจ
📱 Responsive design ทุกหน้าจอ
🚀 Performance optimization

ช่วงกรอกรายละเอียดเพิ่มเติม:
• ชื่อแบรนด์หรือบริษัท?
• สีหลักที่ชอบ?
• ข้อความหลักที่อยากสื่อ?"""
        }
    
    # Mobile app responses  
    elif any(word in message_lower for word in ["app", "แอป", "mobile", "โมบาย"]):
        return {
            "response": """📱 สุดยอด! ผมจะสร้าง Mobile App ให้คุณเลย

กำลังพัฒนา:
🏗️ App Architecture ที่แข็งแรง
🎯 User Experience Flow ที่ลื่นไหล
💾 Database Structure ที่เหมาะสม
🔐 Authentication System
📊 Analytics Integration

บอกผมได้มั้ยครับว่าเป็นแอปประเภทไหน?
(Social, E-commerce, Productivity, Gaming, etc.)"""
        }
    
    # Dashboard responses
    elif any(word in message_lower for word in ["dashboard", "แดชบอร์ด", "admin", "analytics"]):
        return {
            "response": """📊 เข้าใจแล้ว! Dashboard ที่ใช้งานง่ายกำลังมา

Features ที่จะมี:
📈 Real-time Charts & Graphs
📋 Data Tables with Filtering
🔔 Notification System
👥 User Management Panel
🎨 Dark/Light Theme Toggle
📤 Export Data Options

อยากให้แสดงข้อมูลอะไรใน dashboard บ้างครับ?"""
        }
    
    # E-commerce responses
    elif any(word in message_lower for word in ["shop", "ร้าน", "ecommerce", "store", "ขาย"]):
        return {
            "response": """🛒 เจ๋ง! ร้านค้าออนไลน์ระดับโปรกำลังมา

จะมี Features:
🎨 Product Showcase ที่สวยงาม
🛍️ Shopping Cart System
💳 Payment Integration
📦 Order Management
⭐ Review & Rating System
🔍 Search & Filter Products

ขายอะไรครับ? (เสื้อผ้า, อาหาร, อิเล็กทรอนิกส์, etc.)"""
        }
    
    # Blog responses
    elif any(word in message_lower for word in ["blog", "บล็อก", "article", "content"]):
        return {
            "response": """📝 ยอดเยี่ยม! Blog Platform สุดเท่กำลังมา

Features ครบครัน:
✍️ Rich Text Editor
📂 Category & Tags System
💬 Comment System
🔍 Search & Archive
📊 View Analytics
🌐 SEO Optimization

อยากเขียนเกี่ยวกับหัวข้ออะไรครับ?"""
        }
    
    # Portfolio responses
    elif any(word in message_lower for word in ["portfolio", "resume", "cv", "profile"]):
        return {
            "response": """💼 เท่มาก! Portfolio สุดเจ๋งกำลังมา

จะมี Sections:
👤 About Me ที่โดดเด่น
🎯 Skills & Expertise
💼 Work Experience
🚀 Project Showcase
📧 Contact Form
📱 Social Links

อยากโชว์ผลงานด้านไหนครับ? (Design, Development, Marketing, etc.)"""
        }
    
    # Default response
    else:
        return {
            "response": f"""✨ เข้าใจแล้วครับ! ผมจะช่วยสร้าง "{message}" ให้คุณ

🤖 AgentPro กำลังวิเคราะห์:
• Requirements Analysis
• UI/UX Design Planning
• Architecture Design
• Feature Planning
• Code Generation

กำลังเตรียมสร้างให้อยู่ครับ รอสักครู่นะ... 🚀"""
        }

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]

@app.get("/api/conversations")
async def list_conversations():
    """List all conversations"""
    return {
        "conversations": [
            {
                "id": conv_id,
                "created_at": conv_data["created_at"],
                "message_count": len(conv_data["messages"]),
                "last_preview": conv_data.get("last_preview")
            }
            for conv_id, conv_data in conversations.items()
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Lovable Clone API",
        "timestamp": datetime.now().isoformat(),
        "webroot": str(WEBROOT),
        "conversations_count": len(conversations)
    }

if __name__ == "__main__":
    print("🚀 Starting Lovable Clone API Server...")
    print(f"📁 Web files will be saved to: {WEBROOT}")
    print("🌐 Access the app at: http://localhost:8000")
    print("💬 Chat interface at: http://localhost:8000/chat")
    
    uvicorn.run(
        "lovable_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )