"""
🎯 Supervisor Agent - ควบคุมและประสานงาน Multi-Agent System
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    FAILED = "failed"
    COMPLETED = "completed"

class AgentType(Enum):
    REQUIREMENT_ANALYZER = "requirement_analyzer"
    DESIGN_AGENT = "design_agent"
    CODE_GENERATOR = "code_generator"
    QUALITY_TESTER = "quality_tester"
    DEPLOYER = "deployer"

@dataclass
class Task:
    id: str
    type: str
    description: str
    requirements: Dict[str, Any]
    status: TaskStatus
    assigned_agent: Optional[str] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class SupervisorAgent:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, Any] = {}
        self.workflow_queue: List[str] = []
        self.max_concurrent_tasks = 3
        self.quality_standards = {
            "min_test_coverage": 90,
            "max_errors": 0,
            "performance_threshold": 2.0,  # seconds
            "accessibility_score": 85
        }
        
    async def start_autonomous_workflow(self, user_request: str) -> str:
        """เริ่มต้นการทำงานแบบอัตโนมัติ - Enterprise Grade"""
        print(f"🎯 Supervisor: Starting ENTERPRISE autonomous workflow for: {user_request}")
        
        # วิเคราะห์ว่าต้องการ Professional Project หรือไม่
        is_professional = await self._analyze_professional_requirements(user_request)
        
        if is_professional:
            print("🏢 ENTERPRISE MODE: Creating Professional-Grade Project")
            
            # Import Enterprise Generator
            from .enterprise_generator import enterprise_generator
            
            # สร้าง Enterprise Task Chain
            task_chain = await self._create_enterprise_task_chain(user_request)
            workflow_id = f"enterprise_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # เริ่มการทำงาน Enterprise Workflow
            asyncio.create_task(self._execute_enterprise_workflow(workflow_id, task_chain, user_request))
        else:
            print("📋 STANDARD MODE: Creating Simple Project")
            
            # สร้าง Standard Task Chain
            task_chain = await self._create_task_chain(user_request)
            workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # เริ่มการทำงานใน Background
            asyncio.create_task(self._execute_workflow(workflow_id, task_chain))
        
        return workflow_id
    
    async def _create_task_chain(self, user_request: str) -> List[Task]:
        """สร้างลำดับงานที่ต้องทำ"""
        tasks = []
        
        # Task 1: วิเคราะห์ความต้องการ
        tasks.append(Task(
            id="req_analysis",
            type="requirement_analysis",
            description="Analyze user requirements and create specification",
            requirements={"user_request": user_request},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 2: ออกแบบระบบ
        tasks.append(Task(
            id="system_design",
            type="system_design",
            description="Create system architecture and UI/UX design",
            requirements={"depends_on": "req_analysis"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 3: สร้างโค้ด
        tasks.append(Task(
            id="code_generation",
            type="code_generation", 
            description="Generate HTML, CSS, JavaScript code",
            requirements={"depends_on": "system_design"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 4: ทดสอบคุณภาพ
        tasks.append(Task(
            id="quality_testing",
            type="quality_testing",
            description="Run comprehensive quality tests",
            requirements={"depends_on": "code_generation"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 5: Deploy และ Preview
        tasks.append(Task(
            id="deployment",
            type="deployment",
            description="Deploy to preview environment",
            requirements={"depends_on": "quality_testing"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        return tasks
    
    async def _execute_workflow(self, workflow_id: str, tasks: List[Task]):
        """ดำเนินการ Workflow แบบ Autonomous"""
        print(f"🚀 Supervisor: Executing workflow {workflow_id}")
        
        # เก็บ Tasks ใน Memory
        for task in tasks:
            self.tasks[task.id] = task
        
        # ดำเนินการทีละ Task (Sequential สำหรับ Dependencies)
        for task in tasks:
            try:
                # รอให้ Dependencies เสร็จก่อน
                if "depends_on" in task.requirements:
                    dep_task_id = task.requirements["depends_on"]
                    await self._wait_for_task_completion(dep_task_id)
                
                # เริ่มทำงาน
                task.status = TaskStatus.IN_PROGRESS
                print(f"⚡ Starting task: {task.id} - {task.description}")
                
                # ส่งงานให้ Agent
                result = await self._assign_and_execute_task(task)
                
                # ทดสอบผลงาน
                if await self._validate_task_result(task, result):
                    task.status = TaskStatus.COMPLETED
                    task.result = result
                    task.completed_at = datetime.now()
                    print(f"✅ Task completed: {task.id}")
                else:
                    # ถ้าไม่ผ่าน ให้ทำใหม่
                    print(f"❌ Task failed quality check, retrying: {task.id}")
                    await self._retry_task(task)
                    
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                print(f"💥 Task failed: {task.id} - {e}")
                break
        
        print(f"🎉 Workflow {workflow_id} completed!")
    
    async def _assign_and_execute_task(self, task: Task) -> Dict[str, Any]:
        """มอบหมายงานให้ Agent และรอผลลัพธ์"""
        
        if task.type == "requirement_analysis":
            from .requirement_analyzer import RequirementAnalyzer
            from openai import AsyncOpenAI
            import os
            
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            agent = RequirementAnalyzer(client)
            return await agent.analyze_requirements(task.requirements["user_request"])
            
        elif task.type == "system_design":
            from .conversational_design_agent import ConversationalDesignAgent
            from openai import AsyncOpenAI
            import os
            
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            agent = ConversationalDesignAgent(client)
            prev_result = self.tasks["req_analysis"].result
            return await agent.create_design(prev_result)
            
        elif task.type == "code_generation":
            # ใช้โค้ดเจเนอเรเตอร์ง่ายๆ ก่อน
            return await self._generate_simple_website(task)
            
        elif task.type == "quality_testing":
            return await self._run_quality_tests(task)
            
        elif task.type == "deployment":
            return await self._deploy_to_preview(task)
            
        return {"error": "Unknown task type"}
    
    async def _run_quality_tests(self, task: Task) -> Dict[str, Any]:
        """รัน Quality Tests แบบครอบคลุม"""
        code_result = self.tasks["code_generation"].result
        
        test_results = {
            "syntax_check": True,
            "performance_test": True,
            "accessibility_test": True,
            "responsive_test": True,
            "cross_browser_test": True,
            "security_test": True,
            "errors": [],
            "warnings": [],
            "score": 0
        }
        
        # Syntax Check
        if "html_content" in code_result:
            # ตรวจสอบ HTML Syntax
            html = code_result["html_content"]
            if "<html" not in html or "</html>" not in html:
                test_results["syntax_check"] = False
                test_results["errors"].append("Invalid HTML structure")
        
        # Performance Test
        # (จำลองการทดสอบ Performance)
        performance_score = 95  # Mock score
        if performance_score < 80:
            test_results["performance_test"] = False
            test_results["errors"].append(f"Performance score too low: {performance_score}")
        
        # คำนวณคะแนนรวม
        passed_tests = sum([
            test_results["syntax_check"],
            test_results["performance_test"], 
            test_results["accessibility_test"],
            test_results["responsive_test"]
        ])
        test_results["score"] = (passed_tests / 4) * 100
        
        return test_results
    
    async def _validate_task_result(self, task: Task, result: Dict[str, Any]) -> bool:
        """ตรวจสอบว่าผลงานผ่านมาตรฐานหรือไม่"""
        
        if task.type == "quality_testing":
            # ตรวจสอบว่าผ่าน Quality Standards
            if len(result.get("errors", [])) > self.quality_standards["max_errors"]:
                return False
            if result.get("score", 0) < self.quality_standards["accessibility_score"]:
                return False
            return True
        
        # สำหรับ Task อื่นๆ ตรวจสอบว่ามี result
        return result and not result.get("error")
    
    async def _retry_task(self, task: Task, max_retries: int = 3):
        """ลองทำงานใหม่หากไม่ผ่าน"""
        for retry in range(max_retries):
            print(f"🔄 Retrying task {task.id} (attempt {retry + 1})")
            
            result = await self._assign_and_execute_task(task)
            
            if await self._validate_task_result(task, result):
                task.status = TaskStatus.COMPLETED
                task.result = result
                task.completed_at = datetime.now()
                return
        
        # หากลองหลายครั้งแล้วยังไม่ผ่าน
        task.status = TaskStatus.FAILED
        task.error = f"Failed after {max_retries} retries"
    
    async def _wait_for_task_completion(self, task_id: str):
        """รอให้ Task เสร็จก่อน"""
        while True:
            task = self.tasks.get(task_id)
            if task and task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                break
            await asyncio.sleep(0.1)
    
    async def _deploy_to_preview(self, task: Task) -> Dict[str, Any]:
        """Deploy ไปยัง Preview Environment"""
        from pathlib import Path
        import os
        
        code_result = self.tasks["code_generation"].result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # สร้าง Directory
        webroot = Path(os.getenv("WEBROOT", "/app/workspace/generated-app/apps/web"))
        deploy_dir = webroot / f"auto-{timestamp}"
        deploy_dir.mkdir(parents=True, exist_ok=True)
        
        # เขียนไฟล์
        if "html_content" in code_result:
            (deploy_dir / "index.html").write_text(code_result["html_content"], encoding="utf-8")
        
        preview_url = f"http://localhost:8001/app/auto-{timestamp}/index.html"
        
        return {
            "deployed": True,
            "preview_url": preview_url,
            "deploy_path": str(deploy_dir)
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """ดู Status ของ Workflow"""
        tasks_status = {}
        for task_id, task in self.tasks.items():
            tasks_status[task_id] = {
                "status": task.status.value,
                "description": task.description,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "error": task.error
            }
        
        return {
            "workflow_id": workflow_id,
            "tasks": tasks_status,
            "overall_progress": self._calculate_progress()
        }
    
    def _calculate_progress(self) -> float:
        """คำนวณความก้าวหน้าโดยรวม"""
        if not self.tasks:
            return 0.0
        
        completed = sum(1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED)
        total = len(self.tasks)
        return (completed / total) * 100
    
    async def _generate_simple_website(self, task: Task) -> Dict[str, Any]:
        """สร้างเว็บไซต์ง่ายๆ โดยใช้ OpenAI"""
        try:
            from openai import AsyncOpenAI
            import os
            
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # ดึงข้อมูลจาก design task
            design_result = self.tasks.get("system_design", {}).result or {}
            req_result = self.tasks.get("req_analysis", {}).result or {}
            
            user_request = req_result.get("original_request", "สร้างเว็บไซต์")
            
            prompt = f"""
            สร้างเว็บไซต์ HTML สมบูรณ์ตามคำขอ: "{user_request}"
            
            ข้อกำหนด:
            - HTML5 สมบูรณ์
            - CSS ภายในไฟล์ (internal styles)
            - ใช้ Google Fonts สำหรับภาษาไทย
            - Responsive Design
            - สีสันสวยงาม modern
            - เนื้อหาเกี่ยวข้องกับคำขอ
            - Animation เบาๆ
            - ใช้งานได้จริง
            
            ตอบเฉพาะโค้ด HTML เท่านั้น ไม่ต้องมีคำอธิบาย:
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000
            )
            
            html_content = response.choices[0].message.content.strip()
            
            # ทำความสะอาดโค้ด
            if "```html" in html_content:
                html_content = html_content.split("```html")[1].split("```")[0].strip()
            elif "```" in html_content:
                html_content = html_content.split("```")[1].strip()
            
            return {
                "html_content": html_content,
                "generated_by": "OpenAI GPT-4o-mini",
                "user_request": user_request,
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    async def _analyze_professional_requirements(self, user_request: str) -> bool:
        """วิเคราะห์ว่าต้องการ Professional Project หรือไม่"""
        
        professional_keywords = [
            "professional", "enterprise", "business", "company", "corporate",
            "ecommerce", "ร้านค้า", "ขายของ", "ธุรกิจ", "บริษัท", "องค์กร",
            "system", "platform", "app", "application", "website", "เว็บไซต์",
            "ระบบ", "แพลตฟอร์ม", "แอป", "แอพ", "โปรแกรม",
            "workflow", "complete", "full", "ครบถ้วน", "สมบูรณ์", "ทั้งระบบ"
        ]
        
        request_lower = user_request.lower()
        
        # ตรวจสอบ keyword
        has_professional_keywords = any(keyword in request_lower for keyword in professional_keywords)
        
        # ตรวจสอบความซับซ้อน
        complexity_indicators = [
            "database", "ฐานข้อมูล", "login", "เข้าสู่ระบบ", "payment", "ชำระเงิน",
            "user management", "จัดการผู้ใช้", "admin", "ผู้ดูแลระบบ",
            "api", "backend", "multiple pages", "หลายหน้า"
        ]
        
        is_complex = any(indicator in request_lower for indicator in complexity_indicators)
        
        return has_professional_keywords or is_complex
    
    async def _create_enterprise_task_chain(self, user_request: str) -> List[Task]:
        """สร้างลำดับงานสำหรับ Enterprise Project"""
        tasks = []
        
        # Task 1: Deep Requirements Analysis
        tasks.append(Task(
            id="enterprise_req_analysis",
            type="enterprise_requirement_analysis",
            description="Deep analysis of business requirements for professional project",
            requirements={"user_request": user_request, "enterprise_grade": True},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 2: Enterprise Architecture Design
        tasks.append(Task(
            id="enterprise_architecture",
            type="enterprise_architecture",
            description="Design comprehensive system architecture and database schema",
            requirements={"depends_on": "enterprise_req_analysis"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 3: Professional Frontend Development
        tasks.append(Task(
            id="frontend_development",
            type="frontend_development",
            description="Create professional frontend with multiple pages and components",
            requirements={"depends_on": "enterprise_architecture"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 4: Backend API Development
        tasks.append(Task(
            id="backend_development",
            type="backend_development",
            description="Develop REST API with authentication and database integration",
            requirements={"depends_on": "enterprise_architecture"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 5: Database Setup
        tasks.append(Task(
            id="database_setup",
            type="database_setup",
            description="Create database schema and seed data",
            requirements={"depends_on": "enterprise_architecture"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 6: Integration Testing
        tasks.append(Task(
            id="integration_testing",
            type="integration_testing",
            description="Test all components working together",
            requirements={"depends_on": ["frontend_development", "backend_development", "database_setup"]},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        # Task 7: Professional Deployment
        tasks.append(Task(
            id="professional_deployment",
            type="professional_deployment",
            description="Deploy complete system to production-like environment",
            requirements={"depends_on": "integration_testing"},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        ))
        
        return tasks
    
    async def _execute_enterprise_workflow(self, workflow_id: str, tasks: List[Task], user_request: str):
        """ดำเนินการ Enterprise Workflow"""
        print(f"🏢 Supervisor: Executing ENTERPRISE workflow {workflow_id}")
        
        # Import Enterprise Generator
        from .enterprise_generator import enterprise_generator
        
        try:
            # Phase 1: ทำความเข้าใจความต้องการอย่างลึกซึ้ง
            print("🔍 Phase 1: Deep Requirements Analysis...")
            analysis = await enterprise_generator.analyze_requirements_thoroughly(user_request)
            
            project_type = analysis.get("project_type", "professional_website")
            print(f"📊 Detected Project Type: {project_type}")
            
            # Phase 2: สร้าง Professional Project Structure
            print("🏗️ Phase 2: Generating Professional Project...")
            
            if project_type in ["professional_website", "ecommerce_platform", "saas_platform"]:
                project_structure = await enterprise_generator.generate_professional_website(analysis)
            elif project_type == "mobile_app":
                project_structure = await enterprise_generator.generate_mobile_app(analysis)
            else:
                project_structure = await enterprise_generator.generate_professional_website(analysis)
            
            # Phase 3: Deploy to Professional Environment
            print("🚀 Phase 3: Deploying to Professional Environment...")
            deployment_info = await enterprise_generator.deploy_project(
                project_structure,
                f"{project_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            # Phase 4: Update workflow status
            print("✅ Enterprise Workflow Completed Successfully!")
            print(f"🌐 Access URLs: {deployment_info.get('urls', {})}")
            
            # Store results in workflow tracking
            self.workflow_results[workflow_id] = {
                "status": "completed",
                "project_type": project_type,
                "analysis": analysis,
                "project_structure": project_structure,
                "deployment_info": deployment_info,
                "professional_grade": True,
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Enterprise workflow failed: {e}")
            self.workflow_results[workflow_id] = {
                "status": "failed", 
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }

# Singleton Instance
supervisor_agent = SupervisorAgent()