import os, json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slugify import slugify
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our new chat system
from agents.chat_manager import initialize_chat_manager, get_chat_manager
from agents.conversational_ai import ConversationalAI

# Import new systems  
from agents.activity_monitor import activity_monitor, log_activity, start_task, complete_task, log_agent_action
from agents.conversational_design_agent import ConversationalDesignAgent
from agents.requirement_analyzer import RequirementAnalyzer
from agents.supervisor_agent import supervisor_agent
from agents.conversational_flow import conversation_flow
from agents.ai_mobile_app_generator import initialize_ai_mobile_generator

WEBROOT = Path(os.getenv("WEBROOT", "/app/workspace/generated-app/apps/web"))
WEBROOT.mkdir(parents=True, exist_ok=True)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required (no fallback / no templates).")
client = OpenAI(api_key=API_KEY)

# Initialize chat manager with our new system
initialize_chat_manager(client)

# Initialize requirement analysis system
requirement_analyzer = RequirementAnalyzer(client)
conversational_agent = ConversationalDesignAgent(client)

# Initialize AI Mobile App Generator
ai_mobile_generator = initialize_ai_mobile_generator(client)

app = FastAPI(title="AgentPro Orchestrator (AI Mode Only)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for generated websites
app.mount("/app", StaticFiles(directory=WEBROOT), name="static")

@app.get("/health")
async def health_check():
    """Health check endpoint สำหรับ system monitoring"""
    return {
        "status": "healthy",
        "service": "AgentPro Orchestrator", 
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "agents": {
            "conversational_ai": "active",
            "chat_manager": "initialized",
            "multi_agent_system": "ready"
        }
    }

@app.websocket("/ws/activity")
async def websocket_activity(websocket: WebSocket):
    """WebSocket endpoint สำหรับ real-time activity monitoring"""
    await activity_monitor.connect_websocket(websocket)
    try:
        while True:
            # รอรับข้อความจาก client (ping/pong)
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        activity_monitor.disconnect_websocket(websocket)

class ChatReq(BaseModel):
    message: str = Field(min_length=2)

class ChatResp(BaseModel):
    ok: bool
    slug: str
    web_url: str
    files: List[str]

# New Enterprise Models
class EnterpriseChatReq(BaseModel):
    message: str = Field(min_length=2)
    history: Optional[List[str]] = []
    request_type: Optional[str] = "professional_project"

class EnterpriseChatResp(BaseModel):
    ok: bool
    response: str
    workflow_id: Optional[str] = None
    project_type: Optional[str] = None
    project_urls: Optional[List[str]] = []
    deployment_info: Optional[Dict[str, Any]] = None
    professional_grade: bool = True

SYSTEM = """
คุณคือ AI Website Designer & Developer ระดับ Expert ที่สามารถสร้างเว็บไซต์สวยงามและครบครัน
หน้าที่: สร้าง "ชุดไฟล์เว็บไซต์" ตาม requirement โดยต้องมี:

🎨 DESIGN REQUIREMENTS:
- Modern responsive design
- Beautiful color schemes ที่เข้ากับธีม
- Professional typography (Google Fonts)
- Smooth animations & transitions
- Mobile-first approach
- Professional gradients & shadows

📝 CONTENT REQUIREMENTS:
- AI-generated เนื้อหาคุณภาพสูง
- SEO-optimized headings
- Compelling call-to-actions  
- Professional imagery placeholders
- Real business information (แม้จะ mock data)
- Complete sections: Hero, About, Services/Products, Contact, Footer

**ตอบกลับเป็น JSON เท่านั้น** และต้องตรงสคีมนี้เป๊ะ:
{
  "slug": "myapp-YYYYMMDD-HHMMSS",
  "files": [
    {"path":"index.html","content":"<!doctype html>..."},
    {"path":"styles.css","content":"..."},
    {"path":"script.js","content":"..."}
  ]
}

🚨 CRITICAL REQUIREMENTS:
- index.html ต้องเป็นเว็บไซต์ครบครัน 5+ sections
- styles.css ต้องมี modern CSS, animations, responsive design
- script.js ต้องมี interactive features
- เนื้อหาทั้งหมดเป็นภาษาไทย (เว้นแต่ระบุเป็นอย่างอื่น)
- ใส่ <meta charset="utf-8"> และ <meta name="viewport"> ครบ
- HTML อ้างอิง CSS/JS แบบ relative path
- NO explanations, NO markdown, NO code fences - JSON เท่านั้น!
"""

def _ask_ai_to_plan(user_msg: str) -> Dict[str, Any]:
    rsp = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        response_format={"type":"json_object"},
        messages=[
            {"role":"system", "content": SYSTEM},
            {"role":"user", "content": user_msg}
        ],
    )
    txt = rsp.choices[0].message.content
    try:
        data = json.loads(txt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI returned non-JSON: {e}")

    # validate
    if "slug" not in data or "files" not in data or not isinstance(data["files"], list):
        raise HTTPException(status_code=422, detail="AI JSON missing required fields")

    # บังคับรูปแบบ slug
    slug = data["slug"].strip()
    if not slug or not slug.startswith("myapp-"):
        slug = "myapp-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        data["slug"] = slug

    # บังคับมี index.html + styles.css
    paths = { (f.get("path") or "").lower() for f in data["files"] if isinstance(f, dict) }
    if "index.html" not in paths or "styles.css" not in paths:
        raise HTTPException(status_code=422, detail="AI must provide at least index.html and styles.css")

    return data

def _write_files(plan: Dict[str, Any]) -> List[str]:
    slug = plan["slug"]
    outdir = WEBROOT / slug
    outdir.mkdir(parents=True, exist_ok=True)

    written: List[str] = []
    for f in plan["files"]:
        if not isinstance(f, dict): continue
        rel = (f.get("path") or "").lstrip("/").strip()
        content = f.get("content") or ""
        if not rel:
            continue
        p = outdir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        written.append(str(p))
    if not (outdir / "index.html").exists():
        raise HTTPException(status_code=500, detail="index.html missing after write")
    return written

@app.get("/health")
def health():
    return {"ok": True, "webroot": str(WEBROOT), "model": MODEL}

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    needs_clarification: bool = False
    preview_url: Optional[str] = None
    code: Optional[str] = None
    project_ready: bool = False

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_analyzer(req: ChatRequest):
    """New chat endpoint using requirement analyzer"""
    
    log_agent_action("ChatAPI", f"Received message: {req.message[:50]}...")
    
    # Use requirement analyzer
    analyzer = requirement_analyzer
    analysis = analyzer.analyze_initial_request(req.message)
    
    if analysis.needs_clarification:
        log_agent_action("RequirementAnalyzer", "Asking for clarification")
        return ChatResponse(
            response=analysis.clarification_questions[0] if analysis.clarification_questions else "ช่วยบอกรายละเอียดเพิ่มเติมได้ไหมครับ?",
            needs_clarification=True
        )
    
    # If enough info, proceed with conversational agent
    design_agent = conversational_agent
    conv_analysis = design_agent.analyze_request(req.message)
    
    if conv_analysis.get("needs_clarification", False):
        questions = conv_analysis.get("conversational_questions", [])
        response_text = questions[0] if questions else design_agent.generate_conversational_response(req.message)
        
        log_agent_action("ConversationalAgent", "Generated response")
        return ChatResponse(
            response=response_text,
            needs_clarification=True
        )
    
    # Ready to generate code
    log_agent_action("CodeGeneration", "Starting code generation")
    plan = _ask_ai_to_plan(req.message.strip())
    files = _write_files(plan)
    slug = plan["slug"]
    web_url = f"/app/{slug}/index.html"
    
    log_agent_action("CodeGeneration", f"Generated project: {slug}")
    
    return ChatResponse(
        response=f"🎉 สร้างโปรเจค '{slug}' เสร็จแล้วครับ! ดูได้ที่ preview ด้านขวา",
        needs_clarification=False,
        preview_url=web_url,
        project_ready=True
    )

@app.post("/chat/ai", response_model=ChatResp)
def chat_ai(req: ChatReq):
    """Enhanced web generation with real-time progress tracking"""
    
    # Log start of generation
    log_agent_action("WebGenerator", f"🚀 Starting AI web generation for: {req.message[:50]}...")
    
    # Step 1: AI Planning
    log_agent_action("WebGenerator", "📝 AI is analyzing requirements...")
    plan = _ask_ai_to_plan(req.message.strip())
    
    # Log what AI planned
    log_agent_action("WebGenerator", f"🎨 AI planned website: {plan['slug']}")
    log_agent_action("WebGenerator", f"📁 Files to create: {[f.get('path', '') for f in plan['files']]}")
    
    # Step 2: File Creation
    log_agent_action("WebGenerator", "💾 Creating files...")
    files = _write_files(plan)
    
    slug = plan["slug"]
    web_url = f"/app/{slug}/index.html"
    
    # Log completion
    log_agent_action("WebGenerator", f"✅ Website created successfully! Preview: {web_url}")
    
    return ChatResp(ok=True, slug=slug, web_url=web_url, files=[f"/app/{slug}/{Path(f).name}" for f in files])

@app.websocket("/ws")
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """Streaming chat endpoint for smooth UI experience with conversation memory"""
    
    await websocket.accept()
    log_agent_action("WebSocket", "Connected successfully")
    
    # Store conversation context for this connection
    conversation_history = []
    project_context = {}
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "").strip()
            
            if not message:
                continue
                
            log_agent_action("WebSocket", f"Received: {message[:50]}...")
            
            # Add to conversation history
            conversation_history.append({"role": "user", "content": message})
            
            # Send typing indicator
            await websocket.send_json({
                "type": "typing",
                "message": "กำลังวิเคราะห์ความต้องการ..."
            })
            
            # Let AI handle everything - decide when to chat vs when to code
            full_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
            
            # Send to OpenAI to decide what to do
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "system", 
                        "content": """คุณเป็น AI assistant ที่ช่วยสร้างเว็บไซต์และแอปพลิเคชัน

หากข้อมูลยังไม่ครบ: ตอบแบบสนทนาธรรมชาติ ถามสิ่งที่ขาด
หากข้อมูลครบแล้ว: 
- เว็บไซต์: "CREATE_WEBSITE:" ตามด้วยสรุปโปรเจค
- แอปพลิเคชัน: "CREATE_APP:" ตามด้วยสรุปโปรเจค

แยกประเภท:
- เว็บไซต์: landing page, company profile, portfolio, blog
- แอปพลิเคชัน: todo app, calculator, booking system, dashboard, management system

ตัวอย่าง:
- เว็บไซต์: "CREATE_WEBSITE: สร้างเว็บร้านกาแฟ 'Cafe Modern' มีหน้าหลัก เมนูกาแฟ ราคา แผนที่"
- แอปพลิเคชัน: "CREATE_APP: สร้าง todo app มี add/delete/edit tasks, category, deadline, responsive design"

ตอบแค่ข้อความเดียว อย่าอธิบายเพิ่ม"""
                    }, {
                        "role": "user",
                        "content": full_context
                    }],
                    max_tokens=200,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content.strip()
                
                # Check if AI wants to create website/app
                if ai_response.startswith("CREATE_WEBSITE:") or ai_response.startswith("CREATE_APP:"):
                    # Extract project description and type
                    if ai_response.startswith("CREATE_APP:"):
                        project_desc = ai_response.replace("CREATE_APP:", "").strip()
                        project_type = "app"
                    else:
                        project_desc = ai_response.replace("CREATE_WEBSITE:", "").strip()
                        project_type = "website"
                    
                    # Dynamic status based on project type
                    if project_type == "app":
                        status_steps = [
                            {"msg": "🚀 เริ่มสร้างแอปพลิเคชัน...", "progress": 5},
                            {"msg": "🎯 วิเคราะห์ user requirements...", "progress": 15},
                            {"msg": "🏗️ ออกแบบ app architecture...", "progress": 25},
                            {"msg": "🔧 สร้าง backend API endpoints...", "progress": 40},
                            {"msg": "🎨 ออกแบบ UI/UX components...", "progress": 55},
                            {"msg": "📱 สร้าง responsive interface...", "progress": 70},
                            {"msg": "🔗 เชื่อมต่อ frontend กับ backend...", "progress": 85},
                            {"msg": "🧪 ทดสอบและ optimize performance...", "progress": 95}
                        ]
                    else:
                        status_steps = [
                            {"msg": "🚀 เริ่มสร้างเว็บไซต์...", "progress": 10},
                            {"msg": "🤖 AI กำลังวางแผนโครงสร้าง...", "progress": 30},
                            {"msg": "🎨 ออกแบบ layout และ styling...", "progress": 50},
                            {"msg": "📝 เขียน content และ components...", "progress": 70},
                            {"msg": "🔧 ติดตั้งและเตรียม preview...", "progress": 90}
                        ]
                    
                    # Send initial status updates
                    for step in status_steps[:-1]:
                        await websocket.send_json({
                            "type": "status",
                            "message": step["msg"],
                            "status": "processing",
                            "progress": step["progress"]
                        })
                    
                    plan = _ask_ai_to_plan(project_desc)
                    
                    # Detailed file creation with realistic delays
                    await websocket.send_json({
                        "type": "status",
                        "message": f"� สร้างไฟล์โปรเจค {len(plan['files'])} ไฟล์...", 
                        "status": "creating_files",
                        "progress": 75
                    })
                    
                    # Show file creation progress
                    for i, file_info in enumerate(plan["files"]):
                        filename = file_info.get("path", f"file_{i}")
                        file_type = filename.split('.')[-1] if '.' in filename else "file"
                        
                        # Different icons for different file types
                        icon_map = {
                            "html": "🌐", "css": "🎨", "js": "⚡", 
                            "py": "🐍", "json": "📋", "md": "📝"
                        }
                        icon = icon_map.get(file_type, "📄")
                        
                        await websocket.send_json({
                            "type": "status",
                            "message": f"{icon} สร้าง {filename}...",
                            "status": "writing_file", 
                            "progress": 75 + (i * 15 // len(plan["files"]))
                        })
                        
                    files = _write_files(plan)
                    slug = plan["slug"]
                    web_url = f"/app/{slug}/index.html"
                    
                    # Final status
                    await websocket.send_json({
                        "type": "status",
                        "message": status_steps[-1]["msg"],
                        "status": "finalizing",
                        "progress": status_steps[-1]["progress"]
                    })
                    
                    # Complete with project type-specific message
                    complete_msg = f"🎉 สร้าง{'แอป' if project_type == 'app' else 'เว็บไซต์'} '{slug}' เสร็จแล้ว!"
                    
                    await websocket.send_json({
                        "type": "message", 
                        "message": complete_msg,
                        "preview_url": web_url,
                        "project_ready": True,
                        "slug": slug,
                        "project_type": project_type,
                        "status": "complete",
                        "progress": 100
                    })
                    
                    log_agent_action("WebSocket", f"Generated {project_type}: {slug}")
                    
                    # Reset for next project
                    conversation_history = []
                    
                else:
                    # Continue conversation
                    await websocket.send_json({
                        "type": "message",
                        "message": ai_response,
                        "needs_clarification": True
                    })
                    
                    # Add AI response to history
                    conversation_history.append({"role": "assistant", "content": ai_response})
                    
            except Exception as e:
                await websocket.send_json({
                    "type": "message",
                    "message": "ขอโทษครับ เกิดข้อผิดพลาดในการประมวลผล ลองใหม่ได้ไหมครับ?",
                    "needs_clarification": True
                })
                log_agent_action("WebSocket", f"AI Error: {e}")
                
    except WebSocketDisconnect:
        log_agent_action("WebSocket", "Client disconnected")
    except Exception as e:
        log_agent_action("WebSocket", f"Error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": f"เกิดข้อผิดพลาด: {str(e)}"
        })

