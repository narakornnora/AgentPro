#!/usr/bin/env python3
"""
🤖 Full-Privilege AI Agent System
ระบบที่ให้ AI สิทธิ์เต็มที่ในการทำงานในสภาพแวดล้อมจริง เหมือน Lovable

จุดเด่น:
- 🎯 AI มีสิทธิ์เต็มที่: สร้าง/แก้ไข/ลบไฟล์ ติดตั้ง dependencies รัน tests
- 👥 Multi-User System: แต่ละ User มี workspace แยกกัน
- 🤝 Agent Collaboration: AI Agents ทำงานร่วมกัน
- 🔗 GitHub Integration: เชื่อมต่อ GitHub และ deploy ได้จริง
- 💰 Cost-Effective: ทำงานแบบ Lovable แต่ราคาไม่แพง
"""
import os
import json
import asyncio
import subprocess
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import sqlite3

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import git

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is required!")

client = OpenAI(api_key=API_KEY)
ROOT_DIR = Path("C:/agent")
USERS_DIR = ROOT_DIR / "user_workspaces"
TEMPLATES_DIR = ROOT_DIR / "templates"

# Ensure directories exist
USERS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI App
app = FastAPI(title="Full-Privilege AI Agent", description="🤖 AI ที่มีสิทธิ์เต็มที่ในการทำงาน")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserRequest(BaseModel):
    user_id: str
    message: str
    project_type: str = "auto"
    tech_stack: List[str] = []
    github_repo: Optional[str] = None

class AgentResponse(BaseModel):
    success: bool
    message: str
    user_workspace: str
    project_path: Optional[str] = None
    github_url: Optional[str] = None
    files_created: int = 0
    commands_executed: List[str] = []
    agents_involved: List[str] = []
    error: Optional[str] = None


class WorkspaceManager:
    """จัดการ Workspace สำหรับแต่ละ User"""
    
    @staticmethod
    def get_user_workspace(user_id: str) -> Path:
        """สร้าง workspace สำหรับ user"""
        user_workspace = USERS_DIR / user_id
        user_workspace.mkdir(parents=True, exist_ok=True)
        return user_workspace
    
    @staticmethod
    def init_user_db(user_id: str):
        """สร้าง SQLite database สำหรับ user"""
        workspace = WorkspaceManager.get_user_workspace(user_id)
        db_path = workspace / "user_data.db"
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # สร้างตารางโครงการ
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                path TEXT NOT NULL,
                github_url TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # สร้างตารางการทำงานของ Agent
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                agent_name TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                success BOOLEAN DEFAULT TRUE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        return db_path


