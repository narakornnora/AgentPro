"""
Requirements Tracking System
บันทึกและติดตามความต้องการทั้งหมดของผู้ใช้เพื่อป้องกันการทำลายฟีเจอร์เก่า
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json
import time
import uuid
from datetime import datetime
import hashlib

class RequirementType(Enum):
    FUNCTIONAL = "functional"          # ความต้องการทางการทำงาน
    UI_UX = "ui_ux"                   # ความต้องการด้าน UI/UX  
    CONTENT = "content"               # ความต้องการด้านเนื้อหา
    PERFORMANCE = "performance"       # ความต้องการด้านประสิทธิภาพ
    ACCESSIBILITY = "accessibility"   # ความต้องการด้าน accessibility
    BUSINESS = "business"             # ความต้องการทางธุรกิจ

class RequirementStatus(Enum):
    PENDING = "pending"               # รอดำเนินการ
    IN_PROGRESS = "in_progress"       # กำลังดำเนินการ
    IMPLEMENTED = "implemented"       # ดำเนินการแล้ว
    TESTED = "tested"                # ทดสอบแล้ว
    VERIFIED = "verified"            # ยืนยันแล้ว
    DEPRECATED = "deprecated"         # ยกเลิกแล้ว

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Requirement:
    id: str
    type: RequirementType
    title: str
    description: str
    user_input: str                   # ข้อความต้นฉบับของผู้ใช้
    acceptance_criteria: List[str]    # เกณฑ์การยอมรับ
    priority: Priority
    status: RequirementStatus
    created_at: float
    updated_at: float
    implemented_at: Optional[float] = None
    verified_at: Optional[float] = None
    
    # Relationships
    depends_on: List[str] = field(default_factory=list)  # requirements ที่ต้องทำก่อน
    blocks: List[str] = field(default_factory=list)      # requirements ที่ถูกบล็อก
    related_to: List[str] = field(default_factory=list)  # requirements ที่เกี่ยวข้อง
    
    # Implementation tracking
    implemented_files: List[str] = field(default_factory=list)  # ไฟล์ที่เกี่ยวข้อง
    test_cases: List[Dict[str, Any]] = field(default_factory=list)  # test cases
    
    # Metadata
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "user_input": self.user_input,
            "acceptance_criteria": self.acceptance_criteria,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "implemented_at": self.implemented_at,
            "verified_at": self.verified_at,
            "depends_on": self.depends_on,
            "blocks": self.blocks,
            "related_to": self.related_to,
            "implemented_files": self.implemented_files,
            "test_cases": self.test_cases,
            "tags": list(self.tags),
            "metadata": self.metadata
        }

class RequirementTracker:
    """ระบบติดตาม requirements ทั้งหมด"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.requirements: Dict[str, Requirement] = {}
        self.user_sessions: Dict[str, List[str]] = {}  # user -> requirement ids
        self.requirement_history: List[Dict[str, Any]] = []
        
    def extract_requirements_from_input(self, user_input: str, user_id: str) -> List[Requirement]:
        """แยก requirements จากการพูดของผู้ใช้"""
        
        current_time = time.time()
        requirements = []
        
        # ใช้ AI หรือ NLP เพื่อแยก requirements
        extracted_reqs = self._ai_extract_requirements(user_input)
        
        for req_data in extracted_reqs:
            req_id = self._generate_requirement_id(req_data["title"])
            
            requirement = Requirement(
                id=req_id,
                type=RequirementType(req_data["type"]),
                title=req_data["title"],
                description=req_data["description"],
                user_input=user_input,
                acceptance_criteria=req_data["acceptance_criteria"],
                priority=Priority(req_data["priority"]),
                status=RequirementStatus.PENDING,
                created_at=current_time,
                updated_at=current_time,
                tags=set(req_data.get("tags", []))
            )
            
            # บันทึก requirement
            self.requirements[req_id] = requirement
            
            # เชื่อมโยงกับ user
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = []
            self.user_sessions[user_id].append(req_id)
            
            requirements.append(requirement)
            
            # บันทึกประวัติ
            self._record_history("requirement_created", {
                "requirement_id": req_id,
                "user_id": user_id,
                "user_input": user_input
            })
        
        return requirements
    
    def _ai_extract_requirements(self, user_input: str) -> List[Dict[str, Any]]:
        """ใช้ AI แยก requirements จากข้อความผู้ใช้"""
        
        # สำหรับตัวอย่าง ใช้ rule-based approach
        # ในการใช้งานจริงควรใช้ AI model
        
        requirements = []
        
        # ตัวอย่างการแยก requirements แบบง่าย
        if "สร้าง" in user_input or "ทำ" in user_input:
            if "เว็บ" in user_input:
                requirements.append({
                    "type": "functional",
                    "title": "สร้างเว็บไซต์",
                    "description": f"สร้างเว็บไซต์ตามที่ผู้ใช้ต้องการ: {user_input}",
                    "acceptance_criteria": [
                        "เว็บไซต์สามารถแสดงผลได้",
                        "มี responsive design",
                        "โหลดได้ในเบราว์เซอร์"
                    ],
                    "priority": 3,
                    "tags": ["website", "create"]
                })
        
        if "สี" in user_input or "color" in user_input:
            requirements.append({
                "type": "ui_ux",
                "title": "ปรับแต่งสีสัน",
                "description": f"ปรับแต่งสีสันตามที่ต้องการ: {user_input}",
                "acceptance_criteria": [
                    "สีสันตรงตามที่ผู้ใช้ต้องการ",
                    "สีสันสวยงามและเข้ากัน",
                    "อ่านง่ายและ accessible"
                ],
                "priority": 2,
                "tags": ["color", "design", "ui"]
            })
        
        if "ปุ่ม" in user_input or "button" in user_input:
            requirements.append({
                "type": "functional",
                "title": "เพิ่มปุ่ม",
                "description": f"เพิ่มปุ่มตามที่ต้องการ: {user_input}",
                "acceptance_criteria": [
                    "ปุ่มแสดงผลได้",
                    "ปุ่มทำงานได้",
                    "ปุ่มมี hover effect"
                ],
                "priority": 2,
                "tags": ["button", "interactive", "ui"]
            })
        
        return requirements
    
    def update_requirement_status(self, req_id: str, new_status: RequirementStatus, 
                                metadata: Dict[str, Any] = None) -> bool:
        """อัพเดทสถานะของ requirement"""
        
        if req_id not in self.requirements:
            return False
        
        req = self.requirements[req_id]
        old_status = req.status
        req.status = new_status
        req.updated_at = time.time()
        
        if new_status == RequirementStatus.IMPLEMENTED:
            req.implemented_at = time.time()
        elif new_status == RequirementStatus.VERIFIED:
            req.verified_at = time.time()
        
        if metadata:
            req.metadata.update(metadata)
        
        # บันทึกประวัติ
        self._record_history("status_changed", {
            "requirement_id": req_id,
            "old_status": old_status.value,
            "new_status": new_status.value,
            "metadata": metadata
        })
        
        return True
    
    def add_implementation_files(self, req_id: str, files: List[str]):
        """เพิ่มไฟล์ที่เกี่ยวข้องกับการ implement requirement"""
        
        if req_id not in self.requirements:
            return False
        
        req = self.requirements[req_id]
        req.implemented_files.extend(files)
        req.updated_at = time.time()
        
        self._record_history("files_added", {
            "requirement_id": req_id,
            "files": files
        })
        
        return True
    
    def add_test_case(self, req_id: str, test_case: Dict[str, Any]):
        """เพิ่ม test case สำหรับ requirement"""
        
        if req_id not in self.requirements:
            return False
        
        test_case["id"] = str(uuid.uuid4())
        test_case["created_at"] = time.time()
        
        req = self.requirements[req_id]
        req.test_cases.append(test_case)
        req.updated_at = time.time()
        
        self._record_history("test_case_added", {
            "requirement_id": req_id,
            "test_case": test_case
        })
        
        return True
    
    def get_all_active_requirements(self) -> List[Requirement]:
        """ดึง requirements ทั้งหมดที่ยังใช้งานอยู่"""
        return [
            req for req in self.requirements.values() 
            if req.status != RequirementStatus.DEPRECATED
        ]
    
    def get_requirements_by_status(self, status: RequirementStatus) -> List[Requirement]:
        """ดึง requirements ตามสถานะ"""
        return [
            req for req in self.requirements.values() 
            if req.status == status
        ]
    
    def get_user_requirements(self, user_id: str) -> List[Requirement]:
        """ดึง requirements ของผู้ใช้คนหนึ่ง"""
        if user_id not in self.user_sessions:
            return []
        
        req_ids = self.user_sessions[user_id]
        return [self.requirements[req_id] for req_id in req_ids if req_id in self.requirements]
    
    def find_conflicting_requirements(self, new_requirement: Requirement) -> List[Requirement]:
        """หา requirements ที่อาจขัดแย้งกับ requirement ใหม่"""
        conflicts = []
        
        for req in self.requirements.values():
            if req.status == RequirementStatus.DEPRECATED:
                continue
                
            # ตรวจสอบ conflict แบบง่าย
            if (req.type == new_requirement.type and 
                req.id != new_requirement.id and
                self._check_conflict(req, new_requirement)):
                conflicts.append(req)
        
        return conflicts
    
    def _check_conflict(self, req1: Requirement, req2: Requirement) -> bool:
        """ตรวจสอบว่า requirements 2 ตัวขัดแย้งกันไหม"""
        
        # ตัวอย่างการตรวจสอบ conflict แบบง่าย
        # ในการใช้งานจริงควรใช้ AI หรือ logic ที่ซับซ้อนกว่า
        
        if req1.type == RequirementType.UI_UX and req2.type == RequirementType.UI_UX:
            # ตรวจสอบ conflict ด้าน UI/UX (เช่น สีสันขัดแย้ง)
            req1_colors = [tag for tag in req1.tags if "color" in tag.lower()]
            req2_colors = [tag for tag in req2.tags if "color" in tag.lower()]
            
            if req1_colors and req2_colors and req1_colors != req2_colors:
                return True
        
        return False
    
    def generate_regression_tests(self) -> List[Dict[str, Any]]:
        """สร้าง regression tests จาก requirements ทั้งหมด"""
        
        tests = []
        
        for req in self.get_all_active_requirements():
            if req.status in [RequirementStatus.IMPLEMENTED, RequirementStatus.TESTED, RequirementStatus.VERIFIED]:
                
                # สร้าง test cases จาก acceptance criteria
                for i, criteria in enumerate(req.acceptance_criteria):
                    test_case = {
                        "id": f"{req.id}_test_{i}",
                        "requirement_id": req.id,
                        "title": f"Test: {criteria}",
                        "description": f"Verify that {criteria}",
                        "type": "regression",
                        "priority": req.priority.value,
                        "test_steps": self._generate_test_steps(criteria, req),
                        "expected_result": criteria,
                        "files_to_check": req.implemented_files
                    }
                    tests.append(test_case)
        
        return tests
    
    def _generate_test_steps(self, criteria: str, requirement: Requirement) -> List[str]:
        """สร้าง test steps จาก acceptance criteria"""
        
        steps = []
        
        if requirement.type == RequirementType.FUNCTIONAL:
            if "ปุ่ม" in criteria or "button" in criteria:
                steps = [
                    "เปิดเว็บไซต์ในเบราว์เซอร์",
                    "ค้นหาปุ่มที่เกี่ยวข้อง",
                    "คลิกปุ่ม",
                    "ตรวจสอบการทำงานของปุ่ม"
                ]
            elif "แสดงผล" in criteria:
                steps = [
                    "เปิดเว็บไซต์ในเบราว์เซอร์",
                    "ตรวจสอบว่าหน้าเว็บโหลดสำเร็จ",
                    "ตรวจสอบเนื้อหาที่แสดง"
                ]
        
        elif requirement.type == RequirementType.UI_UX:
            if "สี" in criteria or "color" in criteria:
                steps = [
                    "เปิดเว็บไซต์ในเบราว์เซอร์",
                    "ตรวจสอบโทนสีของเว็บไซต์",
                    "ตรวจสอบความเข้ากันของสี",
                    "ตรวจสอบ contrast ratio"
                ]
        
        if not steps:
            steps = [
                "เปิดเว็บไซต์",
                f"ตรวจสอบ: {criteria}",
                "ยืนยันผลลัพธ์"
            ]
        
        return steps
    
    def _generate_requirement_id(self, title: str) -> str:
        """สร้าง unique ID สำหรับ requirement"""
        timestamp = str(int(time.time() * 1000))
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        return f"req_{timestamp}_{title_hash}"
    
    def _record_history(self, action: str, data: Dict[str, Any]):
        """บันทึกประวัติการเปลี่ยนแปลง"""
        history_entry = {
            "timestamp": time.time(),
            "action": action,
            "data": data
        }
        self.requirement_history.append(history_entry)
    
    def export_requirements(self) -> Dict[str, Any]:
        """ส่งออกข้อมูล requirements ทั้งหมด"""
        return {
            "project_id": self.project_id,
            "requirements": {req_id: req.to_dict() for req_id, req in self.requirements.items()},
            "user_sessions": self.user_sessions,
            "history": self.requirement_history,
            "exported_at": time.time()
        }
    
    def import_requirements(self, data: Dict[str, Any]):
        """นำเข้าข้อมูล requirements"""
        self.project_id = data.get("project_id", self.project_id)
        
        # Load requirements
        for req_id, req_data in data.get("requirements", {}).items():
            req = Requirement(
                id=req_data["id"],
                type=RequirementType(req_data["type"]),
                title=req_data["title"],
                description=req_data["description"],
                user_input=req_data["user_input"],
                acceptance_criteria=req_data["acceptance_criteria"],
                priority=Priority(req_data["priority"]),
                status=RequirementStatus(req_data["status"]),
                created_at=req_data["created_at"],
                updated_at=req_data["updated_at"],
                implemented_at=req_data.get("implemented_at"),
                verified_at=req_data.get("verified_at"),
                depends_on=req_data.get("depends_on", []),
                blocks=req_data.get("blocks", []),
                related_to=req_data.get("related_to", []),
                implemented_files=req_data.get("implemented_files", []),
                test_cases=req_data.get("test_cases", []),
                tags=set(req_data.get("tags", [])),
                metadata=req_data.get("metadata", {})
            )
            self.requirements[req_id] = req
        
        # Load other data
        self.user_sessions = data.get("user_sessions", {})
        self.requirement_history = data.get("history", [])