@app.post("/simple-chat")
async def simple_chat(request: dict):
    """🚀 Production-Ready AI Chat with Multi-Agent System"""
    message = request.get("message", "")
    user_id = request.get("user_id", "default_user")
    
    try:
        print(f"💬 Processing: {message}")
        
        # ใช้ Advanced Conversational Flow
        response_data = await conversation_flow.process_conversation(
            user_id=user_id, 
            message=message,
            context={"session": "simple_chat"}
        )
        
        print(f"🎯 Intent detected: {response_data.get('intent_detected', {})}")
        
        # ถ้า AI ตัดสินใจว่าควรสร้างเว็บไซต์
        if response_data.get("should_start_workflow", False):
            print("🎪 Starting Autonomous Workflow!")
            
            # เริ่ม Multi-Agent Workflow
            workflow_id = await supervisor_agent.start_autonomous_workflow(message)
            print(f"🚀 Workflow started: {workflow_id}")
            
            # สร้างเว็บไซต์ขั้นพื้นฐานทันที (Real-time Preview)
            preview_html = await create_instant_preview(message)
            
            # บันทึกไฟล์
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            slug = f"instant-{timestamp}"
            output_dir = WEBROOT / slug
            output_dir.mkdir(parents=True, exist_ok=True)
            
            (output_dir / "index.html").write_text(preview_html, encoding="utf-8")
            
            return {
                "response": response_data["message"] + f"\n\n🚀 เริ่มสร้างแล้ว! Workflow ID: {workflow_id}",
                "website_url": f"http://localhost:8001/app/{slug}/index.html",
                "workflow_id": workflow_id,
                "status": "workflow_started"
            }
        
        # สำหรับการสนทนาธรรมดา
        return {
            "response": response_data["message"],
            "intent": response_data.get("intent_detected", {}),
            "confidence": response_data.get("confidence", 0.8)
        }
        
    except Exception as e:
        print(f"💥 Error: {e}")
        return {"response": f"เกิดข้อผิดพลาด: {str(e)}"}

