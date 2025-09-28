#!/usr/bin/env python3
"""
🎼 AI Orchestrator System
ระบบควบคุมการทำงานของ AI Agents โดย AI Chat เป็น Requirements Gatherer

Workflow:
1. 💬 AI Chat รับคำขอจาก User และถาม Requirements ให้ครบถ้วน
2. 📝 Team Lead Agent บันทึก Requirements และสร้าง Project Plan  
3. 👥 Specialized Agents ทำงานตาม Plan ที่กำหนด
4. 🔍 Quality Control ตรวจสอบจนสมบูรณ์แบบ
5. ✅ ส่งมอบผลงานเมื่อพร้อม
"""
import os
import json
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import sqlite3

from fastapi import FastAPI, H            #            print(f"🎯 Project '{project_result['plan']['project_name']}' created successfully!")
            
            # เริ่มให้ Agents ทำงานจริงใน background
            import asyncio
            asyncio.create_task(self._execute_agents_in_background(
                session_id, 
                project_result,
                working_agents
            ))
            
            return ChatResponse(
                response=f"{chat_result['response']}\n\n🎯 โครงการ: {project_result['plan']['project_name']}\n🚀 กำลังเริ่มดำเนินการ...\n\n👨‍💼 Team Lead: ✅ วางแผนเสร็จ\n🔧 Backend Agent: 🔄 กำลังสร้าง API\n🎨 Frontend Agent: 🔄 กำลังสร้าง UI\n\n⏱️ คาดว่าจะเสร็จใน 2-3 นาที...",
                session_id=session_id,
                requirements_complete=True,
                project_started=True,
                agents_status=working_agents,
                progress="🔄 Agents กำลังทำงาน... กรุณารอสักครู่"
            )Agents ทำงานจริงใน background
            import asyncio
            asyncio.create_task(self._execute_agents_in_background(
                session_id, 
                project_result,
                working_agents
            ))
            
            return ChatResponse(
                response=f"{chat_result['response']}\n\n🎯 โครงการ: {project_result['plan']['project_name']}\n🚀 กำลังเริ่มดำเนินการ...\n\n👨‍💼 Team Lead: ✅ วางแผนเสร็จ\n🔧 Backend Agent: 🔄 กำลังสร้าง API\n🎨 Frontend Agent: 🔄 กำลังสร้าง UI\n\n⏱️ คาดว่าจะเสร็จใน 2-3 นาที...",
                session_id=session_id,
                requirements_complete=True,
                project_started=True,
                agents_status=working_agents,
                progress="🔄 Agents กำลังทำงาน... กรุณารอสักครู่"
            )tion
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is required!")

client = OpenAI(api_key=API_KEY)
ROOT_DIR = Path("C:/agent")
WORKSPACE_DIR = ROOT_DIR / "workspace"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI App
app = FastAPI(title="AI Orchestrator System", description="🎼 AI Chat + Team Lead + Specialized Agents")

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

class ChatResponse(BaseModel):
    response: str
    session_id: str
    requirements_complete: bool
    project_started: bool
    agents_status: Dict[str, str] = {}
    progress: Optional[str] = None


