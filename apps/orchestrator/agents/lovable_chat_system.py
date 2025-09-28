"""
🤖 AI Chat System แบบ Lovable - สำหรับสร้าง Apps ซับซ้อน
ระบบ AI ที่คุยโฟกัสเรื่องการสร้าง applications ทุกระดับความซับซ้อน
"""
import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import openai
from datetime import datetime

class AppComplexity(Enum):
    SIMPLE = "simple"           # หน้าเดียว, ฟีเจอร์พื้นฐาน
    MODERATE = "moderate"       # หลายหน้า, database, API
    COMPLEX = "complex"         # Microservices, advanced features
    ENTERPRISE = "enterprise"   # Distributed, scalable, security

class AppCategory(Enum):
    SOCIAL_MEDIA = "social_media"
    ECOMMERCE = "ecommerce" 
    PRODUCTIVITY = "productivity"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    FINTECH = "fintech"
    IOT = "iot"
    AI_ML = "ai_ml"
    BLOCKCHAIN = "blockchain"

@dataclass
class AppRequirement:
    """ข้อมูลความต้องการของ app"""
    name: str
    category: AppCategory
    complexity: AppComplexity
    platforms: List[str]  # web, mobile, desktop
    key_features: List[str]
    target_users: str
    business_model: str
    tech_preferences: List[str] = None
    performance_needs: Dict = None
    security_level: str = "standard"
    scalability_needs: str = "medium"
    timeline: str = None
    budget_range: str = None