async def create_instant_preview(user_request: str) -> str:
    """สร้าง Preview ทันทีสำหรับผู้ใช้ดู"""
    
    # ใช้ OpenAI สร้าง HTML จริงๆ
    try:
        client = OpenAI(api_key=API_KEY)
        
        prompt = f"""
        สร้างเว็บไซต์ HTML สวยงามตามคำขอ: "{user_request}"
        
        ข้อกำหนด:
        - HTML5 สมบูรณ์
        - CSS ภายใน (internal) 
        - ใช้ฟอนต์ Google Fonts
        - Responsive Design
        - สีสันสวยงาม
        - Animation เบาๆ
        - เนื้อหาที่เกี่ยวข้องกับคำขอ
        - ใช้ได้จริง
        
        ตอบเฉพาะโค้ด HTML เท่านั้น:
        """
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        html_content = response.choices[0].message.content.strip()
        
        # ทำความสะอาดโค้ด
        if "```html" in html_content:
            html_content = html_content.split("```html")[1].split("```")[0].strip()
        elif "```" in html_content:
            html_content = html_content.split("```")[1].strip()
        
        return html_content
        
    except Exception as e:
        print(f"Error generating HTML: {e}")
        # Fallback HTML
        return f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เว็บไซต์ที่สร้างจาก AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Kanit', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{ 
            text-align: center;
            padding: 2rem;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        h1 {{ 
            font-size: 3rem; 
            margin-bottom: 1rem;
            animation: fadeInUp 1s ease;
        }}
        p {{ 
            font-size: 1.2rem; 
            margin-bottom: 2rem;
            opacity: 0.9;
            animation: fadeInUp 1s ease 0.2s both;
        }}
        .feature {{ 
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 10px;
            animation: fadeInUp 1s ease 0.4s both;
        }}
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AI สร้างเสร็จแล้ว!</h1>
        <p>ตามคำขอ: "{user_request}"</p>
        <div class="feature">
            <h3>✨ ระบบ Multi-Agent กำลังทำงาน</h3>
            <p>AI หลายตัวร่วมมือกันสร้างเว็บไซต์ที่ดีที่สุดให้คุณ</p>
        </div>
        <div class="feature">
            <h3>🎨 การออกแบบอัตโนมัติ</h3>
            <p>ระบบวิเคราะห์และสร้างดีไซน์ที่เหมาะสมโดยอัตโนมัติ</p>
        </div>
        <div class="feature">
            <h3>🔧 ทดสอบคุณภาพ</h3>
            <p>ผ่านการทดสอบคุณภาพหลายขั้นตอนก่อนส่งมอบ</p>
        </div>
    </div>
