"""
🎭 Advanced Conversational AI - คุยไหลลื่นเหมือน Lovable
"""

from openai import AsyncOpenAI
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import re

class ConversationalFlowManager:
    def __init__(self):
        self.client = AsyncOpenAI()
        self.conversation_memory = {}
        self.user_preferences = {}
        self.project_context = {}
        
        # Personality โดยรอบ
        self.ai_personality = {
            "tone": "friendly_professional",
            "style": "conversational", 
            "expertise": "web_development",
            "empathy_level": "high",
            "proactivity": "very_high"
        }
        
    async def process_conversation(self, user_id: str, message: str, context: Dict = None) -> Dict[str, Any]:
        """ประมวลผลการสนทนาแบบไหลลื่น"""
        
        # บันทึกข้อความใน Memory
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
            
        self.conversation_memory[user_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now()
        })
        
        # วิเคราะห์ Intent และ Context
        intent_analysis = await self._analyze_user_intent(message, user_id)
        
        # สร้าง Response ที่เหมาะสม
        response_data = await self._generate_contextual_response(
            user_id, message, intent_analysis, context
        )
        
        # บันทึก AI Response
        self.conversation_memory[user_id].append({
            "role": "assistant", 
            "content": response_data["message"],
            "timestamp": datetime.now(),
            "intent": intent_analysis,
            "actions": response_data.get("actions", [])
        })
        
        return response_data
    
    async def _analyze_user_intent(self, message: str, user_id: str) -> Dict[str, Any]:
        """วิเคราะห์เจตนาของผู้ใช้อย่างละเอียด"""
        
        conversation_history = self._get_conversation_context(user_id)
        
        analysis_prompt = f"""
        วิเคราะห์ข้อความของผู้ใช้อย่างละเอียด:
        
        ข้อความปัจจุบัน: "{message}"
        
        ประวัติการสนทนา: {conversation_history}
        
        กรุณาวิเคราะห์:
        1. เจตนาหลัก (primary_intent)
        2. เจตนารอง (secondary_intents) 
        3. ความชัดเจนของข้อมูล (clarity_level: 1-10)
        4. ข้อมูลที่ขาดหายไป (missing_information)
        5. อารมณ์/โทนเสียง (emotional_tone)
        6. ความเร่งด่วน (urgency_level: 1-10)
        7. ประเภทโปรเจ็กต์ (project_type)
        8. ความซับซ้อน (complexity_level: 1-10)
        
        ตอบกลับในรูปแบบ JSON:
        {{
            "primary_intent": "create_website|ask_question|modify_request|get_status|other",
            "secondary_intents": [],
            "clarity_level": 0,
            "missing_information": [],
            "emotional_tone": "excited|neutral|frustrated|confused|urgent",
            "urgency_level": 0,
            "project_type": "website|app|landing_page|ecommerce|portfolio|other",
            "complexity_level": 0,
            "confidence_score": 0.0
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.1
            )
            
            analysis_text = response.choices[0].message.content
            # Extract JSON จาก response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
                
        except Exception as e:
            print(f"Intent analysis error: {e}")
            
        # Fallback analysis
        return {
            "primary_intent": "create_website" if any(word in message.lower() for word in ["สร้าง", "ทำ", "create", "build"]) else "ask_question",
            "clarity_level": 7,
            "emotional_tone": "neutral",
            "urgency_level": 5,
            "project_type": "website",
            "complexity_level": 5,
            "confidence_score": 0.6
        }
    
    async def _generate_contextual_response(self, user_id: str, message: str, intent: Dict, context: Dict = None) -> Dict[str, Any]:
        """สร้าง Response ที่เหมาะสมตาม Context"""
        
        conversation_history = self._get_conversation_context(user_id, last_n=5)
        
        # สร้าง System Prompt ที่ดี
        system_prompt = self._create_system_prompt(intent, context)
        
        # สร้าง Response แบบไหลลื่น
        response_data = await self._generate_natural_response(
            system_prompt, message, conversation_history, intent
        )
        
        # ตรวจสอบว่าควร Trigger Actions ไหม
        if intent["primary_intent"] == "create_website" and intent["clarity_level"] >= 7:
            response_data["should_start_workflow"] = True
            response_data["workflow_params"] = {
                "user_request": message,
                "project_type": intent.get("project_type", "website"),
                "complexity": intent.get("complexity_level", 5),
                "urgency": intent.get("urgency_level", 5)
            }
        
        return response_data
    
    def _create_system_prompt(self, intent: Dict, context: Dict = None) -> str:
        """สร้าง System Prompt ที่เหมาะสม"""
        
        base_personality = """
        คุณเป็น AI Assistant ที่เชี่ยวชาญด้านการพัฒนาเว็บไซต์ มีบุคลิกดังนี้:
        - คุยแบบเป็นกันเองและเข้าใจง่าย
        - ตอบโต้อย่างไหลลื่นและธรรมชาติ  
        - ถามคำถามเพิ่มเติมอย่างชาญฉลาด
        - ให้คำแนะนำที่มีประโยชน์
        - แสดงความเข้าใจและเอาใจใส่
        """
        
        if intent["primary_intent"] == "create_website":
            if intent["clarity_level"] < 6:
                return base_personality + """
                
                ผู้ใช้อยากสร้างเว็บไซต์ แต่ข้อมูลยังไม่ชัดเจน
                กรุณาถามคำถามเพิ่มเติมอย่างฉลาดเพื่อให้ได้ข้อมูลครบถ้วน:
                - ประเภทเว็บไซต์
                - เป้าหมายหลัก  
                - กลุ่มเป้าหมาย
                - สีสันและสไตล์ที่ชอบ
                - ฟีเจอร์พิเศษที่ต้องการ
                
                ถามทีละ 2-3 คำถาม แล้วให้ความรู้สึกว่าคุณเข้าใจและพร้อมช่วยเหลือ
                """
            else:
                return base_personality + """
                
                ผู้ใช้มีข้อมูลชัดเจนแล้ว พร้อมเริ่มสร้างเว็บไซต์
                - แสดงความตื่นเต้นและพร้อม
                - สรุปความเข้าใจ
                - บอกขั้นตอนการทำงาน
                - เริ่มกระบวนการสร้าง
                """
        
        elif intent["emotional_tone"] == "frustrated":
            return base_personality + """
            
            ผู้ใช้ดูท้อใจหรือหงุดหงิด
            - แสดงความเข้าใจและเอาใจใส่
            - ช่วยแก้ปัญหาอย่างอดทน  
            - ให้กำลังใจ
            - เสนอทางเลือกที่เหมาะสม
            """
        
        return base_personality + """
        
        ตอบโต้อย่างเป็นธรรมชาติ ให้ข้อมูลที่เป็นประโยชน์ และพร้อมช่วยเหลือ
        """
    
    async def _generate_natural_response(self, system_prompt: str, message: str, history: str, intent: Dict) -> Dict[str, Any]:
        """สร้าง Response ที่ธรรมชาติและไหลลื่น"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"ประวัติการสนทนา:\n{history}\n\nข้อความใหม่: {message}"}
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            ai_message = response.choices[0].message.content.strip()
            
            return {
                "message": ai_message,
                "intent_detected": intent,
                "response_type": "conversational",
                "confidence": intent.get("confidence_score", 0.8)
            }
            
        except Exception as e:
            print(f"Response generation error: {e}")
            return {
                "message": "ขอโทษครับ เกิดข้อผิดพลาดชั่วคราว ลองใหม่ได้เลยครับ",
                "error": str(e)
            }
    
    def _get_conversation_context(self, user_id: str, last_n: int = 10) -> str:
        """ดึงประวัติการสนทนาย้อนหลัง"""
        
        if user_id not in self.conversation_memory:
            return "ไม่มีประวัติการสนทนา"
        
        recent_messages = self.conversation_memory[user_id][-last_n:]
        
        context_lines = []
        for msg in recent_messages:
            role = "ผู้ใช้" if msg["role"] == "user" else "AI"
            context_lines.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_lines)
    
    def update_user_preferences(self, user_id: str, preferences: Dict):
        """อัพเดตความชอบของผู้ใช้"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        self.user_preferences[user_id].update(preferences)
    
    def get_conversation_summary(self, user_id: str) -> Dict[str, Any]:
        """สรุปการสนทนา"""
        
        if user_id not in self.conversation_memory:
            return {"total_messages": 0, "summary": "ยังไม่มีการสนทนา"}
        
        messages = self.conversation_memory[user_id]
        
        return {
            "total_messages": len(messages),
            "last_conversation": messages[-1]["timestamp"] if messages else None,
            "user_preferences": self.user_preferences.get(user_id, {}),
            "project_context": self.project_context.get(user_id, {})
        }

# Singleton Instance
conversation_flow = ConversationalFlowManager()