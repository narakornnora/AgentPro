"""
🎯 Project Type Classifier & Requirement Analyzer
ระบบซักถามและจำแนกประเภทโปรเจค ก่อนลงมือพัฒนา
"""

from typing import Dict, List, Any, Optional, Tuple
from openai import OpenAI
import json
from datetime import datetime
from enum import Enum

class ProjectType(Enum):
    STATIC_WEBSITE = "static_website"
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    ENTERPRISE_APP = "enterprise_app"
    ECOMMERCE = "ecommerce"
    PORTFOLIO = "portfolio"
    BLOG = "blog"
    DASHBOARD = "dashboard"
    GAME = "game"
    UNKNOWN = "unknown"

class ComplexityLevel(Enum):
    SIMPLE = "simple"        # 1-3 หน้า, แค่แสดงข้อมูล
    MODERATE = "moderate"    # 5-10 หน้า, มีฟอร์มและ interaction
    COMPLEX = "complex"      # 10+ หน้า, มีระบบหลายส่วน
    ENTERPRISE = "enterprise" # ระบบขนาดใหญ่, หลาย user roles

class RequirementAnalyzer:
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.project_brief = {}
        
    def analyze_initial_request(self, user_message: str) -> Dict:
        """วิเคราะห์คำขอเบื้องต้นและจำแนกประเภท"""
        
        analysis_prompt = f"""
คุณเป็นนักวิเคราะห์ระบบที่เก่ง ช่วยวิเคราะห์คำขอนี้:

"{user_message}"

ให้จำแนกประเภทและประเมินความซับซ้อน:

ประเภทโปรเจค:
- static_website: เว็บไซต์ธรรมดา แสดงข้อมูล (company profile, landing page)
- web_app: เว็บแอปพลิเคชัน (todo app, calculator, booking system) 
- mobile_app: แอปมือถือ iOS/Android
- enterprise_app: ระบบองค์กร (ERP, CRM, HR system)
- ecommerce: ร้านค้าออนไลน์
- portfolio: เว็บแสดงผลงาน
- blog: เว็บบล็อก/CMS
- dashboard: หน้าจอควบคุม/รายงาน
- game: เกมหรือแอปโต้ตอบ

ความซับซ้อน:
- simple: 1-3 หน้า, แค่แสดงข้อมูล
- moderate: 5-10 หน้า, มีฟอร์ม interaction
- complex: 10+ หน้า, ระบบหลายส่วน  
- enterprise: ระบบขนาดใหญ่, multi-user

ตอบเป็น JSON:
{{
    "project_type": "web_app",
    "complexity": "moderate", 
    "confidence": 85,
    "identified_features": ["user login", "data form", "responsive design"],
    "missing_requirements": ["target users", "specific features", "design style"],
    "needs_clarification": true,
    "suggested_questions": [
        "เว็บนี้ใครจะเป็นคนใช้หลัก ๆ?",
        "ต้องการให้มีระบบ login หรือไม่?", 
        "อยากได้หน้าตาแบบไหน? โมเดิร์น มินิมอล หรือ colorful?"
    ]
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # เก็บข้อมูลไว้ใน project brief
            self.project_brief.update({
                "initial_request": user_message,
                "analysis_date": datetime.now().isoformat(),
                "project_type": analysis["project_type"],
                "complexity": analysis["complexity"],
                "confidence": analysis["confidence"]
            })
            
            return analysis
            
        except Exception as e:
            return self._fallback_analysis(user_message)
    
    def generate_clarification_questions(self, analysis: Dict) -> List[str]:
        """สร้างคำถามซักถามเพิ่มเติมแบบสนทนาธรรมชาติ"""
        
        project_type = analysis.get("project_type", "unknown")
        missing_req = analysis.get("missing_requirements", [])
        
        base_questions = {
            "static_website": [
                "เว็บนี้เป็นของบริษัท ร้านค้า หรือใช้ส่วนตัว?",
                "มีเนื้อหาหลัก ๆ อะไรบ้างที่อยากให้คนเห็น?",
                "อยากได้แบบเรียบง่าย หรือโดดเด่นสะดุดตา?"
            ],
            "web_app": [
                "แอปนี้ช่วยแก้ปัญหาอะไรให้คนใช้?",
                "ต้องการระบบ login/สมัครสมาชิกมั้ย?",
                "มีข้อมูลที่ต้องเก็บบันทึกไว้หรือเปล่า?",
                "คนใช้จะเข้าผ่านคอม มือถือ หรือทั้งสอง?"
            ],
            "mobile_app": [
                "ต้องการทำทั้ง iOS และ Android หรือเลือกอันเดียว?",
                "แอปนี้ใช้ออนไลนหรือออฟไลน์ก็ได้?",
                "มีฟีเจอร์ที่ต้องใช้กล้อง GPS หรือ notification มั้ย?",
                "เป็นแอปฟรี หรือมีค่าใช้จ่าย?"
            ],
            "enterprise_app": [
                "องค์กรมีพนักงานกี่คน? แผนกไหนจะใช้บ้าง?",
                "มีระบบเก่าที่ต้องเชื่อมต่อด้วยมั้ย?",
                "ต้องการระบบ permission/role แยกระดับผู้ใช้มั้ย?",
                "มีข้อกำหนดด้าน security พิเศษไหม?"
            ],
            "ecommerce": [
                "ขายสินค้าประเภทไหน? มีสินค้ากี่รายการประมาณ?",
                "รับชำระเงินแบบไหนบ้าง? โอนธนาคาร บัตรเครดิต?",
                "มีระบบสมาชิก point หรือโปรโมชั่นมั้ย?",
                "ต้องการระบบจัดการสต็อกด้วยไหม?"
            ]
        }
        
        questions = base_questions.get(project_type, [
            "ช่วยอธิบายเพิ่มเติมหน่อยได้มั้ย ว่าต้องการอะไรแน่ ๆ?",
            "ใครจะเป็นคนใช้หลัก ๆ?",
            "มีตัวอย่างเว็บที่ชอบหรือไม่?"
        ])
        
        return questions[:3]  # คืนแค่ 3 คำถามเพื่อไม่ให้งง
    
    def collect_requirement(self, question: str, answer: str):
        """เก็บข้อมูล requirement ที่ได้จากการตอบคำถาม"""
        
        if "requirements" not in self.project_brief:
            self.project_brief["requirements"] = {}
            
        # วิเคราะห์คำตอบและเก็บข้อมูล
        self.project_brief["requirements"][question] = {
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
        
        # สกัดข้อมูลเพิ่มเติมจากคำตอบ
        extracted_info = self._extract_info_from_answer(question, answer)
        self.project_brief.update(extracted_info)
    
    def is_ready_for_development(self) -> Tuple[bool, float, List[str]]:
        """ตรวจสอบว่าข้อมูลเพียงพอสำหรับพัฒนาหรือยัง"""
        
        required_info = {
            "project_type": 1.0,
            "target_users": 0.8,
            "main_features": 0.9,
            "design_style": 0.6,
            "technical_requirements": 0.7
        }
        
        available_info = []
        missing_info = []
        total_score = 0
        max_score = sum(required_info.values())
        
        for info_type, weight in required_info.items():
            if self._has_info(info_type):
                available_info.append(info_type)
                total_score += weight
            else:
                missing_info.append(info_type)
        
        readiness_score = (total_score / max_score) * 100
        is_ready = readiness_score >= 70  # ต้องมีข้อมูลอย่างน้อย 70%
        
        return is_ready, readiness_score, missing_info
    
    def _has_info(self, info_type: str) -> bool:
        """ตรวจสอบว่ามีข้อมูลประเภทนี้หรือไม่"""
        
        checks = {
            "project_type": lambda: self.project_brief.get("project_type") != "unknown",
            "target_users": lambda: any(key in str(self.project_brief) for key in ["users", "audience", "คน", "ใช้"]),
            "main_features": lambda: any(key in str(self.project_brief) for key in ["features", "function", "ฟีเจอร์", "ทำ"]),
            "design_style": lambda: any(key in str(self.project_brief) for key in ["style", "design", "สี", "แบบ", "หน้าตา"]),
            "technical_requirements": lambda: any(key in str(self.project_brief) for key in ["login", "database", "mobile", "responsive"])
        }
        
        return checks.get(info_type, lambda: False)()
    
    def _extract_info_from_answer(self, question: str, answer: str) -> Dict:
        """สกัดข้อมูลจากคำตอบ"""
        
        extracted = {}
        answer_lower = answer.lower()
        
        # Target users
        if any(word in question.lower() for word in ["ใคร", "คน", "user"]):
            extracted["target_users"] = answer
        
        # Design preferences  
        if any(word in question.lower() for word in ["แบบ", "หน้าตา", "สี", "design"]):
            extracted["design_style"] = answer
            
        # Technical requirements
        if "login" in answer_lower or "สมาชิก" in answer:
            extracted["needs_auth"] = True
        if "database" in answer_lower or "เก็บข้อมูล" in answer:
            extracted["needs_database"] = True
        if "mobile" in answer_lower or "มือถือ" in answer:
            extracted["needs_mobile"] = True
            
        return extracted
    
    def _fallback_analysis(self, user_message: str) -> Dict:
        """กรณีที่ AI analysis ล้มเหลว ใช้ rule-based"""
        
        message_lower = user_message.lower()
        
        # Simple pattern matching
        if any(word in message_lower for word in ["app", "แอป", "application"]):
            if any(word in message_lower for word in ["mobile", "มือถือ", "ios", "android"]):
                project_type = "mobile_app"
            else:
                project_type = "web_app"
        elif any(word in message_lower for word in ["website", "เว็บไซต์", "หน้าเว็บ"]):
            project_type = "static_website"
        elif any(word in message_lower for word in ["shop", "ร้าน", "ขาย", "ecommerce"]):
            project_type = "ecommerce"
        else:
            project_type = "unknown"
            
        return {
            "project_type": project_type,
            "complexity": "moderate",
            "confidence": 50,
            "needs_clarification": True,
            "suggested_questions": [
                "ช่วยอธิบายให้ฟังหน่อยได้มั้ย ว่าอยากได้อะไรแน่ ๆ?",
                "ใครจะเป็นคนใช้หลัก ๆ?",
                "มีฟีเจอร์อะไรที่สำคัญบ้าง?"
            ]
        }
    
    def get_project_brief(self) -> Dict:
        """ดึงข้อมูล project brief ทั้งหมด"""
        return self.project_brief.copy()
    
    def generate_final_specification(self) -> str:
        """สร้างเอกสาร specification สุดท้าย"""
        
        is_ready, score, missing = self.is_ready_for_development()
        
        spec = f"""
# 📋 Project Specification

## ข้อมูลโปรเจค
- **ประเภท:** {self.project_brief.get('project_type', 'ไม่ระบุ')}
- **ความซับซ้อน:** {self.project_brief.get('complexity', 'ปานกลาง')}
- **ความพร้อม:** {score:.1f}% {'✅ พร้อมพัฒนา' if is_ready else '⚠️ ต้องข้อมูลเพิ่ม'}

## Requirements ที่รวบรวมได้
"""
        
        for key, value in self.project_brief.get("requirements", {}).items():
            spec += f"- **{key}:** {value['answer']}\n"
            
        if missing:
            spec += f"\n## ข้อมูลที่ยังขาด\n"
            for item in missing:
                spec += f"- {item}\n"
                
        return spec