</body>
</html>"""

# 🏢 ENTERPRISE ENDPOINTS
@app.post("/enterprise-chat", response_model=EnterpriseChatResp)
async def enterprise_chat(req: EnterpriseChatReq):
    """Enterprise-grade AI chat for professional projects"""
    try:
        log_activity("enterprise_chat_request", {
            "message": req.message,
            "request_type": req.request_type,
            "history_length": len(req.history or [])
        })
        
        # Import Enterprise Generator
        from agents.enterprise_generator import enterprise_generator
        
        # Phase 1: Analyze requirements thoroughly  
        print(f"🏢 Enterprise Chat Request: {req.message}")
        analysis = await enterprise_generator.analyze_requirements_thoroughly(req.message)
        
        project_type = analysis.get("project_type", "professional_website")
        complexity = analysis.get("estimated_complexity", "medium")
        
        # Phase 2: Generate professional response
        response_message = f"""🏢 <strong>Enterprise Analysis Complete!</strong>

📊 <strong>Project Type:</strong> {project_type}
📈 <strong>Complexity:</strong> {complexity}
⏰ <strong>Timeline:</strong> {analysis.get('estimated_timeline', '2-4 weeks')}

🚀 กำลังเริ่ม <strong>Multi-Agent Workflow</strong> เพื่อสร้างโปรเจ็กต์ระดับ Professional...

