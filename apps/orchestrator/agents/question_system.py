"""
🤔 Intelligent Question System
ระบบถามคำถามเพิ่มเติมเมื่อข้อมูลไม่ครบหรือไม่ชัดเจน
"""

from typing import Dict, List, Any, Optional, Tuple
import re
import json
from dataclasses import dataclass
from enum import Enum

class RequirementType(Enum):
    """ประเภทของ requirements"""
    UI_DESIGN = "ui_design"
    FUNCTIONALITY = "functionality" 
    TECHNOLOGY = "technology"
    CONTENT = "content"
    BUSINESS = "business"
    USER_EXPERIENCE = "user_experience"

@dataclass
class Question:
    """คำถามที่จะถาม"""
    id: str
    text: str
    category: RequirementType
    priority: int  # 1=สูงสุด, 5=ต่ำสุด
    options: List[str] = None  # ตัวเลือก (ถ้ามี)
    follow_up: List[str] = None  # คำถามต่อเนื่อง

class RequirementAnalyzer:
    """วิเคราะห์ความต้องการและสร้างคำถามเพิ่มเติม"""
    
    def __init__(self):
        self.question_templates = self._load_question_templates()
        self.keywords = self._load_keywords()
        self.context_history = []
        
    def _load_question_templates(self) -> Dict:
        """โหลดเทมเพลตคำถาม"""
        return {
            # UI & Design Questions
            "color_scheme": Question(
                id="color_scheme",
                text="🎨 คุณต้องการโทนสีแบบไหน?",
                category=RequirementType.UI_DESIGN,
                priority=2,
                options=["สีสดใส (Vibrant)", "สีอ่อน (Pastel)", "สีเข้ม (Dark)", "สีธรรมชาติ (Earth tones)", "ไม่แน่ใจ"]
            ),
            
            "layout_style": Question(
                id="layout_style", 
                text="📱 คุณชอบ layout แบบไหน?",
                category=RequirementType.UI_DESIGN,
                priority=2,
                options=["แบบ Modern/Minimal", "แบบ Corporate", "แบบ Creative/Artistic", "แบบ E-commerce", "ไม่แน่ใจ"]
            ),
            
            "target_device": Question(
                id="target_device",
                text="📱 ใช้งานหลัก ๆ บนอุปกรณ์ไหน?",
                category=RequirementType.UI_DESIGN,
                priority=1,
                options=["มือถือ (Mobile First)", "คอมพิวเตอร์ (Desktop)", "ทั้งสองเท่า ๆ กัน", "แท็บเล็ต"]
            ),
            
            # Functionality Questions  
            "user_auth": Question(
                id="user_auth",
                text="👤 ต้องการระบบ Login/สมัครสมาชิกไหม?",
                category=RequirementType.FUNCTIONALITY,
                priority=1,
                options=["ต้องการ - แบบง่าย", "ต้องการ - แบบครบครัน", "ไม่ต้องการ", "ยังไม่แน่ใจ"]
            ),
            
            "data_storage": Question(
                id="data_storage", 
                text="💾 ต้องการเก็บข้อมูลแบบไหน?",
                category=RequirementType.FUNCTIONALITY,
                priority=2,
                options=["Local (ในเครื่อง)", "Cloud Database", "ไฟล์ JSON/CSV", "ไม่ต้องเก็บข้อมูล"]
            ),
            
            "key_features": Question(
                id="key_features",
                text="⚡ ฟีเจอร์หลัก ๆ ที่ต้องการคืออะไร? (เลือกได้หลายข้อ)",
                category=RequirementType.FUNCTIONALITY, 
                priority=1,
                options=["ค้นหา/กรองข้อมูล", "อัพโหลดไฟล์/รูป", "แชท/ความคิดเห็น", "การแจ้งเตือน", "รายงาน/กราฟ", "อื่น ๆ"]
            ),
            
            # Content Questions
            "content_type": Question(
                id="content_type",
                text="📝 เนื้อหาหลักคืออะไร?",
                category=RequirementType.CONTENT,
                priority=1,
                options=["ข้อความ/บทความ", "รูปภาพ/แกลเลอรี่", "วิดีโอ", "ตาราง/ข้อมูล", "ผลิตภัณฑ์/บริการ"]
            ),
            
            "language_preference": Question(
                id="language_preference", 
                text="🌐 ภาษาที่ใช้ในระบบ?",
                category=RequirementType.CONTENT,
                priority=2,
                options=["ไทย", "อังกฤษ", "ทั้งไทย-อังกฤษ", "หลายภาษา"]
            ),
            
            # Business Questions
            "business_type": Question(
                id="business_type",
                text="🏢 ลักษณะงานหรือธุรกิจคืออะไร?",
                category=RequirementType.BUSINESS,
                priority=1,
                options=["ร้านค้า/E-commerce", "บริษัท/องค์กร", "การศึกษา", "ส่วนตัว/โปรเจกต์", "ไม่แน่ใจ"]
            ),
            
            "target_users": Question(
                id="target_users",
                text="👥 กลุ่มเป้าหมายคือใคร?",
                category=RequirementType.BUSINESS, 
                priority=2,
                options=["ลูกค้าทั่วไป", "พนักงานในบริษัท", "นักเรียน/นักศึกษา", "ผู้เชี่ยวชาญ", "ไม่แน่ใจ"]
            )
        }
    
    def _load_keywords(self) -> Dict:
        """โหลด keywords สำหรับการวิเคราะห์"""
        return {
            "vague_terms": [
                "สวย", "ดี", "เจ๋ง", "ง่าย", "สะดวก", "ทันสมัย", 
                "ปกติ", "ธรรมดา", "คล้าย ๆ", "ประมาณ", "บางอย่าง"
            ],
            "missing_details": [
                "เว็บไซต์", "แอป", "ระบบ", "โปรแกรม", "หน้าเว็บ",
                "แอพพลิเคชั่น", "เครื่องมือ", "platform"
            ],
            "color_keywords": [
                "สี", "โทนสี", "สีสัน", "color", "theme"
            ],
            "feature_keywords": [
                "ฟีเจอร์", "ฟังก์ชั่น", "คุณสมบัติ", "feature", "function"
            ]
        }
    
    def analyze_requirement(self, user_input: str, context: Dict = None) -> Tuple[Dict, List[Question]]:
        """วิเคราะห์ความต้องการและสร้างคำถามเพิ่มเติม"""
        
        analysis = {
            "clarity_score": self._calculate_clarity_score(user_input),
            "detected_type": self._detect_project_type(user_input),
            "missing_aspects": self._find_missing_aspects(user_input),
            "vague_terms": self._find_vague_terms(user_input),
            "confidence_level": 0
        }
        
        # สร้างคำถามตาม analysis
        questions = self._generate_questions(analysis, user_input, context)
        
        # คำนวณ confidence level
        analysis["confidence_level"] = self._calculate_confidence(analysis, user_input)
        
        return analysis, questions
    
    def _calculate_clarity_score(self, text: str) -> float:
        """คำนวณคะแนนความชัดเจน (0-100)"""
        score = 50  # เริ่มต้น 50%
        
        # เพิ่มคะแนนถ้ามีรายละเอียด
        if len(text.split()) > 10:
            score += 20
        if len(text) > 50:
            score += 10
            
        # ลดคะแนนถ้ามี vague terms
        vague_count = sum(1 for term in self.keywords["vague_terms"] 
                         if term in text.lower())
        score -= vague_count * 5
        
        # เพิ่มคะแนนถ้ามี specific terms
        specific_terms = ["สี", "ฟีเจอร์", "ระบบ", "ฐานข้อมูล", "API"]
        specific_count = sum(1 for term in specific_terms 
                           if term in text.lower())
        score += specific_count * 5
        
        return max(0, min(100, score))
    
    def _detect_project_type(self, text: str) -> str:
        """ตรวจหาประเภทโปรเจกต์"""
        text_lower = text.lower()
        
        type_keywords = {
            "e_commerce": ["ร้านค้า", "ขาย", "สินค้า", "shop", "store", "ecommerce"],
            "portfolio": ["portfolio", "ผลงาน", "แฟ้มสะสมผลงาน", "โชว์"],
            "blog": ["blog", "บล็อก", "บทความ", "เขียน"],
            "landing_page": ["landing", "หน้าเดียว", "โปรโมท"],
            "dashboard": ["dashboard", "แดชบอร์ด", "รายงาน", "กราฟ"],
            "social": ["social", "โซเชียล", "แชท", "community"],
            "business": ["บริษัท", "องค์กร", "ธุรกิจ", "corporate"],
            "education": ["การศึกษา", "เรียน", "คอร์ส", "education"]
        }
        
        for project_type, keywords in type_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return project_type
                
        return "general"
    
    def _find_missing_aspects(self, text: str) -> List[str]:
        """หา aspects ที่ขาดหายไป"""
        missing = []
        text_lower = text.lower()
        
        # ตรวจสอบแต่ละ aspect
        aspects_to_check = {
            "color_scheme": ["สี", "โทนสี", "color", "theme"],
            "layout": ["layout", "รูปแบบ", "หน้าตา", "design"],
            "functionality": ["ฟีเจอร์", "ฟังก์ชั่น", "คุณสมบัติ", "feature"],
            "target_audience": ["ลูกค้า", "ผู้ใช้", "กลุ่มเป้าหมาย", "user"],
            "content_type": ["เนื้อหา", "ข้อมูล", "content", "information"],
            "technology": ["เทคโนโลยี", "database", "api", "framework"]
        }
        
        for aspect, keywords in aspects_to_check.items():
            if not any(keyword in text_lower for keyword in keywords):
                missing.append(aspect)
                
        return missing
    
    def _find_vague_terms(self, text: str) -> List[str]:
        """หาคำที่ไม่ชัดเจน"""
        vague_found = []
        text_lower = text.lower()
        
        for term in self.keywords["vague_terms"]:
            if term in text_lower:
                vague_found.append(term)
                
        return vague_found
    
    def _generate_questions(self, analysis: Dict, user_input: str, context: Dict = None) -> List[Question]:
        """สร้างคำถามตาม analysis"""
        questions = []
        
        # ถ้า clarity score ต่ำ ถามคำถามพื้นฐาน
        if analysis["clarity_score"] < 70:
            
            # ถาม project type ก่อนถ้ายังไม่ชัด
            if analysis["detected_type"] == "general":
                questions.append(Question(
                    id="clarify_project",
                    text="🤔 คุณต้องการสร้างอะไรครับ? (เช่น เว็บไซต์ร้านค้า, แอป todo, หน้า portfolio)",
                    category=RequirementType.BUSINESS,
                    priority=1
                ))
            
            # ถามตาม missing aspects
            for aspect in analysis["missing_aspects"][:3]:  # ถามแค่ 3 อย่างแรก
                if aspect in self.question_templates:
                    questions.append(self.question_templates[aspect])
        
        # ถามคำถามเฉพาะตาม project type
        project_specific_questions = self._get_project_specific_questions(analysis["detected_type"])
        questions.extend(project_specific_questions[:2])  # เพิ่มแค่ 2 คำถาม
        
        # เรียงตาม priority
        questions.sort(key=lambda q: q.priority)
        
        return questions[:3]  # คืนแค่ 3 คำถามแรก เพื่อไม่ให้ overwhelming
    
    def _get_project_specific_questions(self, project_type: str) -> List[Question]:
        """ดึงคำถามเฉพาะตาม project type"""
        
        type_questions = {
            "e_commerce": [
                self.question_templates["user_auth"],
                self.question_templates["target_users"],
                Question(
                    id="payment_method",
                    text="💳 ต้องการระบบชำระเงินไหม?",
                    category=RequirementType.FUNCTIONALITY,
                    priority=2,
                    options=["ต้องการ", "ไม่ต้องการตอนนี้", "ยังไม่แน่ใจ"]
                )
            ],
            
            "portfolio": [
                self.question_templates["layout_style"],
                self.question_templates["content_type"],
                Question(
                    id="portfolio_sections",
                    text="📂 ต้องการหมวดหมู่ไหน? (เลือกได้หลายข้อ)",
                    category=RequirementType.CONTENT,
                    priority=2,
                    options=["About Me", "Portfolio/ผลงาน", "Resume/ประวัติ", "Contact", "Blog", "Services"]
                )
            ],
            
            "dashboard": [
                self.question_templates["data_storage"],
                Question(
                    id="chart_types",
                    text="📊 ต้องการกราฟ/แผนภูมิแบบไหน?",
                    category=RequirementType.FUNCTIONALITY,
                    priority=2,
                    options=["Bar Chart", "Line Chart", "Pie Chart", "Table", "ไม่แน่ใจ"]
                )
            ]
        }
        
        return type_questions.get(project_type, [])
    
    def _calculate_confidence(self, analysis: Dict, user_input: str) -> float:
        """คำนวณระดับความมั่นใจที่จะสร้างได้ถูกต้อง"""
        
        base_confidence = analysis["clarity_score"] / 100
        
        # ลดความมั่นใจถ้ามี missing aspects เยอะ
        missing_penalty = len(analysis["missing_aspects"]) * 0.1
        base_confidence -= missing_penalty
        
        # ลดความมั่นใจถ้ามี vague terms เยอะ
        vague_penalty = len(analysis["vague_terms"]) * 0.05
        base_confidence -= vague_penalty
        
        return max(0, min(1, base_confidence))
    
    def format_questions_for_chat(self, questions: List[Question]) -> str:
        """จัดรูปแบบคำถามสำหรับแสดงใน chat"""
        
        if not questions:
            return ""
            
        formatted = "🤔 **ช่วยให้ข้อมูลเพิ่มหน่อยครับ เพื่อให้ได้ผลลัพธ์ที่ดีที่สุด:**\n\n"
        
        for i, q in enumerate(questions, 1):
            formatted += f"**{i}. {q.text}**\n"
            
            if q.options:
                for j, option in enumerate(q.options, 1):
                    formatted += f"   {j}. {option}\n"
            
            formatted += "\n"
        
        formatted += "💡 *ตอบได้แค่ข้อที่รู้นะครับ ส่วนที่ไม่แน่ใจข้ามไปได้*"
        
        return formatted

# Global instance
requirement_analyzer = RequirementAnalyzer()

def analyze_user_requirement(user_input: str, context: Dict = None) -> Tuple[Dict, str]:
    """
    วิเคราะห์ความต้องการและสร้างคำถามเพิ่มเติม
    
    Returns:
        Tuple[Dict, str]: (analysis_result, formatted_questions)
    """
    
    analysis, questions = requirement_analyzer.analyze_requirement(user_input, context)
    
    # ถ้าความมั่นใจสูงพอ ไม่ต้องถามเพิ่ม
    if analysis["confidence_level"] >= 0.8:
        return analysis, ""
    
    # จัดรูปแบบคำถาม
    formatted_questions = requirement_analyzer.format_questions_for_chat(questions)
    
    return analysis, formatted_questions