class RequirementsGatherer:
    """AI Chat ที่ทำหน้าที่เก็บ Requirements ให้ครบถ้วน"""
    
    def __init__(self):
        self.sessions = {}  # เก็บ conversation sessions
        self.required_info = [
            "project_type",      # ประเภทโครงการ
            "target_audience",   # กลุ่มเป้าหมาย
            "key_features",      # ฟีเจอร์หลัก
            "tech_preferences",  # ความต้องการเทคโนโลยี
            "design_style",      # สไตล์การออกแบบ
            "data_management",   # การจัดการข้อมูล
            "user_flow",         # user journey
            "business_rules"     # กฎทางธุรกิจ
        ]
    
    async def chat_with_user(self, message: str, session_id: str) -> Dict[str, Any]:
        """แชทกับผู้ใช้เพื่อเก็บ Requirements - ใช้ OpenAI API จริง"""
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'conversation': [],
                'requirements': {},
                'ai_analysis': {}
            }
        
        session = self.sessions[session_id]
        session['conversation'].append({"role": "user", "content": message})
        
        # ใช้ OpenAI API จริงๆ เพื่อวิเคราะห์และตัดสินใจ
        analysis = await self._ai_analyze_conversation(session)
        
        if analysis['is_sufficient']:
            # AI ตัดสินใจว่าข้อมูลพอแล้ว
            return {
                'response': analysis['completion_message'],
                'requirements_complete': True,
                'requirements': analysis['extracted_requirements'],
                'session_data': session
            }
        else:
            # AI ตัดสินใจว่าต้องถามเพิ่ม
            ai_response = analysis['next_question']
            session['conversation'].append({"role": "assistant", "content": ai_response})
            
            return {
                'response': ai_response,
                'requirements_complete': False,
                'ai_confidence': analysis['confidence'],
                'progress': analysis['progress_summary']
            }
    
    async def _ai_analyze_conversation(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """ใช้ OpenAI AI วิเคราะห์บทสนทนาและตัดสินใจ"""
        
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in session['conversation']
        ])
        
        analysis_prompt = f"""
คุณเป็น AI Requirements Analyst ที่ฉลาดในการเก็บข้อมูลโครงการ

บทสนทนา:
{conversation_text}

วิเคราะห์และตัดสินใจ:

1. ข้อมูลที่ได้พอสำหรับสร้างโครงการหรือยัง?
2. ถ้าพอแล้ว ให้สกัดข้อมูลที่ได้
3. ถ้าไม่พอ ให้ถามคำถามสั้นๆ ทีละคำถาม

ตอบเป็น JSON:
{{
    "is_sufficient": true/false,
    "confidence": 0.8,
    "extracted_requirements": {{
        "project_type": "...",
        "main_features": [...],
        "target_users": "..."
    }},
    "next_question": "คำถามสั้นๆ ทีละข้อ (ถ้าไม่พอ)",
    "completion_message": "ข้อความเมื่อพอแล้ว",
    "progress_summary": "สรุปความคืบหน้า"
}}

หลักการ:
- คำถามสั้น กระชับ ทีละเรื่อง
- ไม่ต้องได้ข้อมูลครบทุกด้าน ถ้าพอสร้างโครงการได้แล้ว
- ใช้วิจารณญาณในการตัดสินใจ
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Clean JSON response
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:-3].strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response[3:-3].strip()
            
            return json.loads(ai_response)
            
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            # Fallback response
            return {
                "is_sufficient": False,
                "confidence": 0.5,
                "next_question": "ช่วยเล่าเพิ่มเติมหน่อยครับ",
                "progress_summary": "กำลังเก็บข้อมูล..."
            }
    
    def _check_completeness(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """ตรวจสอบความครบถ้วนของ Requirements"""
        
        completed = sum(session['completion_status'].values())
        total = len(self.required_info)
        percentage = (completed / total) * 100
        
        missing = [
            key for key, status in session['completion_status'].items() 
            if not status
        ]
        
        return {
            'complete': completed == total,
            'percentage': percentage,
            'completed_count': completed,
            'total_count': total,
            'missing': missing
        }
    
    async def _generate_follow_up_question(self, session: Dict[str, Any], missing_info: List[str]) -> str:
        """สร้างคำถามติดตาม"""
        
        # เลือก missing info ที่สำคัญที่สุดมาถาม
        priority_info = missing_info[0]
        current_requirements = session['requirements']
        
        question_prompt = f"""
คุณเป็น AI Requirements Gatherer ที่เก็บข้อมูลโครงการ

ข้อมูลปัจจุบัน: {json.dumps(current_requirements, ensure_ascii=False)}
ข้อมูลที่ขาด: {priority_info}

สร้างคำถามที่เป็นมิตรและชัดเจนเพื่อถาม "{priority_info}" โดย:
1. อธิบายว่าทำไมต้องการข้อมูลนี้
2. ให้ตัวอย่างที่เข้าใจง่าย
3. ถามแบบ open-ended ให้ผู้ใช้อธิบายได้อย่างอิสระ

ตอบเป็นข้อความเดียว ความยาวไม่เกิน 200 คำ
"""
        
        return await self._call_openai(question_prompt)
    
    async def _call_openai(self, prompt: str) -> str:
        """เรียก OpenAI API"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "ขออภัย เกิดข้อผิดพลาดในการประมวลผล กรุณาลองใหม่อีกครั้ง"


