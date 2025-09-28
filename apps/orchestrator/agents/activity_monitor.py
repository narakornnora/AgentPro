"""
🎬 Real-time Activity Monitor
แสดงกิจกรรม AI ขณะทำงาน - เปิดไฟล์, แก้ไข, สถานะต่าง ๆ
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import asyncio
from fastapi import WebSocket
import threading

class ActivityMonitor:
    def __init__(self):
        self.activities: List[Dict] = []
        self.active_connections: List[WebSocket] = []
        self.current_task = None
        self.task_progress = 0
        self.lock = threading.Lock()
        
    def add_activity(self, 
                    activity_type: str, 
                    description: str, 
                    details: Optional[Dict] = None,
                    status: str = "info"):
        """เพิ่มกิจกรรมใหม่"""
        activity = {
            "id": len(self.activities) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "description": description,
            "details": details or {},
            "status": status  # info, success, warning, error, working
        }
        
        with self.lock:
            self.activities.append(activity)
            # เก็บแค่ 100 activities ล่าสุด
            if len(self.activities) > 100:
                self.activities.pop(0)
        
        # ส่งข้อมูล real-time ไปยัง clients
        asyncio.create_task(self.broadcast_activity(activity))
        
    async def broadcast_activity(self, activity: Dict):
        """ส่งกิจกรรมไปยัง WebSocket clients"""
        if not self.active_connections:
            return
            
        message = json.dumps({
            "type": "activity_update",
            "data": activity
        })
        
        # ส่งไปยัง clients ทั้งหมด
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        # เอา connections ที่หลุดออก
        for conn in disconnected:
            self.active_connections.remove(conn)
    
    async def connect_websocket(self, websocket: WebSocket):
        """เชื่อมต่อ WebSocket client ใหม่"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # ส่งกิจกรรมล่าสุด 10 รายการ
        recent_activities = self.activities[-10:] if self.activities else []
        await websocket.send_text(json.dumps({
            "type": "initial_activities",
            "data": recent_activities
        }))
        
    def disconnect_websocket(self, websocket: WebSocket):
        """ยกเลิกการเชื่อมต่อ WebSocket"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    def start_task(self, task_name: str, total_steps: int = 100):
        """เริ่มงานใหม่"""
        self.current_task = {
            "name": task_name,
            "total_steps": total_steps,
            "current_step": 0,
            "start_time": datetime.now()
        }
        self.add_activity("task_start", f"🚀 เริ่มงาน: {task_name}", 
                         {"task": task_name, "total_steps": total_steps}, "working")
    
    def update_progress(self, step: int, description: str = ""):
        """อัพเดทความคืบหน้า"""
        if not self.current_task:
            return
            
        self.current_task["current_step"] = step
        progress_percent = (step / self.current_task["total_steps"]) * 100
        
        self.add_activity("progress_update", 
                         f"⚡ {description} ({step}/{self.current_task['total_steps']}) - {progress_percent:.1f}%",
                         {"progress": progress_percent, "step": step}, "working")
    
    def complete_task(self, result: str = "สำเร็จ"):
        """เสร็จสิ้นงาน"""
        if not self.current_task:
            return
            
        duration = datetime.now() - self.current_task["start_time"]
        self.add_activity("task_complete", 
                         f"✅ เสร็จสิ้น: {self.current_task['name']} - {result}",
                         {"duration": str(duration), "result": result}, "success")
        self.current_task = None
    
    def file_operation(self, operation: str, filepath: str, details: str = ""):
        """บันทึกการดำเนินการไฟล์"""
        icons = {
            "read": "📖",
            "write": "✏️", 
            "create": "📝",
            "delete": "🗑️",
            "copy": "📋",
            "move": "📦"
        }
        
        icon = icons.get(operation, "📁")
        self.add_activity("file_operation", 
                         f"{icon} {operation.upper()}: {Path(filepath).name}",
                         {"operation": operation, "filepath": filepath, "details": details})
    
    def agent_action(self, agent_name: str, action: str, details: Dict = None):
        """บันทึกการกระทำของ Agent"""
        self.add_activity("agent_action",
                         f"🤖 {agent_name}: {action}",
                         {"agent": agent_name, "action": action, **(details or {})})
    
    def code_generation(self, language: str, component: str, status: str = "generating"):
        """บันทึกการสร้างโค้ด"""
        icons = {
            "generating": "⚙️",
            "completed": "✅", 
            "error": "❌"
        }
        
        icon = icons.get(status, "⚙️")
        self.add_activity("code_generation",
                         f"{icon} สร้าง {component} ({language})",
                         {"language": language, "component": component, "status": status})
    
    def deployment_step(self, step: str, details: str = ""):
        """บันทึกขั้นตอน Deploy"""
        self.add_activity("deployment",
                         f"🚀 Deploy: {step}",
                         {"step": step, "details": details})
    
    def get_recent_activities(self, limit: int = 20) -> List[Dict]:
        """ดึงกิจกรรมล่าสุด"""
        with self.lock:
            return self.activities[-limit:] if self.activities else []
    
    def get_current_status(self) -> Dict:
        """ดึงสถานะปัจจุบัน"""
        return {
            "current_task": self.current_task,
            "total_activities": len(self.activities),
            "active_connections": len(self.active_connections),
            "last_activity": self.activities[-1] if self.activities else None
        }

# Global instance
activity_monitor = ActivityMonitor()

# Helper functions สำหรับใช้งานง่าย
def log_activity(activity_type: str, description: str, details: Dict = None, status: str = "info"):
    """เพิ่มกิจกรรม (shorthand)"""
    activity_monitor.add_activity(activity_type, description, details, status)

def log_file_read(filepath: str, details: str = ""):
    """บันทึกการอ่านไฟล์"""
    activity_monitor.file_operation("read", filepath, details)

def log_file_write(filepath: str, details: str = ""):
    """บันทึกการเขียนไฟล์"""
    activity_monitor.file_operation("write", filepath, details)

def log_file_create(filepath: str, details: str = ""):
    """บันทึกการสร้างไฟล์"""
    activity_monitor.file_operation("create", filepath, details)

def log_agent_action(agent_name: str, action: str, details: Dict = None):
    """บันทึกการกระทำของ Agent"""
    activity_monitor.agent_action(agent_name, action, details)

def log_code_gen(language: str, component: str, status: str = "generating"):
    """บันทึกการสร้างโค้ด"""
    activity_monitor.code_generation(language, component, status)

def start_task(task_name: str, total_steps: int = 100):
    """เริ่มงานใหม่"""
    activity_monitor.start_task(task_name, total_steps)

def update_progress(step: int, description: str = ""):
    """อัพเดทความคืบหน้า"""
    activity_monitor.update_progress(step, description)

def complete_task(result: str = "สำเร็จ"):
    """เสร็จสิ้นงาน"""
    activity_monitor.complete_task(result)