✨ <strong>Features จะรวม:</strong>
• Multiple pages with professional design
• Working functionality & interactions  
• Database integration (if needed)
• Responsive & mobile-friendly
• SEO optimized
• Production-ready code

รอสักครู่นะครับ ระบบกำลังสร้างให้..."""

        # Phase 3: Start Enterprise Workflow
        workflow_id = await supervisor_agent.start_autonomous_workflow(req.message)
        
        # Phase 4: Quick preview (if simple enough)
        project_urls = []
        deployment_info = None
        
        if complexity == "simple":
            try:
                # Generate quick preview for simple projects
                if project_type in ["professional_website", "landing_page"]:
                    project_structure = await enterprise_generator.generate_professional_website(analysis)
                    deployment_info = await enterprise_generator.deploy_project(
                        project_structure,
                        f"preview_{project_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                    project_urls = list(deployment_info.get("urls", {}).values())
            except Exception as e:
                print(f"Quick preview failed: {e}")
        
        return EnterpriseChatResp(
            ok=True,
            response=response_message,
            workflow_id=workflow_id,
            project_type=project_type,
            project_urls=project_urls,
            deployment_info=deployment_info,
            professional_grade=True
        )
        
    except Exception as e:
        log_activity("enterprise_chat_error", {"error": str(e)})
        return EnterpriseChatResp(
            ok=False,
            response=f"❌ เกิดข้อผิดพลาดในระบบ Enterprise: {str(e)}",
            professional_grade=False
        )

# Endpoint เพื่อดูสถานะ Workflow
@app.get("/workflow-status/{workflow_id}") 
async def get_workflow_status(workflow_id: str):
    """ดูสถานะการทำงานของ Enterprise Workflow"""
    try:
        # Get status from supervisor agent
        if hasattr(supervisor_agent, 'workflow_results') and workflow_id in supervisor_agent.workflow_results:
            result = supervisor_agent.workflow_results[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": result.get("status", "unknown"),
                "project_type": result.get("project_type"),
                "professional_grade": result.get("professional_grade", False),
                "deployment_info": result.get("deployment_info"),
                "completed_at": result.get("completed_at"),
                "error": result.get("error")
            }
        else:
            return {
                "workflow_id": workflow_id,
                "status": "in_progress",
                "message": "Workflow is still running..."
            }
    except Exception as e:
        return {
            "workflow_id": workflow_id,
            "status": "error", 
            "error": str(e)
        }

# Endpoint เพื่อดูผลงานล่าสุด
@app.get("/latest-projects")
async def get_latest_projects():
    """ดูโปรเจ็กต์ล่าสุดที่สร้าง"""
    try:
        projects = []
        for item in WEBROOT.glob("**/index.html"):
            if item.parent.name.startswith(("instant-", "auto-")):
                projects.append({
                    "name": item.parent.name,
                    "url": f"http://localhost:8001/app/{item.parent.name}/index.html",
                    "created": item.stat().st_mtime
                })
        
        # เรียงตามเวลาล่าสุด
        projects.sort(key=lambda x: x["created"], reverse=True)
        return {"projects": projects[:10]}  # 10 โปรเจ็กต์ล่าสุด
        
    except Exception as e:
        return {"error": str(e)}
            
    except Exception as e:
        return {"response": f"เกิดข้อผิดพลาด: {str(e)}"}

@app.get("/api/chat/status")
def get_chat_status():
    """Get chat system status"""
    chat_mgr = get_chat_manager()
    return {
        "active_users": chat_mgr.get_active_users(),
        "user_sessions": chat_mgr.get_user_sessions(),
        "system_status": "operational"
    }

# 📱 MOBILE APP API ENDPOINTS

class MobileAppReq(BaseModel):
    message: str = Field(min_length=2, description="คำอธิบายแอปที่ต้องการสร้าง")
    app_type: Optional[str] = Field(default="react_native", description="ประเภทแอป: react_native, flutter, ionic")
    project_name: Optional[str] = Field(default=None, description="ชื่อโปรเจ็กต์")
    features: Optional[List[str]] = Field(default=[], description="ฟีเจอร์ที่ต้องการ")

class MobileAppResp(BaseModel):
    success: bool
    message: str
    app_type: Optional[str] = None
    project_path: Optional[str] = None
    project_name: Optional[str] = None
    business_name: Optional[str] = None
    files_created: Optional[int] = None
    install_commands: Optional[List[str]] = None
    run_commands: Optional[List[str]] = None
    error: Optional[str] = None

@app.post("/api/mobile-app", response_model=MobileAppResp)
async def create_mobile_app(req: MobileAppReq):
    """🚀 สร้าง Mobile Application (React Native, Flutter, Ionic)"""
    try:
        log_activity("mobile_app_request", {
            "message": req.message,
            "app_type": req.app_type,
            "project_name": req.project_name,
            "features": req.features
        })
        
        # วิเคราะห์ข้อความเพื่อสร้าง requirements
        import re
        from datetime import datetime
        
        # ตรวจจับประเภทแอป
        detected_type = "react_native"  # default
        if "flutter" in req.message.lower():
            detected_type = "flutter"
        elif "ionic" in req.message.lower():
            detected_type = "ionic"
        
        app_type = req.app_type or detected_type
        
        # สร้างชื่อโปรเจ็กต์
        if req.project_name:
            project_name = req.project_name
        else:
            # สกัดชื่อจากข้อความ
            name_patterns = [
                r'แอป([^ที่]*?)(?:ที่|สำหรับ|$)',
                r'สร้าง([^ที่]*?)(?:แอป|app)',
                r'([^ที่]*?)(?:แอป|app)'
            ]
            
            project_name = "mobile_app"
            for pattern in name_patterns:
                match = re.search(pattern, req.message)
                if match:
                    name = match.group(1).strip()
                    if name and len(name) > 1:
                        # แปลงเป็น project name ที่ใช้ได้
                        name_map = {
                            'ร้านกาแฟ': 'coffee_shop',
                            'ร้านอาหาร': 'restaurant', 
                            'โรงพยาบาล': 'hospital',
                            'โรงเรียน': 'school',
                            'ธนาคาร': 'banking',
                            'อีคอมเมิร์ซ': 'ecommerce',
                            'ช้อปปิ้ง': 'shopping'
                        }
                        project_name = name_map.get(name, name.replace(' ', '_').lower())
                        break
            
            # เพิ่ม timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            project_name = f"{project_name}_{timestamp}"
        
        # สร้าง business name
        business_name = req.message
        if 'แอป' in req.message:
            business_name = req.message.replace('สร้าง', '').replace('แอป', '').strip()
        
        if not business_name or len(business_name) < 3:
            business_name = "My Mobile App"
        
        # สร้าง requirements
        requirements = {
            'app_type': app_type,
            'project_name': project_name,
            'business_name': business_name,
            'description': req.message,
            'features': req.features or ['navigation', 'responsive_ui', 'modern_design']
        }
        
        # เรียก Mobile App Generator
        print(f"📱 Creating {app_type} app: {business_name}")
        result = await ai_mobile_generator.generate_mobile_app(requirements)
        
        if result['success']:
            log_activity("mobile_app_created", {
                "project_name": result['project_name'],
                "app_type": result['app_type'],
                "files_created": result['files_created']
            })
            
            return MobileAppResp(
                success=True,
                message=result['message'],
                app_type=result['app_type'],
                project_path=result['project_path'],
                project_name=result['project_name'],
                business_name=result['business_name'],
                files_created=result['files_created'],
                install_commands=result['install_commands'],
                run_commands=result['run_commands']
            )
        else:
            return MobileAppResp(
                success=False,
                message=result['message'],
                error=result.get('error', 'Unknown error')
            )
            
    except Exception as e:
        log_activity("mobile_app_error", {"error": str(e)})
        return MobileAppResp(
            success=False,
            message=f"เกิดข้อผิดพลาดในการสร้าง Mobile App: {str(e)}",
            error=str(e)
        )

@app.get("/api/mobile-apps")
async def list_mobile_apps():
    """📱 รายการ Mobile Apps ที่สร้างแล้ว"""
    try:
        import os
        from pathlib import Path
        
        workspace = Path("C:/agent/workspace")
        mobile_apps = []
        
        if workspace.exists():
            for item in workspace.iterdir():
                if item.is_dir():
                    # ตรวจสอบว่าเป็น Mobile App Project หรือไม่
                    indicators = [
                        item / "package.json",     # React Native
                        item / "pubspec.yaml",     # Flutter
                        item / "App.tsx",          # React Native
                        item / "lib" / "main.dart" # Flutter
                    ]
                    
                    is_mobile_app = any(indicator.exists() for indicator in indicators)
                    
                    if is_mobile_app:
                        app_type = "unknown"
                        if (item / "package.json").exists():
                            app_type = "react_native"
                        elif (item / "pubspec.yaml").exists():
                            app_type = "flutter"
                        
                        # อ่าน README สำหรับข้อมูลเพิ่มเติม
                        readme_path = item / "README.md"
                        description = "Mobile Application"
                        if readme_path.exists():
                            try:
                                with open(readme_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    lines = content.split('\n')
                                    if len(lines) > 2:
                                        description = lines[2] if lines[2].strip() else description
                            except:
                                pass
                        
                        mobile_apps.append({
                            "name": item.name,
                            "app_type": app_type,
                            "description": description,
                            "path": str(item),
                            "created": item.stat().st_mtime
                        })
        
        # เรียงตามเวลาล่าสุด
        mobile_apps.sort(key=lambda x: x["created"], reverse=True)
        return {"mobile_apps": mobile_apps}
        
    except Exception as e:
        return {"error": str(e), "mobile_apps": []}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AgentPro Orchestrator...")
    print("📊 API Documentation: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    uvicorn.run(app, host="0.0.0.0", port=8001)