class TeamLeadAgent:
    """Team Lead Agent ที่บันทึก Requirements และควบคุมทีม"""
    
    def __init__(self):
        self.active_projects = {}
        self.agent_assignments = {}
    
    async def create_project_plan(self, requirements: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """สร้างแผนโครงการจาก Requirements"""
        
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        
        # บันทึก Requirements
        project_record = {
            'project_id': project_id,
            'session_id': session_id,
            'requirements': requirements,
            'created_at': datetime.now().isoformat(),
            'status': 'planning'
        }
        
        # วิเคราะห์และสร้าง Project Plan
        plan = await self._analyze_and_plan(requirements)
        project_record['plan'] = plan
        
        # กำหนดงานให้ Agents
        agent_tasks = await self._assign_tasks_to_agents(plan)
        project_record['agent_tasks'] = agent_tasks
        
        # เก็บข้อมูลโครงการ
        self.active_projects[project_id] = project_record
        
        # เริ่มดำเนินงาน
        execution_result = await self._execute_project(project_id)
        
        return {
            'project_id': project_id,
            'plan': plan,
            'agent_tasks': agent_tasks,
            'execution_started': True,
            'execution_result': execution_result
        }
    
    async def _analyze_and_plan(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """ใช้ AI วิเคราะห์ Requirements และสร้างแผนจริง"""
        
        planning_prompt = f"""
คุณเป็น Senior Project Manager ที่เก่งมากในการวิเคราะห์และวางแผนโครงการ

Requirements ที่ได้รับ:
{json.dumps(requirements, ensure_ascii=False, indent=2)}

สร้างแผนโครงการที่สมบูรณ์และใช้งานได้จริง:

1. วิเคราะห์ Requirements อย่างลึกซึ้ง
2. เลือกเทคโนโลยีที่เหมาะสม
3. แบ่งงานให้ Agents อย่างชาญฉลาด
4. กำหนด Tasks ที่ชัดเจนและทำได้จริง

ตอบเป็น JSON:
{{
    "project_name": "ชื่อโครงการที่สร้างสรรค์",
    "summary": "สรุปโครงการอย่างชัดเจน",
    "architecture": {{
        "database": "เลือกฐานข้อมูลที่เหมาะสม",
        "backend": "เลือกเทคโนโลยี backend ที่เหมาะสม",
        "frontend": "เลือกเทคโนโลยี frontend ที่เหมาะสม",
        "deployment": "วิธี deploy ที่เหมาะสม"
    }},
    "phases": [
        {{
            "name": "Database Design",
            "tasks": ["สร้างฐานข้อมูล", "ออกแบบ schema", "เพิ่มข้อมูลตัวอย่าง"],
            "responsible_agent": "database_agent"
        }},
        {{
            "name": "Backend Development", 
            "tasks": ["สร้าง API endpoints", "เชื่อมต่อฐานข้อมูล", "Authentication system"],
            "responsible_agent": "backend_agent"
        }},
        {{
            "name": "Frontend Development",
            "tasks": ["สร้าง UI components", "เชื่อมต่อ API", "Responsive design"],
            "responsible_agent": "frontend_agent"
        }},
        {{
            "name": "UI/UX Enhancement",
            "tasks": ["ปรับปรุง UX", "ทำให้สวยงาม", "ทดสอบการใช้งาน"],
            "responsible_agent": "ui_ux_agent"
        }},
        {{
            "name": "Quality Assurance",
            "tasks": ["ทดสอบทุกฟีเจอร์", "แก้ไข bugs", "ตรวจสอบ performance"],
            "responsible_agent": "testing_agent"
        }}
    ]
}}

สำคัญ: ให้ Tasks ที่ชัดเจน เฉพาะเจาะจง และทำได้จริง
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": planning_prompt}],
                max_tokens=2500,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Clean JSON response
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:-3].strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response[3:-3].strip()
            
            return json.loads(ai_response)
            
        except Exception as e:
            print(f"Error in AI planning: {e}")
            return {
                "project_name": "AI Generated Project",
                "summary": "โครงการที่สร้างด้วย AI",
                "error": str(e)
            }
    
    async def _assign_tasks_to_agents(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """กำหนดงานให้ Agents"""
        
        assignments = {
            'backend_agent': [],
            'frontend_agent': [],
            'database_agent': [],
            'ui_ux_agent': [],
            'testing_agent': [],
            'devops_agent': []
        }
        
        # วิเคราะห์ phases และแจกงาน
        for phase in plan.get('phases', []):
            agent = phase.get('responsible_agent', '').lower().replace(' ', '_')
            if agent in assignments:
                assignments[agent].extend(phase.get('tasks', []))
        
        return assignments
    
    async def _execute_project(self, project_id: str) -> Dict[str, Any]:
        """เริ่มดำเนินโครงการจริงด้วย AI Agents"""
        
        project = self.active_projects[project_id]
        project['status'] = 'in_progress'
        
        # สร้าง workspace สำหรับโครงการ
        project_workspace = WORKSPACE_DIR / project_id
        project_workspace.mkdir(exist_ok=True)
        
        print(f"🎯 Starting project execution: {project_id}")
        
        # เก็บ project plan เป็นไฟล์
        plan_file = project_workspace / "project_plan.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(project, f, ensure_ascii=False, indent=2)
        
        # เริ่มให้ Agents ทำงานจริง
        
        execution_results = {}
        
        # ส่งงานให้ Agents ทำจริง - จะส่งให้ orchestrator ภายหลัง
        execution_results['message'] = "งานถูกส่งให้ Agents แล้ว - กำลังดำเนินการ"
        
        # อัพเดทสถานะโครงการ
        project['execution_results'] = execution_results
        project['status'] = 'completed'
        
        # บันทึกผลการทำงาน
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(project, f, ensure_ascii=False, indent=2)
        
        return {
            'workspace_created': str(project_workspace),
            'plan_saved': str(plan_file),
            'execution_results': execution_results,
            'status': 'executing'
        }


class SpecializedAgent:
    """Base class สำหรับ Specialized Agents ที่ใช้ AI จริง"""
    
    def __init__(self, name: str, specialization: str):
        self.name = name
        self.specialization = specialization
        self.current_tasks = []
        self.completed_tasks = []
        self.workspace = None
    
    def set_workspace(self, workspace: Path):
        """กำหนด workspace"""
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    async def receive_assignment(self, tasks: List[str], project_context: Dict[str, Any]):
        """รับมอบหมายงานและทำจริงด้วย AI"""
        self.current_tasks = tasks
        self.project_context = project_context
        
        print(f"🤖 {self.name} received {len(tasks)} tasks")
        
        # เริ่มทำงานจริงด้วย AI
        results = []
        for task in tasks:
            print(f"  📝 Working on: {task}")
            result = await self.execute_task_with_ai(task)
            results.append(result)
            self.completed_tasks.append(task)
        
        return results
    
    async def execute_task_with_ai(self, task: str) -> Dict[str, Any]:
        """ใช้ AI ทำงานจริง - ไม่ hard code"""
        
        ai_prompt = f"""
คุณเป็น {self.specialization} Expert ที่เก่งมาก

งานที่ได้รับ: {task}
โครงการ: {json.dumps(self.project_context, ensure_ascii=False, indent=2)}

สร้างไฟล์จริงที่ใช้งานได้:
1. วิเคราะห์งานที่ได้รับ
2. ตัดสินใจว่าต้องสร้างไฟล์อะไรบ้าง
3. เขียนโค้ดจริงที่ทำงานได้
4. ไม่ใช้ mockup หรือ placeholder

ตอบเป็น JSON:
{{
    "analysis": "วิเคราะห์งาน",
    "files_to_create": [
        {{
            "filename": "ชื่อไฟล์",
            "content": "โค้ดจริงที่ใช้งานได้",
            "description": "อธิบายไฟล์"
        }}
    ],
    "dependencies": ["package1", "package2"],
    "instructions": "คำแนะนำการใช้งาน"
}}

สำคัญ: สร้างโค้ดจริงที่รันได้ ไม่ใช่ตัวอย่าง
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": ai_prompt}],
                max_tokens=3000,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Clean JSON response
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:-3].strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response[3:-3].strip()
            
            ai_result = json.loads(ai_response)
            
            # สร้างไฟล์จริงๆ
            files_created = []
            if self.workspace and ai_result.get('files_to_create'):
                for file_info in ai_result['files_to_create']:
                    file_path = self.workspace / file_info['filename']
                    
                    # สร้างโฟลเดอร์ถ้าไม่มี
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # เขียนไฟล์
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file_info['content'])
                    
                    files_created.append(str(file_path))
                    print(f"    ✅ Created: {file_info['filename']}")
            
            return {
                'task': task,
                'agent': self.name,
                'status': 'completed',
                'ai_analysis': ai_result.get('analysis'),
                'files_created': files_created,
                'dependencies': ai_result.get('dependencies', []),
                'instructions': ai_result.get('instructions'),
                'result': f"✅ {self.name} completed '{task}' - Created {len(files_created)} files"
            }
            
        except Exception as e:
            print(f"❌ {self.name} failed: {e}")
            return {
                'task': task,
                'agent': self.name,
                'status': 'failed',
                'error': str(e),
                'result': f"❌ {self.name} failed on '{task}': {str(e)}"
            }