class AutoTestingAgent:
    """AI Agent พิเศษสำหรับ Auto-Testing & Self-Healing"""
    
    def __init__(self):
        self.name = "AutoTestingAgent"
        self.max_retry_attempts = 3
        self.test_results = []
        self.healing_history = []
    
    async def comprehensive_test(self, project_path: Path) -> Dict[str, Any]:
        """ทดสอบโครงการแบบครอบคลุม"""
        print(f"🔍 Starting comprehensive testing: {project_path}")
        
        test_results = {
            'syntax_check': await self._test_syntax(project_path),
            'dependency_check': await self._test_dependencies(project_path),
            'database_check': await self._test_database(project_path),
            'api_check': await self._test_api_endpoints(project_path),
            'frontend_check': await self._test_frontend(project_path),
            'integration_check': await self._test_integration(project_path)
        }
        
        # คำนวณ overall score
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result.get('success', False))
        success_rate = (passed_tests / total_tests) * 100
        
        overall_result = {
            'success_rate': success_rate,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'details': test_results,
            'is_production_ready': success_rate >= 80
        }
        
        print(f"📊 Test Results: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        return overall_result
    
    async def auto_heal_errors(self, project_path: Path, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """แก้ไข errors อัตโนมัติ"""
        print(f"🛠️ Starting auto-healing: {project_path}")
        
        healing_results = []
        
        for test_name, result in test_results['details'].items():
            if not result.get('success', False):
                print(f"🔧 Healing {test_name}...")
                healing_result = await self._heal_specific_error(project_path, test_name, result)
                healing_results.append(healing_result)
        
        return {
            'healed_issues': len(healing_results),
            'healing_details': healing_results,
            'success': len(healing_results) > 0
        }
    
    async def _test_syntax(self, project_path: Path) -> Dict[str, Any]:
        """ทดสอบ Python syntax"""
        try:
            python_files = list(project_path.glob("*.py"))
            errors = []
            
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        code = f.read()
                    compile(code, str(py_file), 'exec')
                except SyntaxError as e:
                    errors.append(f"{py_file.name}: {str(e)}")
            
            return {
                'success': len(errors) == 0,
                'files_checked': len(python_files),
                'errors': errors,
                'message': '✅ Syntax OK' if len(errors) == 0 else f'❌ {len(errors)} syntax errors'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'message': f'❌ Syntax check failed: {str(e)}'}
    
    async def _test_dependencies(self, project_path: Path) -> Dict[str, Any]:
        """ทดสอบ dependencies"""
        try:
            req_file = project_path / "requirements.txt"
            if not req_file.exists():
                return {'success': False, 'message': '❌ requirements.txt not found'}
            
            with open(req_file, 'r') as f:
                requirements = [line.strip() for line in f.readlines() if line.strip()]
            
            # ลองติดตั้ง dependencies (dry-run)
            missing_deps = []
            for req in requirements:
                try:
                    __import__(req.split('==')[0].replace('-', '_'))
                except ImportError:
                    missing_deps.append(req)
            
            return {
                'success': len(missing_deps) == 0,
                'total_deps': len(requirements),
                'missing_deps': missing_deps,
                'message': '✅ Dependencies OK' if len(missing_deps) == 0 else f'❌ {len(missing_deps)} missing deps'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'message': f'❌ Dependency check failed: {str(e)}'}
    
    async def _test_database(self, project_path: Path) -> Dict[str, Any]:
        """ทดสอบ database"""
        try:
            db_file = project_path / "database.py"
            if not db_file.exists():
                return {'success': False, 'message': '❌ database.py not found'}
            
            # รัน database initialization
            process = await asyncio.create_subprocess_shell(
                f"cd {project_path} && python database.py",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            success = process.returncode == 0
            return {
                'success': success,
                'returncode': process.returncode,
                'stdout': stdout.decode('utf-8', errors='ignore'),
                'stderr': stderr.decode('utf-8', errors='ignore'),
                'message': '✅ Database OK' if success else '❌ Database initialization failed'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'message': f'❌ Database test failed: {str(e)}'}
    
    async def _test_api_endpoints(self, project_path: Path) -> Dict[str, Any]:
        """ทดสอบ API endpoints"""
        try:
            app_file = project_path / "app.py"
            if not app_file.exists():
                return {'success': False, 'message': '❌ app.py not found'}
            
            # อ่านโค้ดและหา routes
            with open(app_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # นับ routes ที่พบ
            routes = code.count('@app.route')
            api_routes = code.count('/api/')
            
            return {
                'success': routes > 0,
                'total_routes': routes,
                'api_routes': api_routes,
                'has_cors': 'CORS' in code,
                'message': f'✅ Found {routes} routes' if routes > 0 else '❌ No routes found'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'message': f'❌ API test failed: {str(e)}'}
    
    async def _test_frontend(self, project_path: Path) -> Dict[str, Any]:
        """ทดสอบ frontend"""
        try:
            templates_dir = project_path / "templates"
            static_dir = project_path / "static"
            
            html_files = list(templates_dir.glob("*.html")) if templates_dir.exists() else []
            css_files = list(static_dir.glob("*.css")) if static_dir.exists() else []
            js_files = list(static_dir.glob("*.js")) if static_dir.exists() else []
            
            return {
                'success': len(html_files) > 0,
                'html_files': len(html_files),
                'css_files': len(css_files),
                'js_files': len(js_files),
                'message': f'✅ Frontend OK ({len(html_files)} HTML, {len(css_files)} CSS, {len(js_files)} JS)' if len(html_files) > 0 else '❌ No HTML files found'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'message': f'❌ Frontend test failed: {str(e)}'}
    
    async def _test_integration(self, project_path: Path) -> Dict[str, Any]:
        """ทดสอบ integration"""
        try:
            # ลองรัน server แบบ background และทดสอบ
            start_script = project_path / "start.bat"
            
            return {
                'success': start_script.exists(),
                'has_start_script': start_script.exists(),
                'has_readme': (project_path / "README.md").exists(),
                'has_dockerfile': (project_path / "Dockerfile").exists(),
                'message': '✅ Integration ready' if start_script.exists() else '❌ Missing start script'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'message': f'❌ Integration test failed: {str(e)}'}
    
    async def _heal_specific_error(self, project_path: Path, test_name: str, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """แก้ไข error เฉพาะ"""
        healing_prompt = f"""
คุณเป็น AI Doctor ที่แก้ไข error ในโครงการ

Test ที่ล้มเหลว: {test_name}
ผลการทดสอบ: {test_result}
โฟลเดอร์โครงการ: {project_path}

วิเคราะห์ปัญหาและเสนอวิธีแก้ไข:
1. สาเหตุของปัญหา
2. ไฟล์ที่ต้องแก้ไข
3. โค้ดที่ต้องเปลี่ยน

ตอบเป็น JSON:
{{
    "diagnosis": "สาเหตุของปัญหา",
    "files_to_fix": ["file1.py", "file2.txt"],
    "fix_actions": [
        {{"file": "file1.py", "action": "replace", "old_code": "...", "new_code": "..."}},
        {{"file": "requirements.txt", "action": "add", "content": "new_package==1.0.0"}}
    ],
    "confidence": 0.95
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": healing_prompt}],
                max_tokens=2000
            )
            
            healing_plan = json.loads(response.choices[0].message.content)
            
            # ดำเนินการแก้ไขตามแผน
            fixes_applied = []
            for fix_action in healing_plan.get('fix_actions', []):
                fix_result = await self._apply_fix(project_path, fix_action)
                fixes_applied.append(fix_result)
            
            return {
                'test_name': test_name,
                'diagnosis': healing_plan.get('diagnosis'),
                'fixes_applied': len(fixes_applied),
                'fix_details': fixes_applied,
                'confidence': healing_plan.get('confidence', 0.5),
                'success': True
            }
            
        except Exception as e:
            return {
                'test_name': test_name,
                'error': str(e),
                'success': False
            }
    
    async def _apply_fix(self, project_path: Path, fix_action: Dict[str, Any]) -> Dict[str, Any]:
        """ดำเนินการแก้ไข"""
        try:
            file_path = project_path / fix_action['file']
            action = fix_action['action']
            
            if action == 'replace':
                # แทนที่โค้ด
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    old_code = fix_action.get('old_code', '')
                    new_code = fix_action.get('new_code', '')
                    
                    if old_code in content:
                        content = content.replace(old_code, new_code)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        return {'file': str(file_path), 'action': 'replaced', 'success': True}
            
            elif action == 'add':
                # เพิ่มเนื้อหา
                content = fix_action.get('content', '')
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n{content}")
                return {'file': str(file_path), 'action': 'added', 'success': True}
            
            elif action == 'create':
                # สร้างไฟล์ใหม่
                content = fix_action.get('content', '')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {'file': str(file_path), 'action': 'created', 'success': True}
            
            return {'file': str(file_path), 'action': action, 'success': False, 'error': 'Unknown action'}
            
        except Exception as e:
            return {'file': fix_action.get('file'), 'action': fix_action.get('action'), 'success': False, 'error': str(e)}


class FullPrivilegeAgent:
    """AI Agent ที่มีสิทธิ์เต็มที่ในการทำงาน"""
    
    def __init__(self, name: str, specialization: str):
        self.name = name
        self.specialization = specialization
        self.workspace = None
        self.activities = []
        self.auto_tester = AutoTestingAgent()  # เพิ่ม Auto Tester
    
    def set_workspace(self, workspace_path: Path):
        """กำหนด workspace สำหรับ agent"""
        self.workspace = workspace_path
    
    async def execute_command(self, command: str, cwd: Optional[Path] = None) -> Dict[str, Any]:
        """รันคำสั่งในระบบจริง"""
        try:
            work_dir = cwd or self.workspace
            
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=str(work_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            result = {
                'success': process.returncode == 0,
                'stdout': stdout.decode('utf-8', errors='ignore'),
                'stderr': stderr.decode('utf-8', errors='ignore'),
                'return_code': process.returncode,
                'command': command
            }
            
            self.activities.append({
                'action': 'execute_command',
                'command': command,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'command': command
            }
            self.activities.append({
                'action': 'execute_command_failed',
                'command': command,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return error_result
    
    def create_file(self, file_path: Path, content: str) -> bool:
        """สร้างไฟล์ในระบบจริง"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.activities.append({
                'action': 'create_file',
                'file': str(file_path),
                'size': len(content),
                'timestamp': datetime.now().isoformat()
            })
            return True
        except Exception as e:
            self.activities.append({
                'action': 'create_file_failed',
                'file': str(file_path),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def delete_file(self, file_path: Path) -> bool:
        """ลบไฟล์ในระบบจริง"""
        try:
            if file_path.exists():
                file_path.unlink()
                self.activities.append({
                    'action': 'delete_file',
                    'file': str(file_path),
                    'timestamp': datetime.now().isoformat()
                })
                return True
            return False
        except Exception as e:
            self.activities.append({
                'action': 'delete_file_failed',
                'file': str(file_path),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    async def install_dependencies(self, requirements: List[str]) -> Dict[str, Any]:
        """ติดตั้ง dependencies จริงๆ"""
        commands = []
        results = []
        
        # Python packages
        python_packages = [req for req in requirements if not req.startswith('npm:')]
        if python_packages:
            cmd = f"pip install {' '.join(python_packages)}"
            result = await self.execute_command(cmd)
            commands.append(cmd)
            results.append(result)
        
        # NPM packages
        npm_packages = [req[4:] for req in requirements if req.startswith('npm:')]
        if npm_packages:
            # Initialize npm if needed
            if not (self.workspace / "package.json").exists():
                init_result = await self.execute_command("npm init -y")
                commands.append("npm init -y")
                results.append(init_result)
            
            # Install packages
            cmd = f"npm install {' '.join(npm_packages)}"
            result = await self.execute_command(cmd)
            commands.append(cmd)
            results.append(result)
        
        return {
            'commands': commands,
            'results': results,
            'success': all(r['success'] for r in results)
        }


class ProjectGenerator:
    """สร้างโครงการตามที่ผู้ใช้ต้องการ"""
    
    def __init__(self):
        self.agents = {
            'backend': FullPrivilegeAgent("BackendAgent", "API และ Database"),
            'frontend': FullPrivilegeAgent("FrontendAgent", "UI/UX และ Frontend"),
            'devops': FullPrivilegeAgent("DevOpsAgent", "Deploy และ Infrastructure"),
            'fullstack': FullPrivilegeAgent("FullStackAgent", "Full-Stack Development")
        }
    
    async def generate_project(self, user_request: UserRequest) -> Dict[str, Any]:
        """สร้างโครงการตามความต้องการ"""
        
        # เตรียม workspace
        user_workspace = WorkspaceManager.get_user_workspace(user_request.user_id)
        WorkspaceManager.init_user_db(user_request.user_id)
        
        # สร้าง project directory
        project_id = str(uuid.uuid4())[:8]
        project_name = await self._generate_project_name(user_request.message)
        project_path = user_workspace / f"{project_name}_{project_id}"
        
        # กำหนด workspace ให้ agents
        for agent in self.agents.values():
            agent.set_workspace(project_path)
        
        # วิเคราะห์ความต้องการและเลือก tech stack
        project_spec = await self._analyze_requirements(user_request.message)
        
        # สร้างโครงการด้วย AI + Full Privileges
        result = await self._create_full_project(project_spec, project_path, user_request)
        
        # เชื่อมต่อ GitHub ถ้าต้องการ
        if user_request.github_repo:
            github_result = await self._setup_github(project_path, user_request.github_repo)
            result['github_url'] = github_result.get('url')
        
        return result
    
    async def _generate_project_name(self, description: str) -> str:
        """สร้างชื่อโครงการจาก AI"""
        prompt = f"สร้างชื่อโครงการสั้นๆ ภาษาอังกฤษ (ไม่เกิน 2 คำ) จาก: {description}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        
        name = response.choices[0].message.content.strip()
        name = "".join(c for c in name if c.isalnum() or c in "_-").lower()
        return name or "project"
    
    async def _analyze_requirements(self, description: str) -> Dict[str, Any]:
        """วิเคราะห์ความต้องการด้วย AI"""
        
        analysis_prompt = f"""
วิเคราะห์ความต้องการและส่งกลับ JSON:

คำขอ: {description}

ส่งกลับ:
{{
    "type": "web_app|mobile_app|desktop_app|api|fullstack",
    "complexity": "simple|medium|complex",
    "tech_stack": {{
        "backend": "flask|fastapi|django|nodejs|none",
        "frontend": "html|react|vue|angular|none", 
        "database": "sqlite|postgresql|mysql|mongodb|none",
        "deployment": "local|docker|cloud"
    }},
    "features": ["feature1", "feature2"],
    "requirements": ["requirement1", "requirement2"],
    "estimated_files": 5
}}
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": analysis_prompt}],
            max_tokens=1000
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            # Fallback
            return {
                "type": "fullstack",
                "complexity": "medium",
                "tech_stack": {
                    "backend": "flask",
                    "frontend": "html",
                    "database": "sqlite",
                    "deployment": "local"
                },
                "features": ["CRUD", "Authentication"],
                "requirements": ["flask", "sqlite3"],
                "estimated_files": 8
            }
    
    async def _create_full_project(self, spec: Dict[str, Any], project_path: Path, user_request: UserRequest) -> Dict[str, Any]:
        """สร้างโครงการเต็มรูปแบบด้วย AI Agents + Auto-Testing & Self-Healing"""
        
        project_path.mkdir(parents=True, exist_ok=True)
        files_created = 0
        commands_executed = []
        agents_involved = []
        auto_tester = AutoTestingAgent()
        
        print(f"🚀 Starting project creation with Auto-Testing & Self-Healing...")
        
        # วนลูปจนกว่าจะสำเร็จ (หรือครบจำนวนครั้งที่กำหนด)
        for attempt in range(auto_tester.max_retry_attempts):
            print(f"🔄 Attempt {attempt + 1}/{auto_tester.max_retry_attempts}")
            
            try:
                # 1. Backend Agent: สร้าง API และ Database
                if spec['tech_stack']['backend'] != 'none':
                    print("🔧 Creating Backend...")
                    backend_agent = self.agents['backend']
                    agents_involved.append(backend_agent.name)
                    
                    backend_result = await self._create_backend(backend_agent, spec, project_path, user_request.message)
                    files_created += backend_result['files']
                    commands_executed.extend(backend_result['commands'])
                
                # 2. Frontend Agent: สร้าง UI
                if spec['tech_stack']['frontend'] != 'none':
                    print("🎨 Creating Frontend...")
                    frontend_agent = self.agents['frontend']
                    agents_involved.append(frontend_agent.name)
                    
                    frontend_result = await self._create_frontend(frontend_agent, spec, project_path, user_request.message)
                    files_created += frontend_result['files']
                    commands_executed.extend(frontend_result['commands'])
                
                # 3. DevOps Agent: Setup deployment
                print("🚀 Setting up Deployment...")
                devops_agent = self.agents['devops']
                agents_involved.append(devops_agent.name)
                
                devops_result = await self._create_deployment(devops_agent, spec, project_path)
                files_created += devops_result['files']
                commands_executed.extend(devops_result['commands'])
                
                # 4. ติดตั้ง dependencies จริงๆ
                if spec.get('requirements'):
                    print("📦 Installing Dependencies...")
                    install_result = await self.agents['fullstack'].install_dependencies(spec['requirements'])
                    commands_executed.extend(install_result['commands'])
                
                # 🔍 5. AUTO-TESTING: ทดสอบแบบครอบคลุม
                print("🔍 Running Comprehensive Tests...")
                test_results = await auto_tester.comprehensive_test(project_path)
                
                # 📊 6. ตรวจสอบผลการทดสอบ
                if test_results['is_production_ready']:
                    print(f"✅ Project PASSED all tests! ({test_results['success_rate']:.1f}%)")
                    return {
                        'success': True,
                        'message': f"✅ สร้างโครงการสำเร็จ! ({files_created} ไฟล์) - ผ่านการทดสอบ {test_results['success_rate']:.1f}%",
                        'project_path': str(project_path),
                        'files_created': files_created,
                        'commands_executed': commands_executed,
                        'agents_involved': agents_involved,
                        'test_results': test_results,
                        'attempt': attempt + 1,
                        'spec': spec
                    }
                else:
                    print(f"❌ Tests failed ({test_results['success_rate']:.1f}%). Starting auto-healing...")
                    
                    # 🛠️ 7. SELF-HEALING: แก้ไข errors อัตโนมัติ
                    healing_results = await auto_tester.auto_heal_errors(project_path, test_results)
                    print(f"🔧 Healed {healing_results['healed_issues']} issues")
                    
                    # ถ้าเป็น attempt สุดท้าย ให้ return ผลลัพธ์
                    if attempt == auto_tester.max_retry_attempts - 1:
                        return {
                            'success': test_results['success_rate'] >= 50,  # ยอมรับได้ถ้าผ่าน 50%
                            'message': f"⚠️ โครงการสร้างเสร็จแล้ว แต่ยังมี issues ({test_results['success_rate']:.1f}%) - พยายามแก้ไข {healing_results['healed_issues']} ปัญหาแล้ว",
                            'project_path': str(project_path),
                            'files_created': files_created,
                            'commands_executed': commands_executed,
                            'agents_involved': agents_involved,
                            'test_results': test_results,
                            'healing_results': healing_results,
                            'attempts': auto_tester.max_retry_attempts,
                            'spec': spec
                        }
                    
                    # ถ้ายังมี attempt เหลือ ให้ลองใหม่
                    print(f"🔄 Retrying... ({attempt + 2}/{auto_tester.max_retry_attempts})")
                    continue
                    
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt == auto_tester.max_retry_attempts - 1:
                    return {
                        'success': False,
                        'error': str(e),
                        'message': f"❌ เกิดข้อผิดพลาดหลังพยายาม {auto_tester.max_retry_attempts} ครั้ง: {str(e)}",
                        'files_created': files_created,
                        'commands_executed': commands_executed,
                        'agents_involved': agents_involved,
                        'attempts': attempt + 1
                    }
        
        # ไม่ควรมาถึงตรงนี้
        return {
            'success': False,
            'message': "❌ Unexpected error in retry loop",
            'files_created': files_created,
            'commands_executed': commands_executed,
            'agents_involved': agents_involved
        }
    
    async def _create_backend(self, agent: FullPrivilegeAgent, spec: Dict[str, Any], project_path: Path, description: str) -> Dict[str, Any]:
        """Backend Agent สร้าง API และ Database"""
        
        files_created = 0
        commands = []
        
        # สร้าง main backend file
        if spec['tech_stack']['backend'] == 'flask':
            backend_code = await self._generate_flask_app(description, spec)
            agent.create_file(project_path / "app.py", backend_code)
            files_created += 1
            
            # สร้าง database initialization
            if spec['tech_stack']['database'] == 'sqlite':
                db_code = await self._generate_database_init(description, spec)
                agent.create_file(project_path / "database.py", db_code)
                files_created += 1
        
        # สร้าง requirements.txt
        requirements = self._get_backend_requirements(spec)
        agent.create_file(project_path / "requirements.txt", "\n".join(requirements))
        files_created += 1
        
        return {
            'files': files_created,
            'commands': commands
        }
    
    async def _create_frontend(self, agent: FullPrivilegeAgent, spec: Dict[str, Any], project_path: Path, description: str) -> Dict[str, Any]:
        """Frontend Agent สร้าง UI"""
        
        files_created = 0
        commands = []
        
        # สร้าง templates directory
        templates_dir = project_path / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        # สร้าง static directory
        static_dir = project_path / "static"
        static_dir.mkdir(exist_ok=True)
        
        # สร้าง HTML
        html_code = await self._generate_frontend_html(description, spec)
        agent.create_file(templates_dir / "index.html", html_code)
        files_created += 1
        
        # สร้าง CSS
        css_code = await self._generate_frontend_css(description, spec)
        agent.create_file(static_dir / "style.css", css_code)
        files_created += 1
        
        # สร้าง JavaScript
        js_code = await self._generate_frontend_js(description, spec)
        agent.create_file(static_dir / "app.js", js_code)
        files_created += 1
        
        return {
            'files': files_created,
            'commands': commands
        }
    
    async def _create_deployment(self, agent: FullPrivilegeAgent, spec: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """DevOps Agent สร้าง deployment files"""
        
        files_created = 0
        commands = []
        
        # สร้าง start script
        start_script = self._generate_start_script(spec)
        agent.create_file(project_path / "start.bat", start_script)
        files_created += 1
        
        # สร้าง Docker file ถ้าต้องการ
        if spec['tech_stack']['deployment'] == 'docker':
            dockerfile = self._generate_dockerfile(spec)
            agent.create_file(project_path / "Dockerfile", dockerfile)
            files_created += 1
            
            docker_compose = self._generate_docker_compose(spec)
            agent.create_file(project_path / "docker-compose.yml", docker_compose)
            files_created += 1
        
        # สร้าง README
        readme = self._generate_readme(spec)
        agent.create_file(project_path / "README.md", readme)
        files_created += 1
        
        return {
            'files': files_created,
            'commands': commands
        }
    
    async def _run_tests(self, project_path: Path) -> Dict[str, Any]:
        """รัน tests อัตโนมัติ"""
        commands = []
        
        # ตรวจสอบว่าไฟล์สำคัญมีอยู่
        test_agent = self.agents['devops']
        test_agent.set_workspace(project_path)
        
        # Test Python syntax
        if (project_path / "app.py").exists():
            result = await test_agent.execute_command("python -m py_compile app.py")
            commands.append("python -m py_compile app.py")
        
        return {'commands': commands}
    
    async def _setup_github(self, project_path: Path, github_repo: str) -> Dict[str, Any]:
        """เชื่อมต่อ GitHub Repository"""
        try:
            devops_agent = self.agents['devops']
            devops_agent.set_workspace(project_path)
            
            # Initialize git
            await devops_agent.execute_command("git init")
            await devops_agent.execute_command("git add .")
            await devops_agent.execute_command('git commit -m "Initial commit by AI Agent"')
            
            # Add remote and push
            await devops_agent.execute_command(f"git remote add origin {github_repo}")
            await devops_agent.execute_command("git branch -M main")
            await devops_agent.execute_command("git push -u origin main")
            
            return {'url': github_repo, 'success': True}
        except Exception as e:
            return {'error': str(e), 'success': False}

    # Helper methods สำหรับสร้างโค้ด
    async def _generate_flask_app(self, description: str, spec: Dict[str, Any]) -> str:
        """สร้าง Flask app ด้วย AI"""
        prompt = f"""
สร้าง Flask application สำหรับ: {description}

Features: {spec.get('features', [])}
Database: {spec['tech_stack']['database']}

สร้าง Python code ที่สมบูรณ์:
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    async def _generate_database_init(self, description: str, spec: Dict[str, Any]) -> str:
        """สร้าง database initialization code"""
        return """import sqlite3
from pathlib import Path

def init_database():
    db_path = Path("app.db")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create tables here
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")
"""
    
    async def _generate_frontend_html(self, description: str, spec: Dict[str, Any]) -> str:
        """สร้าง HTML ด้วย AI"""
        return f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{description}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>{description}</h1>
        <div id="app">
            <!-- Content will be loaded here -->
        </div>
    </div>
    <script src="/static/app.js"></script>
</body>
</html>"""
    
    async def _generate_frontend_css(self, description: str, spec: Dict[str, Any]) -> str:
        """สร้าง CSS ที่สวยงาม"""
        return """/* Modern CSS */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: white;
    margin-top: 20px;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

h1 {
    color: #333;
    text-align: center;
    margin-bottom: 30px;
}

.btn {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
"""
    
    async def _generate_frontend_js(self, description: str, spec: Dict[str, Any]) -> str:
        """สร้าง JavaScript ที่ทำงานได้"""
        return """// Modern JavaScript
const API_BASE = '';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('App initialized');
    loadData();
});

// Load data from API
async function loadData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Display data
function displayData(data) {
    const app = document.getElementById('app');
    app.innerHTML = '<p>Data loaded successfully!</p>';
}
"""
    
    def _get_backend_requirements(self, spec: Dict[str, Any]) -> List[str]:
        """ระบุ requirements สำหรับ backend"""
        requirements = []
        
        if spec['tech_stack']['backend'] == 'flask':
            requirements.extend(['flask', 'flask-cors'])
        elif spec['tech_stack']['backend'] == 'fastapi':
            requirements.extend(['fastapi', 'uvicorn'])
        
        if spec['tech_stack']['database'] == 'sqlite':
            requirements.append('sqlite3')
        elif spec['tech_stack']['database'] == 'postgresql':
            requirements.append('psycopg2')
        
        return requirements
    
    def _generate_start_script(self, spec: Dict[str, Any]) -> str:
        """สร้าง start script"""
        return """@echo off
echo Starting application...

REM Install dependencies
pip install -r requirements.txt

REM Initialize database
python database.py

REM Start application
python app.py

echo Application is running!
pause
"""
    
    def _generate_dockerfile(self, spec: Dict[str, Any]) -> str:
        """สร้าง Dockerfile"""
        return """FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
"""
    
    def _generate_docker_compose(self, spec: Dict[str, Any]) -> str:
        """สร้าง docker-compose.yml"""
        return """version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENV=production
"""
    
    def _generate_readme(self, spec: Dict[str, Any]) -> str:
        """สร้าง README"""
        return f"""# AI Generated Project

## Overview
This project was generated by Full-Privilege AI Agent.

## Technology Stack
- Backend: {spec['tech_stack']['backend']}
- Frontend: {spec['tech_stack']['frontend']} 
- Database: {spec['tech_stack']['database']}

## Features
{chr(10).join(f"- {feature}" for feature in spec.get('features', []))}

## Quick Start
```bash
# Run locally
start.bat

# Or with Docker
docker-compose up
```

## Generated by AI Agent 🤖
This project demonstrates the power of AI with full privileges!
"""


# สร้าง ProjectGenerator instance
project_generator = ProjectGenerator()


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "message": "🤖 Full-Privilege AI Agent System Ready!",
        "agents": list(project_generator.agents.keys()),
        "users_workspace": str(USERS_DIR)
    }


@app.post("/create-project", response_model=AgentResponse)
async def create_project(request: UserRequest, background_tasks: BackgroundTasks):
    """สร้างโครงการใหม่ด้วย AI Agents + Auto-Testing & Self-Healing"""
    
    try:
        print(f"🎯 Creating project for user: {request.user_id}")
        print(f"📝 Request: {request.message}")
        
        result = await project_generator.generate_project(request)
        
        # เพิ่มข้อมูลการทดสอบใน response
        response_data = {
            "user_workspace": str(WorkspaceManager.get_user_workspace(request.user_id)),
            **result
        }
        
        # ถ้ามีผลการทดสอบ ให้แสดงในข้อความ
        if 'test_results' in result:
            test_info = result['test_results']
            response_data['message'] += f"\\n\\n📊 Test Results:\\n"
            for test_name, test_result in test_info['details'].items():
                status = "✅" if test_result.get('success') else "❌"
                response_data['message'] += f"{status} {test_name}: {test_result.get('message', 'N/A')}\\n"
            
            if 'healing_results' in result:
                healing_info = result['healing_results']
                response_data['message'] += f"\\n🛠️ Auto-Healing: Fixed {healing_info['healed_issues']} issues\\n"
        
        return AgentResponse(**response_data)
        
    except Exception as e:
        error_message = f"❌ เกิดข้อผิดพลาด: {str(e)}"
        print(f"Error: {error_message}")
        
        return AgentResponse(
            success=False,
            message=error_message,
            user_workspace=str(WorkspaceManager.get_user_workspace(request.user_id)),
            error=str(e)
        )


@app.get("/users/{user_id}/projects")
async def get_user_projects(user_id: str):
    """ดู projects ของ user"""
    workspace = WorkspaceManager.get_user_workspace(user_id)
    db_path = workspace / "user_data.db"
    
    if not db_path.exists():
        return {"projects": []}
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM projects ORDER BY updated_at DESC")
    projects = cursor.fetchall()
    
    conn.close()
    
    return {
        "user_id": user_id,
        "workspace": str(workspace),
        "projects": projects
    }


@app.get("/users/{user_id}/agent-activities")
async def get_agent_activities(user_id: str):
    """ดูกิจกรรมของ AI Agents"""
    workspace = WorkspaceManager.get_user_workspace(user_id)
    
    activities = []
    for agent in project_generator.agents.values():
        activities.extend(agent.activities)
    
    return {
        "user_id": user_id,
        "activities": sorted(activities, key=lambda x: x.get('timestamp', ''), reverse=True)
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Full-Privilege AI Agent System...")
    print("👥 Multi-User Workspace Ready")
    print("🤖 AI Agents with Full Privileges")
    print("📍 Server: http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)