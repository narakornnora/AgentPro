"""
Simple Agent Manager Implementation
จัดการ agents และ workflow แบบ autonomous
"""

import asyncio
import json
import time
import uuid
from typing import Dict, List, Any, Optional, AsyncIterator
from dataclasses import dataclass
from pathlib import Path

from .base_agent import BaseAgent, AgentTask, AgentResult, TaskPriority, AgentStatus

@dataclass
class SimpleTask:
    id: str
    type: str
    input_data: Dict[str, Any]
    created_at: float
    status: str = "pending"

class SimpleAgentManager:
    """Simple implementation of agent manager for testing"""
    
    def __init__(self, webroot: Path, openai_client):
        self.webroot = webroot
        self.client = openai_client
        self.active_tasks: Dict[str, SimpleTask] = {}
        
    async def create_immediate_task(self, task_data: Dict[str, Any]) -> str:
        """Create and queue immediate task"""
        
        task_id = f"task_{int(time.time() * 1000)}"
        
        task = SimpleTask(
            id=task_id,
            type=task_data.get("type", "create_website"),
            input_data=task_data,
            created_at=time.time()
        )
        
        self.active_tasks[task_id] = task
        return task_id
    
    async def execute_with_streaming(self, task_id: str) -> AsyncIterator[Dict[str, Any]]:
        """Execute task with streaming updates"""
        
        if task_id not in self.active_tasks:
            yield {"status": "error", "message": "Task not found"}
            return
        
        task = self.active_tasks[task_id]
        
        try:
            # Simulate the website creation process
            yield {"status": "started", "agent": "RequirementsAnalyst", "message": "วิเคราะห์ความต้องการ...", "progress": 10}
            await asyncio.sleep(1)
            
            yield {"status": "progress", "agent": "UIDesigner", "message": "ออกแบบ UI/UX...", "progress": 30}
            await asyncio.sleep(1)
            
            yield {"status": "progress", "agent": "CodeGenerator", "message": "เขียนโค้ด HTML, CSS, JS...", "progress": 60}
            await asyncio.sleep(2)
            
            # Actually create the website using existing system
            result = await self._create_website_files(task.input_data)
            
            yield {
                "status": "completed", 
                "agent": "SystemManager", 
                "message": "สร้างเว็บไซต์เสร็จสิ้น",
                "progress": 100,
                "preview_url": result.get("web_url"),
                "files": result.get("files", [])
            }
            
            task.status = "completed"
            
        except Exception as e:
            yield {"status": "error", "message": f"Error: {str(e)}", "progress": 0}
            task.status = "failed"
    
    async def _create_website_files(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create website files using the existing AI system"""
        
        # Use the existing AI planning system
        user_message = task_data.get("requirements", "สร้างเว็บไซต์")
        
        # Call existing AI system
        plan = await self._ask_ai_to_plan_async(user_message)
        files = self._write_files(plan)
        slug = plan["slug"]
        web_url = f"/app/{slug}/index.html"
        
        return {
            "ok": True,
            "slug": slug, 
            "web_url": web_url,
            "files": [f"/app/{slug}/{Path(f).name}" for f in files]
        }
    
    async def _ask_ai_to_plan_async(self, user_msg: str) -> Dict[str, Any]:
        """Async version of AI planning"""
        
        SYSTEM = """
        คุณคือ Codegen Orchestrator. หน้าที่คุณคือ สร้าง "ชุดไฟล์เว็บ" ตาม requirement สั้น ๆ เป็นภาษาไทย/อังกฤษ
        **ตอบกลับเป็น JSON เท่านั้น** และต้องตรงสคีมนี้เป๊ะ:
        {
          "slug": "myapp-YYYYMMDD-HHMMSS",
          "files": [
            {"path":"index.html","content":"<!doctype html>..."},
            {"path":"styles.css","content":"..."},
            {"path":"script.js","content":"..."},
            {"path":"menu.html","content":"..."},
            {"path":"contact.html","content":"..."}
          ]
        }

        ข้อกำหนด:
        - "files" ต้องมีอย่างน้อย: index.html, styles.css
        - HTML ทุกไฟล์ต้องอ้างอิงกันแบบ relative (เช่น <link rel="stylesheet" href="./styles.css">)
        - ใส่ <meta charset="utf-8"> และ <meta name="viewport" ...> ครบ
        - หากผู้ใช้ระบุประเภท (เช่น ร้านอาหาร, คาเฟ่, POS, Blog, Shop) ให้โครงสร้างเนื้อหาสอดคล้อง
        - ห้ามอธิบาย, ห้ามใส่ข้อความนอก JSON, ห้าม markdown, ห้าม code fence
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                temperature=0.3,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user_msg}
                ],
                timeout=30
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            # Validate and fix data
            slug = data.get("slug", "").strip()
            if not slug or not slug.startswith("myapp-"):
                from datetime import datetime
                slug = "myapp-" + datetime.now().strftime("%Y%m%d-%H%M%S")
                data["slug"] = slug
            
            # Ensure required files exist
            files = data.get("files", [])
            paths = {f.get("path", "").lower() for f in files if isinstance(f, dict)}
            
            if "index.html" not in paths:
                files.append({
                    "path": "index.html",
                    "content": "<!DOCTYPE html><html><head><meta charset='utf-8'><title>My Website</title></head><body><h1>Welcome</h1></body></html>"
                })
            
            if "styles.css" not in paths:
                files.append({
                    "path": "styles.css", 
                    "content": "body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }"
                })
            
            data["files"] = files
            return data
            
        except Exception as e:
            print(f"AI planning error: {e}")
            # Fallback response
            from datetime import datetime
            return {
                "slug": "myapp-" + datetime.now().strftime("%Y%m%d-%H%M%S"),
                "files": [
                    {
                        "path": "index.html",
                        "content": """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
    <link rel="stylesheet" href="./styles.css">
</head>
<body>
    <header>
        <h1>ยินดีต้อนรับ</h1>
    </header>
    <main>
        <p>เว็บไซต์ของคุณถูกสร้างแล้ว</p>
    </main>
    <script src="./script.js"></script>
</body>
</html>"""
                    },
                    {
                        "path": "styles.css",
                        "content": """
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    line-height: 1.6;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 1rem;
    text-align: center;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

h1 {
    margin: 0;
    font-size: 2.5rem;
}

@media (max-width: 768px) {
    h1 {
        font-size: 2rem;
    }
}
"""
                    },
                    {
                        "path": "script.js",
                        "content": """
// Interactive functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Website loaded successfully!');
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
"""
                    }
                ]
            }
    
    def _write_files(self, plan: Dict[str, Any]) -> List[str]:
        """Write files to filesystem"""
        
        slug = plan["slug"]
        outdir = self.webroot / slug
        outdir.mkdir(parents=True, exist_ok=True)
        
        written: List[str] = []
        
        for f in plan["files"]:
            if not isinstance(f, dict):
                continue
                
            rel_path = f.get("path", "").lstrip("/").strip()
            content = f.get("content", "")
            
            if not rel_path:
                continue
                
            file_path = outdir / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                file_path.write_text(content, encoding="utf-8")
                written.append(str(file_path))
            except Exception as e:
                print(f"Error writing file {file_path}: {e}")
        
        return written
    
    async def modify_project(self, project_id: str, modification_request: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Modify existing project"""
        
        # This would implement project modification logic
        # For now, return a simple response
        
        return {
            "success": True,
            "preview_url": f"/app/{project_id}/index.html",
            "changes": [f"Applied modification: {modification_request}"],
            "message": "Project modified successfully"
        }