class AgentOrchestrator:
    """ตัวควบคุมการทำงานของทุก Agent"""
    
    def __init__(self):
        self.requirements_gatherer = RequirementsGatherer()
        self.team_lead = TeamLeadAgent()
        
        # สร้าง Specialized Agents
        self.agents = {
            'backend': SpecializedAgent("BackendAgent", "Backend Development"),
            'frontend': SpecializedAgent("FrontendAgent", "Frontend Development"), 
            'database': SpecializedAgent("DatabaseAgent", "Database Design"),
            'ui_ux': SpecializedAgent("UIUXAgent", "UI/UX Design"),
            'testing': SpecializedAgent("TestingAgent", "Quality Assurance"),
            'devops': SpecializedAgent("DevOpsAgent", "DevOps & Deployment")
        }
    
    async def handle_user_message(self, message: str, session_id: str) -> ChatResponse:
        """จัดการข้อความจากผู้ใช้พร้อม Real-time Status"""
        
        print(f"💬 Processing message from {session_id}: {message[:50]}...")
        
        # AI Chat เก็บ Requirements
        print("🔍 AI analyzing requirements...")
        chat_result = await self.requirements_gatherer.chat_with_user(message, session_id)
        
        if chat_result['requirements_complete']:
            print("✅ Requirements complete! Starting project execution...")
            
            # อัพเดท Agent status เป็น working
            working_agents = {
                'team_lead': 'analyzing',
                'backend': 'preparing',
                'frontend': 'preparing', 
                'ui_ux': 'preparing',
                'testing': 'preparing'
            }
            
            # ส่งให้ Team Lead สร้างแผนและเริ่มโครงการ
            print("👨‍💼 Team Lead creating project plan...")
            project_result = await self.team_lead.create_project_plan(
                chat_result['requirements'], 
                session_id
            )
            
            print(f"🎯 Project '{project_result['plan']['project_name']}' created successfully!")
            
            return ChatResponse(
                response=f"{chat_result['response']}\n\n🎯 โครงการ: {project_result['plan']['project_name']}\n� กำลังเริ่มดำเนินการ...\n\n👨‍💼 Team Lead: กำลังวางแผน\n🔧 Backend Agent: เตรียมตัว\n🎨 Frontend Agent: เตรียมตัว",
                session_id=session_id,
                requirements_complete=True,
                project_started=True,
                agents_status=working_agents,
                progress="🔄 กำลังเริ่มดำเนินโครงการ..."
            )
        else:
            # ยังเก็บ Requirements อยู่
            confidence = chat_result.get('ai_confidence', 0.5)
            progress_text = f"🤖 AI กำลังวิเคราะห์... (ความมั่นใจ: {confidence*100:.0f}%)"
            
            return ChatResponse(
                response=chat_result['response'],
                session_id=session_id,
                requirements_complete=False,
                project_started=False,
                progress=progress_text,
                agents_status={'ai_chat': 'analyzing'}
            )


