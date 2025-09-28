"""
💬 Natural Conversational AI Agent
คุยสนทนาธรรมชาติ ถามเพิ่มเติมเมื่อข้อมูลไม่ชัด ไม่รีบสร้างโค้ด
"""

from typing import Dict, List, Any, Optional
from openai import OpenAI
import json
import re
from datetime import datetime
from .activity_monitor import log_agent_action, start_task, update_progress, complete_task

class ConversationalDesignAgent:
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.conversation_history = []
        self.project_context = {}
        self.clarification_needed = False
        
    def analyze_request(self, user_message: str, conversation_history: List = None) -> Dict:
        """วิเคราะห์คำขอและตัดสินใจว่าต้องถามเพิ่มหรือไม่"""
        
        log_agent_action("ConversationalAgent", f"วิเคราะห์คำขอ: {user_message[:50]}...")
        
        # สร้าง context จากประวัติการสนทนา
        context = self._build_context(conversation_history or [])
        
        analysis_prompt = f"""
คุณเป็น AI Designer ที่เก่งในการสร้างเว็บไซต์และแอป คุณต้องวิเคราะห์คำขอนี้:

ข้อความจากผู้ใช้: "{user_message}"

ประวัติการสนทนา:
{context}

ให้วิเคราะห์ว่า:
1. ข้อมูลเพียงพอสำหรับสร้างแอป/เว็บไซต์หรือไม่?
2. หากไม่เพียงพอ ต้องถามอะไรเพิ่มเติม?
3. ถามแบบสนทนาธรรมชาติ ไม่ใช่คำถามแบบแบนเ questionnaire

ตอบเป็น JSON:
{{
    "needs_clarification": true/false,
    "confidence_level": 0-100,
    "missing_info": ["สีธีม", "target audience", "ฟีเจอร์หลัก"],
    "conversational_questions": [
        "เอ้า ทำเว็บร้านกาแฟนะ... แต่เดี๋ยวก่อน อยากได้โทนสีแบบไหนล่ะ? อบอุ่น ๆ แบบคาเฟ่ย่านเก่า หรือแบบโมเดิร์นเซียน ๆ?",
        "แล้วคนที่มาใช้เว็บส่วนใหญ่เป็นใครเอ่ย? วัยรุ่นที่ชอบ aesthetic หรือคนทำงานที่อยากหาที่นั่งชิล ๆ?"
    ],
    "can_proceed": true/false,
    "next_action": "ask_questions" หรือ "start_development"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            log_agent_action("ConversationalAgent", f"วิเคราะห์เสร็จ - confidence: {analysis.get('confidence_level', 0)}%")
            
            return analysis
            
        except Exception as e:
            log_agent_action("ConversationalAgent", f"Error ในการวิเคราะห์: {str(e)}", {"error": str(e)})
            return {
                "needs_clarification": True,
                "confidence_level": 0,
                "conversational_questions": ["เอ๊ะ เกิดข้อผิดพลาดนิดหน่อย ช่วยบอกรายละเอียดเพิ่มเติมให้หน่อยได้มั้ย? อยากได้อะไรยังไงแน่ๆ?"],
                "can_proceed": False,
                "next_action": "ask_questions"
            }
    
    def generate_conversational_response(self, user_message: str, missing_info: List[str] = None) -> str:
        """สร้างคำตอบแบบสนทนาธรรมชาติ"""
        
        log_agent_action("ConversationalAgent", "สร้างคำตอบแบบสนทนา")
        
        # เก็บข้อมูลที่ได้จากข้อความ
        extracted_info = self._extract_project_info(user_message)
        self.project_context.update(extracted_info)
        
        conversation_prompt = f"""
คุณเป็น AI Developer ที่เป็นกันเองและชอบคุยสนทนา คุณกำลังช่วยสร้างเว็บไซต์/แอปให้ลูกค้า

ข้อความจากลูกค้า: "{user_message}"

ข้อมูลที่รู้แล้ว:
{json.dumps(self.project_context, ensure_ascii=False, indent=2)}

ข้อมูลที่ยังขาด: {missing_info or []}

ให้คุยแบบเป็นธรรมชาติ เป็นกันเอง และถามข้อมูลที่ขาดอย่างไม่เป็นทางการ เช่น:

❌ ไม่ดี: "กรุณาระบุสีธีม target audience และฟีเจอร์หลัก"
✅ ดี: "เออ ทำเว็บร้านกาแฟนะ! เจ๋งเลย 😊 เดี๋ยวก่อน อยากได้แบบไหนล่ะ? โทนอบอุ่น ๆ แบบคาเฟ่ในซอย หรือแบบมินิมอลเซียน ๆ? แล้วคนที่มาใช้เว็บส่วนใหญ่เป็นใครเอ่ย?"

