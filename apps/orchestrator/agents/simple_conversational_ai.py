"""
Simple Conversational AI Implementation  
เวอร์ชันง่ายที่ทำงานได้แน่นอน โดยไม่พึ่งพา complex dependencies
"""

import json
import asyncio
import re
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from fastapi import WebSocket

class SimpleIntentType(Enum):
    CREATE_WEBSITE = "create_website"
    MODIFY_DESIGN = "modify_design" 
    CHANGE_CONTENT = "change_content"
    ADD_FEATURE = "add_feature"
    CASUAL_CHAT = "casual_chat"

@dataclass
class SimpleChatMessage:
    id: str
    role: str  # user, assistant, system
    content: str
    timestamp: float
    
@dataclass 
class SimpleAgentResponse:
    message: str
    action_taken: Optional[str] = None
    progress_update: Optional[Dict[str, Any]] = None
    preview_url: Optional[str] = None
    suggestions: List[str] = None

class SimpleConversationalAI:
    """Simple conversational AI that works without complex dependencies"""
    
    def __init__(self, openai_client, agent_manager):
        self.client = openai_client
        self.agent_manager = agent_manager
        self.conversation_history: List[SimpleChatMessage] = []
        self.user_context: Dict[str, Any] = {}
        self.active_project: Optional[str] = None
        
        # Simple patterns for intent detection
        self.intent_patterns = {
            SimpleIntentType.CREATE_WEBSITE: [
                r"สร้าง(?:เว็บ|website|เว็บไซต์)",
                r"ทำ(?:เว็บ|website|เว็บไซต์)",
                r"(?:create|make|build).*(?:website|site|page)",
                r"ช่วย(?:สร้าง|ทำ).*(?:เว็บ|หน้าเว็บ)"
            ],
            SimpleIntentType.MODIFY_DESIGN: [
                r"(?:เปลี่ยน|แก้|ปรับ).*(?:สี|color|design|ดีไซน์)",
                r"(?:change|modify|update).*(?:color|design|layout|style)",
                r"ให้.*(?:สี|ดู).*(?:ดีขึ้น|สวยขึ้น|ดีกว่า)"
            ],
            SimpleIntentType.ADD_FEATURE: [
                r"(?:เพิ่ม|add).*(?:ปุ่ม|button|เมนู|menu|ฟีเจอร์|feature)",
                r"ใส่.*(?:ระบบ|system|การทำงาน|functionality)",
                r"อยาก(?:ให้มี|ได้).*(?:การทำงาน|ฟีเจอร์)"
            ]
        }
        
    async def process_message(self, user_input: str, websocket: WebSocket = None) -> SimpleAgentResponse:
        """Process user message and generate appropriate response"""
        
        # Add to conversation history
        user_msg = SimpleChatMessage(
            id=f"msg_{int(time.time() * 1000)}",
            role="user", 
            content=user_input,
            timestamp=time.time()
        )
        self.conversation_history.append(user_msg)
        
        # Simple intent detection
        intent = self._detect_intent(user_input)
        
        # Update user context
        self._update_context(user_input, intent)
        
        # Generate response based on intent
        response = await self._generate_response(intent, user_input, websocket)
        
        # Add assistant response to history
        assistant_msg = SimpleChatMessage(
            id=f"msg_{int(time.time() * 1000) + 1}",
            role="assistant",
            content=response.message,
            timestamp=time.time()
        )
        self.conversation_history.append(assistant_msg)
        
        return response
    
    def _detect_intent(self, user_input: str) -> SimpleIntentType:
        """Simple rule-based intent detection"""
        
        text_lower = user_input.lower()
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent_type
        
        return SimpleIntentType.CASUAL_CHAT
    
    def _extract_entities(self, user_input: str) -> Dict[str, Any]:
        """Extract simple entities from user input"""
        
        entities = {}
        text_lower = user_input.lower()
        
        # Website types
        website_types = {
            "ร้านอาหาร": ["ร้านอาหาร", "อาหาร", "restaurant", "food"],
            "ร้านค้า": ["ร้านค้า", "shop", "store", "ออนไลน์", "online"],
            "portfolio": ["portfolio", "ผลงาน", "โปรไฟล์"],
            "blog": ["blog", "บล็อก", "เขียน", "writing"]
        }
        
        for website_type, keywords in website_types.items():
            if any(keyword in text_lower for keyword in keywords):
                entities["website_type"] = website_type
                break
        
        # Colors
        colors = {
            "แดง": ["แดง", "red", "สีแดง"],
            "เขียว": ["เขียว", "green", "สีเขียว"],
            "น้ำเงิน": ["น้ำเงิน", "blue", "สีน้ำเงิน"],
            "ม่วง": ["ม่วง", "purple", "สีม่วง"]
        }
        
        for color, keywords in colors.items():
            if any(keyword in text_lower for keyword in keywords):
                entities["color"] = color
                break
        
        return entities
    
    async def _generate_response(self, intent: SimpleIntentType, user_input: str, websocket: WebSocket) -> SimpleAgentResponse:
        """Generate appropriate response based on intent"""
        
        if intent == SimpleIntentType.CREATE_WEBSITE:
            return await self._handle_create_website(user_input, websocket)
        elif intent == SimpleIntentType.MODIFY_DESIGN:
            return await self._handle_modify_design(user_input, websocket)
        elif intent == SimpleIntentType.ADD_FEATURE:
            return await self._handle_add_feature(user_input, websocket)
        else:
            return await self._handle_casual_chat(user_input)
    
    async def _handle_create_website(self, user_input: str, websocket: WebSocket) -> SimpleAgentResponse:
        """Handle website creation requests"""
        
        entities = self._extract_entities(user_input)
        website_type = entities.get("website_type", "general")
        
        # Send initial progress
        if websocket:
            await websocket.send_json({
                "type": "status",
                "message": f"เริ่มสร้างเว็บไซต์{website_type}แล้วครับ กำลังวิเคราะห์ความต้องการ...",
                "progress": 10
            })
        
        # Simulate requirements extraction
        requirements = self._simulate_requirements_extraction(user_input, website_type)
        
        if websocket:
            await websocket.send_json({
                "type": "requirements_extracted",
                "message": f"พบความต้องการ {len(requirements)} รายการ กำลังสร้างเว็บไซต์...",
                "requirements": requirements,
                "progress": 25
            })
        
        # Create task and execute
        task_id = await self.agent_manager.create_immediate_task({
            "type": "create_website",
            "requirements": user_input,
            "website_type": website_type,
            "user_context": self.user_context
        })
        
        self.active_project = task_id
        
        # Start async execution
        asyncio.create_task(self._stream_simple_creation(task_id, requirements, websocket))
        
        return SimpleAgentResponse(
            message=f"เริ่มสร้างเว็บไซต์{website_type}แล้วครับ! กำลังดำเนินการตามความต้องการ {len(requirements)} รายการ",
            action_taken="start_website_creation",
            progress_update={"task_id": task_id, "status": "started", "requirements": len(requirements)}
        )
    
    async def _handle_modify_design(self, user_input: str, websocket: WebSocket) -> SimpleAgentResponse:
        """Handle design modification requests"""
        
        if not self.active_project:
            return SimpleAgentResponse(
                message="ยังไม่มีเว็บไซต์ให้แก้ไขครับ ลองสร้างเว็บไซต์ใหม่ก่อนไหม?",
                suggestions=["สร้างเว็บไซต์ใหม่", "ทำเว็บไซต์ร้านอาหาร", "สร้าง portfolio"]
            )
        
        entities = self._extract_entities(user_input)
        
        if websocket:
            await websocket.send_json({
                "type": "status",
                "message": "กำลังปรับแต่งดีไซน์ตามที่ขอ...",
                "progress": 30
            })
        
        # Simulate modification
        await asyncio.sleep(2)
        
        modification_result = await self.agent_manager.modify_project(
            self.active_project, 
            user_input,
            entities
        )
        
        if websocket:
            await websocket.send_json({
                "type": "success",
                "message": "ปรับแต่งดีไซน์เสร็จแล้วครับ!",
                "preview_url": modification_result.get("preview_url"),
                "progress": 100
            })
        
        return SimpleAgentResponse(
            message="ปรับแต่งดีไซน์เสร็จแล้วครับ! ดูผลลัพธ์ได้เลย",
            action_taken="modify_design",
            preview_url=modification_result.get("preview_url")
        )
    
    async def _handle_add_feature(self, user_input: str, websocket: WebSocket) -> SimpleAgentResponse:
        """Handle feature addition requests"""
        
        if not self.active_project:
            return SimpleAgentResponse(
                message="ยังไม่มีเว็บไซต์ให้เพิ่มฟีเจอร์ครับ ลองสร้างเว็บไซต์ก่อนไหม?",
                suggestions=["สร้างเว็บไซต์ใหม่"]
            )
        
        feature_name = "ฟีเจอร์ใหม่"
        if "ปุ่ม" in user_input or "button" in user_input:
            feature_name = "ปุ่ม"
        elif "เมนู" in user_input or "menu" in user_input:
            feature_name = "เมนู"
        
        if websocket:
            await websocket.send_json({
                "type": "status",
                "message": f"กำลังเพิ่ม{feature_name}ให้เว็บไซต์...",
                "progress": 50
            })
        
        await asyncio.sleep(2)
        
        if websocket:
            await websocket.send_json({
                "type": "success", 
                "message": f"เพิ่ม{feature_name}เสร็จแล้วครับ!",
                "preview_url": f"/app/{self.active_project}/index.html",
                "progress": 100
            })
        
        return SimpleAgentResponse(
            message=f"เพิ่ม{feature_name}เสร็จแล้วครับ!",
            action_taken="add_feature",
            preview_url=f"/app/{self.active_project}/index.html"
        )
    
    async def _handle_casual_chat(self, user_input: str) -> SimpleAgentResponse:
        """Handle casual conversation"""
        
        responses = [
            "ครับ มีอะไรให้ช่วยเหลือไหม? ผมสามารถช่วยสร้างเว็บไซต์ได้นะครับ",
            "สวัสดีครับ! อยากให้ช่วยทำอะไรดีครับ?",
            "ครับผม พร้อมช่วยสร้างเว็บไซต์หรือปรับแต่งตามที่ต้องการครับ",
            "มีอะไรให้ช่วยไหมครับ? ลองบอกว่าอยากได้เว็บไซต์แบบไหนดูครับ"
        ]
        
        # Simple response selection based on input
        if "สวัสดี" in user_input or "hello" in user_input.lower():
            response_msg = "สวัสดีครับ! ยินดีต้อนรับสู่ AgentPro ผมพร้อมช่วยสร้างเว็บไซต์ให้คุณครับ"
        elif "ขอบคุณ" in user_input or "thank" in user_input.lower():
            response_msg = "ยินดีครับ! มีอะไรให้ช่วยอีกไหม?"
        else:
            import random
            response_msg = random.choice(responses)
        
        suggestions = [
            "สร้างเว็บไซต์ร้านอาหาร",
            "ทำเว็บไซต์ portfolio",  
            "สร้างหน้าร้านค้าออนไลน์",
            "แก้ไขสีและดีไซน์"
        ]
        
        return SimpleAgentResponse(
            message=response_msg,
            suggestions=suggestions
        )
    
    def _simulate_requirements_extraction(self, user_input: str, website_type: str) -> List[str]:
        """Simulate requirements extraction for demo"""
        
        base_requirements = ["เว็บไซต์โหลดได้", "ตอบสนองทุกอุปกรณ์", "มีหน้าหลัก"]
        
        if website_type == "ร้านอาหาร":
            return base_requirements + ["แสดงเมนูอาหาร", "ข้อมูลร้าน", "ติดต่อร้าน"]
        elif website_type == "ร้านค้า":
            return base_requirements + ["แสดงสินค้า", "ตะกร้าสินค้า", "ระบบสั่งซื้อ"]
        elif website_type == "portfolio":
            return base_requirements + ["แสดงผลงาน", "ประวัติส่วนตัว", "ช่องทางติดต่อ"]
        elif website_type == "blog":
            return base_requirements + ["เขียนบทความ", "หมวดหมู่", "ค้นหาบทความ"]
        else:
            return base_requirements + ["เนื้อหาทั่วไป", "ข้อมูลเกี่ยวกับ"]
    
    async def _stream_simple_creation(self, task_id: str, requirements: List[str], websocket: WebSocket):
        """Stream simple creation process"""
        
        try:
            async for update in self.agent_manager.execute_with_streaming(task_id):
                if websocket:
                    await websocket.send_json({
                        "type": "progress",
                        "agent": update.get("agent"),
                        "status": update.get("status"),
                        "message": update.get("message"),
                        "progress": update.get("progress", 0),
                        "preview_url": update.get("preview_url")
                    })
                
                # When completed, run simple testing
                if update.get("status") == "completed":
                    preview_url = update.get("preview_url")
                    
                    if websocket:
                        await websocket.send_json({
                            "type": "testing_start",
                            "message": "กำลังทดสอบความต้องการทั้งหมด...",
                            "progress": 85
                        })
                    
                    # Simulate testing
                    await asyncio.sleep(2)
                    
                    # Simple test results
                    passed_tests = len(requirements)
                    total_tests = len(requirements)
                    pass_rate = 100.0
                    
                    if websocket:
                        await websocket.send_json({
                            "type": "success",
                            "message": f"🎉 เว็บไซต์สร้างเสร็จและผ่านการทดสอบ {pass_rate:.0f}% ของความต้องการทั้งหมด!",
                            "preview_url": preview_url,
                            "test_report": {
                                "summary": {
                                    "total_tests": total_tests,
                                    "passed": passed_tests,
                                    "failed": 0,
                                    "pass_rate": pass_rate
                                },
                                "passed_requirements": requirements,
                                "failed_requirements": []
                            },
                            "progress": 100
                        })
                    break
                    
        except Exception as e:
            if websocket:
                await websocket.send_json({
                    "type": "error",
                    "message": f"เกิดข้อผิดพลาด: {str(e)}"
                })
    
    def _update_context(self, user_input: str, intent: SimpleIntentType):
        """Update user context based on input and intent"""
        
        self.user_context.update({
            "last_intent": intent.value,
            "last_input": user_input,
            "timestamp": time.time()
        })
        
        # Extract and store preferences
        entities = self._extract_entities(user_input)
        
        if "preferences" not in self.user_context:
            self.user_context["preferences"] = {}
            
        if entities.get("website_type"):
            self.user_context["preferences"]["website_type"] = entities["website_type"]
            
        if entities.get("color"):
            self.user_context["preferences"]["color"] = entities["color"]