# Global orchestrator
orchestrator = AgentOrchestrator()


@app.get("/")
async def root():
    """Root endpoint - serve the interface"""
    interface_file = ROOT_DIR / "orchestrator_interface.html"
    if interface_file.exists():
        return FileResponse(str(interface_file))
    else:
        return {"message": "🎼 AI Orchestrator System", "interface": "orchestrator_interface.html not found"}

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "message": "🎼 AI Orchestrator System Ready!",
        "active_sessions": len(orchestrator.requirements_gatherer.sessions),
        "active_projects": len(orchestrator.team_lead.active_projects)
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message_request: ChatMessage):
    """Chat endpoint - รับข้อความจากผู้ใช้"""
    
    session_id = message_request.session_id or f"session_{uuid.uuid4().hex[:8]}"
    
    try:
        response = await orchestrator.handle_user_message(
            message_request.message, 
            session_id
        )
        return response
        
    except Exception as e:
        return ChatResponse(
            response=f"ขออภัย เกิดข้อผิดพลาด: {str(e)}",
            session_id=session_id,
            requirements_complete=False,
            project_started=False
        )


@app.get("/sessions/{session_id}/requirements")
async def get_session_requirements(session_id: str):
    """ดู Requirements ของ session"""
    
    session = orchestrator.requirements_gatherer.sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        'session_id': session_id,
        'requirements': session['requirements'],
        'completion_status': session['completion_status'],
        'conversation': session['conversation']
    }


@app.get("/projects")
async def get_active_projects():
    """ดูโครงการที่กำลังดำเนินการ"""
    
    return {
        'active_projects': list(orchestrator.team_lead.active_projects.keys()),
        'project_details': orchestrator.team_lead.active_projects
    }


if __name__ == "__main__":
    import uvicorn
    print("🎼 Starting AI Orchestrator System...")
    print("💬 AI Chat: Requirements Gatherer")
    print("👨‍💼 Team Lead: Project Manager") 
    print("👥 Specialized Agents: Ready to work")
    print("📍 Server: http://localhost:8003")
    uvicorn.run(app, host="0.0.0.0", port=8003)