ตอบแบบสั้น ๆ กระชับ และถามทีละ 1-2 คำถาม ไม่ทิ้งระเบิดคำถาม
ใช้อีโมจิประกอบเล็กน้อย และใช้ภาษาไทยแบบเป็นธรรมชาติ
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": conversation_prompt}],
                temperature=0.8  # ให้คุยแบบ creative กว่า
            )
            
            conversational_response = response.choices[0].message.content
            log_agent_action("ConversationalAgent", "สร้างคำตอบเสร็จ")
            
            return conversational_response
            
        except Exception as e:
            log_agent_action("ConversationalAgent", f"Error สร้างคำตอบ: {str(e)}")
            return "เอ๊ะ เกิดปัญหาขึ้นนิดหน่อย 😅 ช่วยลองพิมพ์ใหม่ให้หน่อยได้มั้ย?"
    
    def _extract_project_info(self, message: str) -> Dict:
        """สกัดข้อมูล project จากข้อความ"""
        info = {}
        message_lower = message.lower()
        
        # ประเภทเว็บไซต์/แอป
        if any(word in message_lower for word in ['ร้านกาแฟ', 'คาเฟ่', 'coffee', 'cafe']):
            info['project_type'] = 'ร้านกาแฟ'
        elif any(word in message_lower for word in ['ร้านอาหาร', 'restaurant']):
            info['project_type'] = 'ร้านอาหาร'
        elif any(word in message_lower for word in ['โรงแรม', 'hotel']):
            info['project_type'] = 'โรงแรม'
        elif any(word in message_lower for word in ['shop', 'ร้านค้า', 'ecommerce']):
            info['project_type'] = 'ร้านค้าออนไลน์'
        
        # สี
        colors = {
            'แดง': 'red', 'น้ำเงิน': 'blue', 'เขียว': 'green', 
            'เหลือง': 'yellow', 'ม่วง': 'purple', 'ส้ม': 'orange',
            'ขาว': 'white', 'ดำ': 'black', 'เทา': 'gray'
        }
        for thai_color, eng_color in colors.items():
            if thai_color in message or eng_color in message_lower:
                info['color_theme'] = thai_color
                break
        
        # สไตล์
        if any(word in message_lower for word in ['โมเดิร์น', 'modern', 'เซียน']):
            info['style'] = 'โมเดิร์น'
        elif any(word in message_lower for word in ['อบอุ่น', 'cozy', 'คลาสสิก']):
            info['style'] = 'อบอุ่น'
        elif any(word in message_lower for word in ['มินิมอล', 'minimal', 'เรียบ']):
            info['style'] = 'มินิมอล'
        
        return info
    
    def _build_context(self, conversation_history: List) -> str:
        """สร้าง context จากประวัติการสนทนา"""
        if not conversation_history:
            return "ยังไม่มีประวัติการสนทนา"
        
        context_lines = []
        for msg in conversation_history[-5:]:  # เอาแค่ 5 ข้อความล่าสุด
            role = "ผู้ใช้" if msg.get('role') == 'user' else "AI"
            content = msg.get('content', '')[:100]  # จำกัดความยาว
            context_lines.append(f"{role}: {content}")
        
        return "\n".join(context_lines)
    
    def should_proceed_with_development(self) -> bool:
        """ตัดสินใจว่าควรเริ่มพัฒนาหรือยัง"""
        required_info = ['project_type']
        optional_info = ['color_theme', 'style', 'target_audience']
        
        # ต้องมีข้อมูลพื้นฐาน
        has_required = all(key in self.project_context for key in required_info)
        
        # หรือมีข้อมูลเสริมอย่างน้อย 1 อย่าง
        has_optional = any(key in self.project_context for key in optional_info)
        
        confidence = (len(self.project_context) / (len(required_info) + len(optional_info))) * 100
        
        log_agent_action("ConversationalAgent", f"ตรวจสอบข้อมูล - confidence: {confidence:.1f}%", {
            "has_required": has_required,
            "has_optional": has_optional,
            "project_context": self.project_context
        })
        
        return has_required and (has_optional or confidence >= 60)
    
    def get_development_brief(self) -> Dict:
        """สร้าง brief สำหรับทีมพัฒนา"""
        return {
            "project_context": self.project_context,
            "timestamp": datetime.now().isoformat(),
            "confidence_level": (len(self.project_context) / 5) * 100,
            "ready_for_development": self.should_proceed_with_development()
        }