class LovableAIChatSystem:
    """AI Chat System ที่โฟกัสการสร้าง Apps แบบ Lovable"""
    
    def __init__(self, openai_api_key: str = None):
        if openai_api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
        else:
            self.openai_client = None
        self.conversation_history = []
        self.current_app_context = None
        self.app_templates = self._initialize_app_templates()
        self.complexity_patterns = self._initialize_complexity_patterns()
        
    def _initialize_app_templates(self) -> Dict:
        """เริ่มต้น templates สำหรับ apps แต่ละประเภท"""
        return {
            AppCategory.SOCIAL_MEDIA: {
                "simple": {
                    "features": ["user_profiles", "posts", "comments", "likes"],
                    "tech_stack": ["React", "Firebase", "React Native"],
                    "components": ["feed", "profile", "chat"]
                },
                "complex": {
                    "features": ["real_time_messaging", "video_calls", "AI_recommendations", "content_moderation"],
                    "tech_stack": ["React", "Node.js", "WebRTC", "AI/ML", "Microservices"],
                    "components": ["advanced_feed", "video_system", "ai_engine", "moderation_system"]
                }
            },
            AppCategory.ECOMMERCE: {
                "simple": {
                    "features": ["product_catalog", "shopping_cart", "checkout", "payments"],
                    "tech_stack": ["React", "Stripe", "MongoDB"],
                    "components": ["product_grid", "cart", "payment_form"]
                },
                "complex": {
                    "features": ["inventory_management", "recommendation_engine", "multi_vendor", "analytics"],
                    "tech_stack": ["Microservices", "AI/ML", "Data Analytics", "Multi-region"],
                    "components": ["inventory_system", "recommendation_ai", "vendor_portal", "analytics_dashboard"]
                }
            },
            AppCategory.FINTECH: {
                "simple": {
                    "features": ["account_management", "transactions", "balance_tracking"],
                    "tech_stack": ["React", "Secure APIs", "Encryption"],
                    "components": ["account_dashboard", "transaction_history"]
                },
                "complex": {
                    "features": ["algorithmic_trading", "fraud_detection", "compliance", "multi_currency"],
                    "tech_stack": ["High-frequency systems", "ML/AI", "Blockchain", "Regulatory compliance"],
                    "components": ["trading_engine", "fraud_ai", "compliance_system", "currency_exchange"]
                }
            }
        }
    
    def _initialize_complexity_patterns(self) -> Dict:
        """เริ่มต้น patterns สำหรับแต่ละระดับความซับซ้อน"""
        return {
            AppComplexity.SIMPLE: {
                "architecture": "Monolith",
                "database": "Single database",
                "deployment": "Single server",
                "team_size": "1-2 developers",
                "timeline": "2-8 weeks",
                "technologies": ["React/Vue", "Node.js/Python", "SQLite/MongoDB"],
                "complexity_score": 1
            },
            AppComplexity.MODERATE: {
                "architecture": "Layered architecture",
                "database": "Primary + Cache",
                "deployment": "Load balanced",
                "team_size": "3-5 developers", 
                "timeline": "2-4 months",
                "technologies": ["React/Vue", "API Gateway", "PostgreSQL", "Redis"],
                "complexity_score": 3
            },
            AppComplexity.COMPLEX: {
                "architecture": "Microservices",
                "database": "Multiple databases",
                "deployment": "Container orchestration", 
                "team_size": "5-10 developers",
                "timeline": "4-8 months",
                "technologies": ["React/Angular", "Microservices", "Kubernetes", "Event Sourcing"],
                "complexity_score": 7
            },
            AppComplexity.ENTERPRISE: {
                "architecture": "Distributed systems",
                "database": "Multi-region, CQRS",
                "deployment": "Multi-cloud, Auto-scaling",
                "team_size": "10+ developers",
                "timeline": "8+ months", 
                "technologies": ["Enterprise frameworks", "Service mesh", "Event streaming", "AI/ML"],
                "complexity_score": 10
            }
        }
    
    async def chat(self, user_message: str, context: Dict = None) -> Dict[str, Any]:
        """หลัก method สำหรับคุยกับ AI"""
        try:
            # วิเคราะห์ user intent
            intent = await self._analyze_user_intent(user_message)
            
            # เพิ่มข้อความใน conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_message,
                "intent": intent
            })
            
            # สร้าง response ตาม intent
            if intent["type"] == "app_idea":
                response = await self._handle_app_idea_discussion(user_message, intent)
            elif intent["type"] == "technical_question":
                response = await self._handle_technical_question(user_message, intent)
            elif intent["type"] == "complexity_analysis":
                response = await self._handle_complexity_analysis(user_message, intent)
            elif intent["type"] == "architecture_design":
                response = await self._handle_architecture_design(user_message, intent)
            elif intent["type"] == "implementation_help":
                response = await self._handle_implementation_help(user_message, intent)
            else:
                response = await self._handle_general_chat(user_message, intent)
            
            # เพิ่ม AI response ใน history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "ai": response["message"],
                "suggestions": response.get("suggestions", []),
                "generated_content": response.get("generated_content")
            })
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "message": "ขออภัย เกิดข้อผิดพลาดในการประมวลผล",
                "error": str(e)
            }
    
    async def _analyze_user_intent(self, message: str) -> Dict:
        """วิเคราะห์ความตั้งใจของผู้ใช้"""
        
        # Keywords สำหรับแต่ละประเภท intent
        intent_keywords = {
            "app_idea": ["สร้างแอป", "ทำแอป", "app ใหม่", "ไอเดียแอป", "แอปพลิเคชัน"],
            "technical_question": ["เทคนิค", "โค้ด", "ภาษา", "framework", "database", "API"],
            "complexity_analysis": ["ซับซ้อน", "ยาก", "enterprise", "scalable", "performance"],
            "architecture_design": ["สถาปัตยกรรม", "architecture", "microservice", "system design"],
            "implementation_help": ["ช่วยทำ", "สร้างให้", "generate", "implement", "เริ่มต้น"]
        }
        
        message_lower = message.lower()
        detected_intents = []
        
        for intent_type, keywords in intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_intents.append(intent_type)
        
        # ใช้ AI เพื่อวิเคราะห์เพิ่มเติม
        ai_analysis = await self._get_ai_intent_analysis(message)
        
        return {
            "type": detected_intents[0] if detected_intents else "general_chat",
            "confidence": len(detected_intents) / len(intent_keywords),
            "detected_intents": detected_intents,
            "ai_analysis": ai_analysis,
            "entities": await self._extract_entities(message)
        }
    
    async def _get_ai_intent_analysis(self, message: str) -> Dict:
        """ใช้ AI วิเคราะห์ intent เพิ่มเติม"""
        
        system_prompt = """
        คุณเป็น AI ที่เชี่ยวชาญในการวิเคราะห์ความต้องการสร้าง applications
        วิเคราะห์ข้อความและบอก:
        1. ประเภทของ app ที่ผู้ใช้สนใจ
        2. ระดับความซับซ้อน
        3. เทคโนโลยีที่เกี่ยวข้อง
        4. ข้อแนะนำเพิ่มเติม
        
        ตอบเป็น JSON format เท่านั้น
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"วิเคราะห์: {message}"}
                ],
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except:
            return {"app_type": "unknown", "complexity": "unknown"}
    
    async def _extract_entities(self, message: str) -> Dict:
        """สกัดข้อมูลสำคัญจากข้อความ"""
        entities = {
            "app_names": [],
            "technologies": [],
            "platforms": [],
            "features": [],
            "business_domains": []
        }
        
        # Technology keywords
        tech_keywords = {
            "web": ["react", "vue", "angular", "nextjs", "web", "website"],
            "mobile": ["react native", "flutter", "mobile", "app", "ios", "android"],
            "backend": ["nodejs", "python", "fastapi", "express", "api"],
            "database": ["mongodb", "postgresql", "mysql", "firebase", "redis"],
            "ai_ml": ["ai", "machine learning", "ml", "chatbot", "recommendation"]
        }
        
        message_lower = message.lower()
        for category, keywords in tech_keywords.items():
            found_techs = [keyword for keyword in keywords if keyword in message_lower]
            if found_techs:
                entities["technologies"].extend(found_techs)
        
        return entities
    
    async def _handle_app_idea_discussion(self, message: str, intent: Dict) -> Dict:
        """จัดการการคุยเรื่องไอเดีย app"""
        
        # สร้าง response ที่โฟกัสการสร้าง app
        system_prompt = f"""
        คุณเป็น AI ผู้เชี่ยวชาญในการสร้าง applications ทุกประเภท
        
        ให้คุยกับผู้ใช้เกี่ยวกับไอเดีย app โดยโฟกัส:
        1. วิเคราะห์ความต้องการอย่างลึกซึ้ง  
        2. แนะนำเทคโนโลยีที่เหมาะสม
        3. ประเมินความซับซ้อน
        4. เสนอ features ที่น่าสนใจ
        5. วางแผนการพัฒนา
        
        ตอบแบบเป็นมิตร มีประโยชน์ และกระตุ้นให้คิดเพิ่มเติม
        
        Context: {intent}
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7
            )
            
            ai_message = response.choices[0].message.content
            
            # สร้าง suggestions
            suggestions = await self._generate_app_suggestions(intent)
            
            return {
                "success": True,
                "message": ai_message,
                "suggestions": suggestions,
                "follow_up_questions": await self._generate_follow_up_questions(intent),
                "quick_actions": [
                    {"text": "วิเคราะห์ความซับซ้อน", "action": "analyze_complexity"},
                    {"text": "แนะนำเทคโนโลยี", "action": "suggest_tech"},
                    {"text": "เริ่มสร้าง prototype", "action": "start_prototype"}
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "ขออภัย ไม่สามารถประมวลผลได้ในขณะนี้",
                "error": str(e)
            }
    
    async def _handle_complexity_analysis(self, message: str, intent: Dict) -> Dict:
        """วิเคราะห์ความซับซ้อนของ app"""
        
        # ใช้ AI วิเคราะห์ความซับซ้อน
        complexity_prompt = f"""
        วิเคราะห์ความซับซ้อนของ application ตามข้อความ: {message}
        
        ให้ประเมินใน 4 ระดับ:
        1. SIMPLE - app พื้นฐาน 1-2 features
        2. MODERATE - app ที่มี database, API, หลาย features  
        3. COMPLEX - app ที่ต้องใช้ microservices, advanced features
        4. ENTERPRISE - distributed system, scalable, security สูง
        
        ตอบเป็น JSON ที่มี:
        - complexity_level
        - reasoning  
        - technical_requirements
        - estimated_timeline
        - team_size_needed
        - key_challenges
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": complexity_prompt}
                ],
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            complexity_level = AppComplexity(analysis["complexity_level"].lower())
            
            # เพิ่มข้อมูลจาก patterns
            pattern_info = self.complexity_patterns[complexity_level]
            
            return {
                "success": True,
                "message": f"📊 **วิเคราะห์ความซับซ้อน: {complexity_level.value.upper()}**\n\n" +
                          f"**เหตุผล:** {analysis['reasoning']}\n\n" +
                          f"**ความต้องการทางเทคนิค:** {analysis['technical_requirements']}\n\n" +
                          f"**ประมาณเวลา:** {analysis['estimated_timeline']}\n\n" +
                          f"**ขนาดทีม:** {analysis['team_size_needed']}\n\n" +
                          f"**ความท้าทาย:** {analysis['key_challenges']}",
                "analysis": analysis,
                "pattern_info": pattern_info,
                "complexity_score": pattern_info["complexity_score"],
                "quick_actions": [
                    {"text": "ดูสถาปัตยกรรมแนะนำ", "action": "show_architecture"},
                    {"text": "แนะนำเทคโนโลยี", "action": "suggest_tech_stack"},
                    {"text": "สร้าง prototype", "action": "create_prototype"}
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "ไม่สามารถวิเคราะห์ความซับซ้อนได้",
                "error": str(e)
            }
    
    async def _handle_architecture_design(self, message: str, intent: Dict) -> Dict:
        """ออกแบบสถาปัตยกรรมของ app"""
        
        architecture_prompt = f"""
        ออกแบบสถาปัตยกรรม application สำหรับ: {message}
        
        ให้ครอบคลุม:
        1. System Architecture (monolith/microservices/serverless)
        2. Database Design (รวม schema หลัก)
        3. API Design (endpoints สำคัญ)
        4. Security Architecture
        5. Scalability Strategy
        6. Technology Stack แนะนำ
        7. Deployment Architecture
        
        ตอบเป็น JSON ที่มีรายละเอียดครบถ้วน
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": architecture_prompt}
                ],
                temperature=0.4
            )
            
            architecture = json.loads(response.choices[0].message.content)
            
            # สร้าง visual representation
            visual_arch = await self._create_architecture_visual(architecture)
            
            return {
                "success": True,
                "message": "🏗️ **สถาปัตยกรรม Application**\n\n" +
                          self._format_architecture_response(architecture),
                "architecture": architecture,
                "visual": visual_arch,
                "generated_content": {
                    "database_schema": architecture.get("database_design"),
                    "api_endpoints": architecture.get("api_design"),
                    "tech_stack": architecture.get("technology_stack")
                },
                "quick_actions": [
                    {"text": "สร้างโค้ด prototype", "action": "generate_code"},
                    {"text": "สร้าง database schema", "action": "create_database"},
                    {"text": "วิเคราะห์ cost", "action": "analyze_cost"}
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "ไม่สามารถออกแบบสถาปัตยกรรมได้",
                "error": str(e)
            }
    
    async def _handle_implementation_help(self, message: str, intent: Dict) -> Dict:
        """ช่วยในการ implement"""
        
        # ถ้ามี current_app_context ใช้เป็นข้อมูลเพิ่มเติม
        context_info = ""
        if self.current_app_context:
            context_info = f"App context: {json.dumps(asdict(self.current_app_context), indent=2)}"
        
        implementation_prompt = f"""
        ช่วยการ implement application ตามคำขอ: {message}
        
        {context_info}
        
        ให้:
        1. สร้างโค้ดตัวอย่างที่ใช้งานได้จริง
        2. อธิบาย step-by-step
        3. แนะนำ best practices
        4. ระบุ dependencies ที่ต้องติดตั้ง
        5. ให้คำแนะนำการ deploy
        
        โฟกัสที่การสร้าง production-ready code
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": implementation_prompt}
                ],
                temperature=0.3
            )
            
            implementation_guide = response.choices[0].message.content
            
            # สร้างโค้ดตัวอย่าง
            code_examples = await self._generate_code_examples(message, intent)
            
            return {
                "success": True,
                "message": implementation_guide,
                "generated_content": {
                    "code_examples": code_examples,
                    "implementation_steps": await self._extract_implementation_steps(implementation_guide)
                },
                "quick_actions": [
                    {"text": "สร้างโปรเจกต์เต็ม", "action": "create_full_project"},
                    {"text": "ทดสอบโค้ด", "action": "test_code"},
                    {"text": "deploy app", "action": "deploy_app"}
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "ไม่สามารถช่วยการ implement ได้",
                "error": str(e)
            }
    
    async def create_app_from_conversation(self) -> Dict:
        """สร้าง app จากการสนทนาที่ผ่านมา"""
        
        if not self.conversation_history:
            return {
                "success": False,
                "message": "ยังไม่มีการสนทนาเกี่ยวกับ app"
            }
        
        # รวมข้อมูลจากการสนทนา
        conversation_summary = await self._summarize_conversation()
        
        # สร้าง AppRequirement
        app_req = await self._extract_app_requirements(conversation_summary)
        
        # สร้าง app ตาม requirements
        return await self._generate_complete_app(app_req)
    
    def _format_architecture_response(self, architecture: Dict) -> str:
        """จัดรูปแบบ response สถาปัตยกรรม"""
        formatted = f"**System Type:** {architecture.get('system_architecture', 'N/A')}\n\n"
        
        if architecture.get('database_design'):
            formatted += f"**Database:** {architecture['database_design']}\n\n"
            
        if architecture.get('technology_stack'):
            formatted += f"**Tech Stack:** {', '.join(architecture['technology_stack'])}\n\n"
            
        if architecture.get('scalability_strategy'):
            formatted += f"**Scalability:** {architecture['scalability_strategy']}\n\n"
            
        return formatted
    
    async def _generate_app_suggestions(self, intent: Dict) -> List[str]:
        """สร้าง suggestions สำหรับ app"""
        return [
            "💡 เพิ่ม AI features เพื่อความน่าสนใจ",
            "📱 ทำ mobile app ควบคู่ไปด้วย", 
            "🔄 เพิ่ม real-time features",
            "🛡️ ออกแบบ security ที่แข็งแกร่ง",
            "📈 วางแผน scalability ตั้งแต่เริ่มต้น"
        ]
    
    async def _generate_follow_up_questions(self, intent: Dict) -> List[str]:
        """สร้างคำถามติดตาม"""
        return [
            "ใครคือ target users หลักของ app นี้?",
            "คุณต้องการ app นี้รองรับกี่คนใช้พร้อมกัน?",
            "มี budget หรือข้อจำกัดด้านเทคโนโลยีไหม?",
            "ต้องการ launch เมื่อไหร่?",
            "มีแผนทำเงินจาก app นี้อย่างไร?"
        ]

# สร้าง instance
def create_lovable_chat_system(openai_api_key: str) -> LovableAIChatSystem:
    """สร้าง LovableAIChatSystem instance"""
    return LovableAIChatSystem(openai_api_key)

# Helper functions
async def demo_complex_app_chat():
    """ตัวอย่างการใช้งานสำหรับ complex apps"""
    
    print("🚀 Lovable AI Chat System - สร้าง Apps ซับซ้อน")
    print("=" * 50)
    
    # ตัวอย่าง conversations
    sample_conversations = [
        "ผมอยากสร้าง social media app แบบ Instagram แต่เพิ่ม AI ที่แนะนำเพื่อนตามความสนใจ",
        "ทำ e-commerce platform ที่รองรับ multi-vendor และมี ML recommendation engine",
        "สร้าง fintech app สำหรับ trading cryptocurrency ด้วย algorithmic trading",
        "ผมต้องการ IoT platform ที่เชื่อม smart devices และ analyze data real-time",
        "อยากทำ enterprise CRM ที่มี AI chatbot และ advanced analytics"
    ]
    
    for i, conv in enumerate(sample_conversations, 1):
        print(f"\n{i}. {conv}")
    
    print("\n✨ ระบบนี้สามารถ:")
    print("📊 วิเคราะห์ความซับซ้อน และแนะนำสถาปัตยกรรม")
    print("🛠️ สร้างโค้ด และ database schema")
    print("🚀 ออกแบบ deployment strategy")
    print("💡 แนะนำ advanced features")
    print("🔒 วางแผน security และ scalability")

if __name__ == "__main__":
    asyncio.run(demo_complex_app_chat())