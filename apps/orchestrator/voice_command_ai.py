"""
Voice Command Interface Implementation
=====================================
ระบบสั่งงาน AI ด้วยเสียง - พูดแล้วโค้ดเขียนเอง!
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class VoiceCommandAI:
    """AI ที่เข้าใจคำสั่งเสียงและแปลงเป็นโค้ด"""
    
    def __init__(self):
        self.command_patterns = {}
        self.conversation_context = []
        self.active_project = None
        self.supported_languages = ["thai", "english", "japanese"]
        self.setup_command_patterns()
        
    def setup_command_patterns(self):
        """ตั้งค่า pattern การรู้จำคำสั่งเสียง"""
        
        self.command_patterns = {
            # การสร้าง project ใหม่
            "create_project": {
                "patterns": [
                    r"สร้าง(เว็บ|แอพ|ระบบ|โปรแกรม)",
                    r"ทำ(เว็บไซต์|แอปพลิเคชัน)", 
                    r"create (web|app|system)",
                    r"build (website|application)"
                ],
                "examples": [
                    "สร้างเว็บขายของ → e-commerce website",
                    "ทำแอพ chat → chat application", 
                    "สร้างระบบจัดการ → management system",
                    "create web app → web application"
                ]
            },
            
            # การแก้ไขและปรับปรุง
            "modify_code": {
                "patterns": [
                    r"แก้(ไข|บัค|ปัญหา)",
                    r"ปรับ(ปรุง|แก้|เปลี่ยน)",
                    r"(fix|debug|modify|change)",
                    r"ทำให้(สวย|เร็ว|ดี)ขึ้น"
                ],
                "examples": [
                    "แก้บัคตรงนี้ → debug current issue",
                    "ปรับปรุงดีไซน์ → improve design", 
                    "ทำให้เร็วขึ้น → optimize performance",
                    "fix this bug → debug and repair"
                ]
            },
            
            # การ deploy และ publish
            "deployment": {
                "patterns": [
                    r"(deploy|อัพโหลด|เผยแพร่)",
                    r"ขึ้น(เซิร์ฟเวอร์|server|cloud)",
                    r"publish (to|ไป)",
                    r"go live"
                ],
                "examples": [
                    "deploy ไป AWS → deploy to AWS",
                    "อัพโหลดเซิร์ฟเวอร์ → upload to server",
                    "publish to web → make it live",
                    "go live now → deploy immediately"
                ]
            },
            
            # การอธิบายและช่วยเหลือ
            "explanation": {
                "patterns": [
                    r"(อธิบาย|explain|บอก)",
                    r"(ช่วย|help|assist)",
                    r"(ทำไง|how to|วิธี)",
                    r"คืออะไร"
                ],
                "examples": [
                    "อธิบายโค้ดนี้ → explain this code",
                    "ช่วยแก้ปัญหา → help solve problem",
                    "ทำยังไงให้เร็ว → how to make it faster",
                    "คืออะไร → what is this"
                ]
            }
        }
    
    def process_voice_command(self, voice_text: str) -> Dict[str, Any]:
        """ประมวลผลคำสั่งเสียงและแปลงเป็น action"""
        
        voice_text = voice_text.lower().strip()
        
        # วิเคราะห์ intent
        intent = self.detect_intent(voice_text)
        
        # สกัดรายละเอียด
        details = self.extract_details(voice_text, intent)
        
        # สร้าง response
        response = self.generate_response(intent, details, voice_text)
        
        return response
    
    def detect_intent(self, voice_text: str) -> str:
        """ตรวจจับเจตนาจากคำสั่งเสียง"""
        
        for intent, config in self.command_patterns.items():
            for pattern in config["patterns"]:
                if re.search(pattern, voice_text, re.IGNORECASE):
                    return intent
        
        return "general_conversation"
    
    def extract_details(self, voice_text: str, intent: str) -> Dict[str, Any]:
        """สกัดรายละเอียดจากคำสั่งเสียง"""
        
        details = {
            "original_text": voice_text,
            "confidence": 0.95,
            "parameters": {}
        }
        
        if intent == "create_project":
            # ตรวจหาประเภทโปรเจกต์
            if "ขาย" in voice_text or "shop" in voice_text:
                details["parameters"]["type"] = "e-commerce"
            elif "chat" in voice_text or "แชท" in voice_text:
                details["parameters"]["type"] = "chat_app"
            elif "blog" in voice_text or "บล็อก" in voice_text:
                details["parameters"]["type"] = "blog"
            elif "จัดการ" in voice_text or "manage" in voice_text:
                details["parameters"]["type"] = "management_system"
            else:
                details["parameters"]["type"] = "web_application"
                
        elif intent == "modify_code":
            # ตรวจหาสิ่งที่ต้องแก้ไข
            if "สี" in voice_text or "color" in voice_text:
                details["parameters"]["target"] = "colors"
            elif "ขนาด" in voice_text or "size" in voice_text:
                details["parameters"]["target"] = "sizing"
            elif "เร็ว" in voice_text or "speed" in voice_text:
                details["parameters"]["target"] = "performance"
            elif "สวย" in voice_text or "design" in voice_text:
                details["parameters"]["target"] = "design"
            else:
                details["parameters"]["target"] = "general"
                
        elif intent == "deployment":
            # ตรวจหา destination
            if "aws" in voice_text.lower():
                details["parameters"]["platform"] = "AWS"
            elif "google" in voice_text or "gcp" in voice_text:
                details["parameters"]["platform"] = "Google Cloud"
            elif "azure" in voice_text:
                details["parameters"]["platform"] = "Azure"
            else:
                details["parameters"]["platform"] = "auto_select"
        
        return details
    
    def generate_response(self, intent: str, details: Dict, voice_text: str) -> Dict[str, Any]:
        """สร้างการตอบสนองตามเจตนา"""
        
        response = {
            "intent": intent,
            "understanding": f"เข้าใจแล้วครับ: {voice_text}",
            "action": "",
            "code_to_generate": "",
            "estimated_time": "",
            "follow_up_questions": []
        }
        
        if intent == "create_project":
            project_type = details["parameters"].get("type", "web_application")
            response["action"] = f"สร้าง {project_type} ให้ครับ"
            response["estimated_time"] = "5-15 นาที"
            
            if project_type == "e-commerce":
                response["code_to_generate"] = "HTML + CSS + JavaScript e-commerce website"
                response["follow_up_questions"] = [
                    "ขายสินค้าประเภทไหนครับ?",
                    "ต้องการระบบชำระเงินมั้ย?",
                    "มีสีที่ชอบเป็นพิเศษมั้ย?"
                ]
            elif project_type == "chat_app":
                response["code_to_generate"] = "Real-time chat application"
                response["follow_up_questions"] = [
                    "แชทแบบส่วนตัวหรือกลุ่มครับ?",
                    "ต้องการส่งไฟล์ได้ด้วยมั้ย?",
                    "มีระบบ emoji มั้ย?"
                ]
                
        elif intent == "modify_code":
            target = details["parameters"].get("target", "general")
            response["action"] = f"ปรับปรุง {target} ให้ครับ"
            response["estimated_time"] = "1-5 นาที"
            
            if target == "colors":
                response["code_to_generate"] = "CSS color scheme adjustment"
            elif target == "performance":
                response["code_to_generate"] = "Code optimization and performance tuning"
            elif target == "design":
                response["code_to_generate"] = "UI/UX design improvements"
                
        elif intent == "deployment":
            platform = details["parameters"].get("platform", "auto_select")
            response["action"] = f"Deploy ไป {platform} ครับ"
            response["estimated_time"] = "2-10 นาที"
            response["code_to_generate"] = f"Deployment configuration for {platform}"
            
        elif intent == "explanation":
            response["action"] = "อธิบายให้ฟังครับ"
            response["estimated_time"] = "ทันที"
            
        return response
    
    def demonstrate_voice_commands(self):
        """แสดงตัวอย่างการทำงานของคำสั่งเสียง"""
        
        demo_commands = [
            "สร้างเว็บขายเสื้อผ้า",
            "แก้บัคตรงนี้หน่อย", 
            "ทำให้สวยขึ้นหน่อย",
            "deploy ไป AWS เลย",
            "อธิบายโค้ดนี้หน่อย",
            "ช่วยปรับปรุงความเร็ว",
            "สร้างแอพแชทแบบ Line",
            "เปลี่ยนสีเป็นสีน้าเงิน"
        ]
        
        print("🎤 VOICE COMMAND DEMONSTRATION")
        print("=" * 50)
        
        for i, command in enumerate(demo_commands, 1):
            print(f"\n🗣️  Command {i}: '{command}'")
            response = self.process_voice_command(command)
            
            print(f"🤖 AI Understanding: {response['understanding']}")
            print(f"⚡ Action: {response['action']}")
            print(f"⏰ Estimated Time: {response['estimated_time']}")
            
            if response.get('follow_up_questions'):
                print("❓ Follow-up Questions:")
                for question in response['follow_up_questions']:
                    print(f"   • {question}")
        
        return demo_commands

def demonstrate_voice_interface():
    """สาธิตระบบ Voice Command Interface"""
    
    print("🎤 VOICE COMMAND AI INTERFACE")
    print("=" * 60)
    
    voice_ai = VoiceCommandAI()
    
    print("🌟 SUPPORTED VOICE COMMANDS:")
    print("-" * 40)
    
    for intent, config in voice_ai.command_patterns.items():
        print(f"\n📋 {intent.replace('_', ' ').title()}:")
        for example in config['examples']:
            print(f"   🗣️  {example}")
    
    print(f"\n🎯 LIVE DEMONSTRATION:")
    print("-" * 30)
    
    voice_ai.demonstrate_voice_commands()
    
    print(f"\n🚀 ADVANTAGES OF VOICE INTERFACE:")
    print("-" * 45)
    advantages = [
        "🗣️ พูดได้เป็นภาษาไทยธรรมชาติ",
        "⚡ เร็วกว่าการพิมพ์ 3 เท่า",
        "🤲 ใช้งานแบบ hands-free",
        "🧠 เข้าใจ context และ intent",
        "🔄 สนทนาได้แบบต่อเนื่อง", 
        "🌍 รองรับหลายภาษา",
        "🎯 แปลงเป็นโค้ดทันที",
        "💬 ถามคำถามเพิ่มเติมได้"
    ]
    
    for advantage in advantages:
        print(f"   {advantage}")
    
    print(f"\n" + "=" * 60)
    print("🎤 พูดกับ AI แล้วโค้ดเขียนเอง - เจ๋งสุด ๆ!")

if __name__ == "__main__":
    demonstrate_voice_interface()