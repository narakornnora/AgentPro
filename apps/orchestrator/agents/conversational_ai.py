"""
Conversational AI Interface for Real-time Agent Management
Provides natural, flowing chat experience with instant AI responses
"""

import json
import asyncio
import re
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import openai
from fastapi import WebSocket, WebSocketDisconnect
import uuid

# Import our agent modules
from .base_agent import AgentTask, TaskPriority
from .requirement_tracker import RequirementTracker, RequirementStatus
from .requirements_analysis_agent import RequirementsAnalysisAgent
from .regression_tester import RegressionTester, TestCase, TestType

class IntentType(Enum):
    CREATE_WEBSITE = "create_website"
    MODIFY_DESIGN = "modify_design" 
    CHANGE_CONTENT = "change_content"
    ADD_FEATURE = "add_feature"
    FIX_ISSUE = "fix_issue"
    IMPROVE_QUALITY = "improve_quality"
    GET_STATUS = "get_status"
    CASUAL_CHAT = "casual_chat"

class ActionType(Enum):
    IMMEDIATE = "immediate"  # Execute right away
    PLANNED = "planned"      # Add to workflow
    CLARIFY = "clarify"      # Need more info

@dataclass
class UserIntent:
    intent: IntentType
    action: ActionType
    entities: Dict[str, Any]
    confidence: float
    raw_text: str
    context: Dict[str, Any] = None

@dataclass
class ChatMessage:
    id: str
    role: str  # user, assistant, system
    content: str
    timestamp: float
    metadata: Dict[str, Any] = None
    
@dataclass 
class AgentResponse:
    message: str
    action_taken: Optional[str] = None
    progress_update: Optional[Dict[str, Any]] = None
    preview_url: Optional[str] = None
    suggestions: List[str] = None

class ConversationalAI:
    def __init__(self, openai_client, agent_manager):
        self.client = openai_client
        self.agent_manager = agent_manager
        self.conversation_history: List[ChatMessage] = []
        self.user_context: Dict[str, Any] = {}
        self.active_project: Optional[str] = None
        
        # Initialize requirement tracking and analysis  
        try:
            from .requirement_tracker import RequirementTracker
            from .requirements_analysis_agent import RequirementsAnalysisAgent  
            from .regression_tester import RegressionTester
            
            self.requirement_tracker = RequirementTracker("default_project")
            self.requirements_analyst = RequirementsAnalysisAgent(openai_client)
            self.regression_tester = RegressionTester()
        except Exception as e:
            print(f"Warning: Could not initialize advanced features: {e}")
            self.requirement_tracker = None
            self.requirements_analyst = None 
            self.regression_tester = None
        
        # Intent patterns for Thai and English
        self.intent_patterns = {
            IntentType.CREATE_WEBSITE: [
                r"สร้าง(?:เว็บ|website|เว็บไซต์)",
                r"ทำ(?:เว็บ|website|เว็บไซต์)",
                r"(?:create|make|build).*(?:website|site|page)",
                r"ช่วย(?:สร้าง|ทำ).*(?:เว็บ|หน้าเว็บ)"
            ],
            IntentType.MODIFY_DESIGN: [
                r"(?:เปลี่ยน|แก้|ปรับ).*(?:สี|color|design|ดีไซน์)",
                r"(?:change|modify|update).*(?:color|design|layout|style)",
                r"ให้.*(?:สี|ดู).*(?:ดีขึ้น|สวยขึ้น|ดีกว่า)"
            ],
            IntentType.ADD_FEATURE: [
                r"(?:เพิ่ม|add).*(?:ปุ่ม|button|เมนู|menu|ฟีเจอร์|feature)",
                r"ใส่.*(?:ระบบ|system|การทำงาน|functionality)",
                r"อยาก(?:ให้มี|ได้).*(?:การทำงาน|ฟีเจอร์)"
            ],
            IntentType.FIX_ISSUE: [
                r"(?:แก้|fix|solve).*(?:ปัญหา|problem|bug|error)",
                r"(?:ไม่|not).*(?:ทำงาน|work|working)",
                r"มีปัญหา|เสีย|พัง|broken"
            ]
        }
        
    async def process_message(self, user_input: str, websocket: WebSocket = None) -> AgentResponse:
        """Process user message and generate appropriate response"""
        
        # Add to conversation history
        msg_id = str(uuid.uuid4())
        user_msg = ChatMessage(
            id=msg_id,
            role="user", 
            content=user_input,
            timestamp=datetime.now().timestamp()
        )
        self.conversation_history.append(user_msg)
        
        # Analyze user intent
        intent = await self._analyze_intent(user_input)
        
        # Update user context
        self._update_context(intent)
        
        # Generate response based on intent and context
        response = await self._generate_response(intent, websocket)
        
        # Add assistant response to history
        assistant_msg = ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response.message,
            timestamp=datetime.now().timestamp(),
            metadata={"intent": intent.intent.value, "action": response.action_taken}
        )
        self.conversation_history.append(assistant_msg)
        
        return response
    
    async def _analyze_intent(self, user_input: str) -> UserIntent:
        """Analyze user intent using patterns and AI"""
        
        # First, try pattern matching for quick common intents
        detected_intent = self._pattern_match_intent(user_input)
        
        if detected_intent:
            return detected_intent
            
        # If no pattern match, use AI for more complex analysis
        return await self._ai_analyze_intent(user_input)
    
    def _pattern_match_intent(self, text: str) -> Optional[UserIntent]:
        """Quick pattern matching for common intents"""
        
        text_lower = text.lower()
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    entities = self._extract_entities(text, intent_type)
                    action_type = ActionType.IMMEDIATE if self._is_immediate_request(text) else ActionType.PLANNED
                    
                    return UserIntent(
                        intent=intent_type,
                        action=action_type,
                        entities=entities,
                        confidence=0.8,
                        raw_text=text,
                        context=self.user_context
                    )
        return None
    
    async def _ai_analyze_intent(self, user_input: str) -> UserIntent:
        """Use AI to analyze complex intents"""
        
        context = self._get_conversation_context()
        
        prompt = f"""
        วิเคราะห์ความตั้งใจของผู้ใช้จากข้อความต่อไปนี้:
        "{user_input}"
        
        บริบทการสนทนา: {context}
        
        ตอบกลับเป็น JSON ในรูปแบบ:
        {{
            "intent": "create_website|modify_design|add_feature|fix_issue|improve_quality|get_status|casual_chat",
            "action": "immediate|planned|clarify",
            "entities": {{}},
            "confidence": 0.0-1.0,
            "explanation": "คำอธิบายสั้นๆ"
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return UserIntent(
                intent=IntentType(result["intent"]),
                action=ActionType(result["action"]),
                entities=result.get("entities", {}),
                confidence=result.get("confidence", 0.5),
                raw_text=user_input,
                context=self.user_context
            )
            
        except Exception as e:
            print(f"AI intent analysis failed: {e}")
            # Fallback to casual chat
            return UserIntent(
                intent=IntentType.CASUAL_CHAT,
                action=ActionType.CLARIFY,
                entities={},
                confidence=0.3,
                raw_text=user_input
            )
    
    def _extract_entities(self, text: str, intent_type: IntentType) -> Dict[str, Any]:
        """Extract entities based on intent type"""
        
        entities = {}
        
        if intent_type == IntentType.CREATE_WEBSITE:
            # Extract website type, features, etc.
            website_types = ["ร้านอาหาร", "ร้านค้า", "บล็อก", "portfolio", "restaurant", "shop", "blog"]
            for wtype in website_types:
                if wtype.lower() in text.lower():
                    entities["website_type"] = wtype
                    break
                    
        elif intent_type == IntentType.MODIFY_DESIGN:
            # Extract colors, design elements
            colors = ["แดง", "เขียว", "น้ำเงิน", "red", "green", "blue", "สีแดง", "สีเขียว", "สีน้ำเงิน"]
            for color in colors:
                if color.lower() in text.lower():
                    entities["color"] = color
                    break
                    
        elif intent_type == IntentType.ADD_FEATURE:
            # Extract feature types
            features = ["ปุ่ม", "เมนู", "ตะกร้า", "button", "menu", "cart", "contact", "gallery"]
            for feature in features:
                if feature.lower() in text.lower():
                    entities["feature"] = feature
                    break
        
        return entities
    
    def _is_immediate_request(self, text: str) -> bool:
        """Check if user wants immediate action"""
        immediate_keywords = [
            "เดี๋ยวนี้", "ทันที", "ตอนนี้", "เลย", "now", "immediately", "right now",
            "ช่วย", "please", "กด", "click"
        ]
        return any(keyword in text.lower() for keyword in immediate_keywords)
    
    async def _generate_response(self, intent: UserIntent, websocket: WebSocket = None) -> AgentResponse:
        """Generate appropriate response based on intent"""
        
        if intent.action == ActionType.IMMEDIATE:
            return await self._execute_immediate_action(intent, websocket)
        elif intent.action == ActionType.PLANNED:
            return await self._create_planned_action(intent)
        else:
            return await self._request_clarification(intent)
    
    async def _execute_immediate_action(self, intent: UserIntent, websocket: WebSocket) -> AgentResponse:
        """Execute immediate actions"""
        
        if intent.intent == IntentType.CREATE_WEBSITE:
            return await self._create_website_immediately(intent, websocket)
        elif intent.intent == IntentType.MODIFY_DESIGN:
            return await self._modify_design_immediately(intent, websocket)
        elif intent.intent == IntentType.ADD_FEATURE:
            return await self._add_feature_immediately(intent, websocket)
        elif intent.intent == IntentType.GET_STATUS:
            return await self._get_current_status()
        else:
            return await self._casual_chat_response(intent)
    
    async def _create_website_immediately(self, intent: UserIntent, websocket: WebSocket) -> AgentResponse:
        """Create website immediately with requirements tracking"""
        
        if websocket:
            await websocket.send_json({
                "type": "status",
                "message": "เริ่มสร้างเว็บไซต์แล้วครับ กำลังวิเคราะห์ความต้องการ...",
                "progress": 10
            })
        
        # Step 1: Extract and track requirements
        user_id = self.user_context.get("user_id", "anonymous")
        
        if self.requirement_tracker:
            requirements = self.requirement_tracker.extract_requirements_from_input(intent.raw_text, user_id)
        else:
            # Fallback if requirements tracker is not available
            requirements = []
        
        if websocket:
            await websocket.send_json({
                "type": "requirements_extracted",
                "message": f"พบความต้องการ {len(requirements)} รายการ กำลังวิเคราะห์รายละเอียด...",
                "requirements": [req.title for req in requirements],
                "progress": 25
            })
        
        # Step 2: Detailed requirements analysis
        if self.requirements_analyst:
            analysis_task = AgentTask(
                id=f"analysis_{int(time.time())}",
                type="analyze_requirements",
                priority=TaskPriority.CRITICAL,
                input_data={
                    "user_input": intent.raw_text,
                    "user_context": self.user_context,
                    "extracted_requirements": [req.to_dict() for req in requirements] if requirements else []
                },
                requirements=["detailed_analysis", "technical_specs", "implementation_plan"]
            )
            
            analysis_result = await self.requirements_analyst.execute_task(analysis_task)
        else:
            # Fallback analysis
            analysis_result = AgentResult(
                success=True,
                data={
                    "complexity_score": 5,
                    "website_analysis": {"primary_type": "general"}
                }
            )
        
        if websocket:
            await websocket.send_json({
                "type": "analysis_complete",
                "message": f"วิเคราะห์เสร็จแล้ว ความซับซ้อน: {analysis_result.data.get('complexity_score', 5)}/10",
                "complexity": analysis_result.data.get('complexity_score', 5),
                "progress": 40
            })
        
        # Step 3: Create implementation task with full context
        website_type = intent.entities.get("website_type", analysis_result.data.get("website_analysis", {}).get("primary_type", "general"))
        
        task_id = await self.agent_manager.create_immediate_task({
            "type": "create_website",
            "requirements": intent.raw_text,
            "website_type": website_type,
            "user_context": self.user_context,
            "detailed_analysis": analysis_result.data,
            "tracked_requirements": [req.to_dict() for req in requirements]
        })
        
        self.active_project = task_id
        
        if websocket:
            await websocket.send_json({
                "type": "status", 
                "message": "กำลังออกแบบและเขียนโค้ดตามความต้องการ...",
                "progress": 60
            })
        
        # Step 4: Start async execution with regression testing
        asyncio.create_task(self._stream_creation_with_testing(task_id, requirements, websocket))
        
        return AgentResponse(
            message=f"เริ่มสร้างเว็บไซต์แล้วครับ! ติดตามความต้องการ {len(requirements)} รายการ จะทดสอบให้อัตโนมัติ",
            action_taken="start_website_creation_with_tracking",
            progress_update={
                "task_id": task_id, 
                "status": "started",
                "requirements_tracked": len(requirements),
                "complexity_score": analysis_result.data.get('complexity_score', 5)
            }
        )
    
    async def _stream_creation_with_testing(self, task_id: str, requirements: List, websocket: WebSocket):
        """Stream progress with automatic testing"""
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
                
                # When implementation is completed, run regression tests
                if update.get("status") == "completed":
                    preview_url = update.get("preview_url")
                    files_created = update.get("files", [])
                    
                    if websocket:
                        await websocket.send_json({
                            "type": "testing_start",
                            "message": "เว็บไซต์สร้างเสร็จแล้ว กำลังทดสอบความต้องการทั้งหมด...",
                            "progress": 85
                        })
                    
                    # Generate and run regression tests
                    await self._run_automatic_testing(task_id, requirements, preview_url, files_created, websocket)
                    break
                    
        except Exception as e:
            if websocket:
                await websocket.send_json({
                    "type": "error",
                    "message": f"เกิดข้อผิดพลาด: {str(e)}"
                })
    
    async def _run_automatic_testing(self, task_id: str, requirements: List, preview_url: Optional[str], files_created: List[str], websocket: WebSocket):
        """Run automatic regression testing"""
        
        try:
            # Generate test cases from requirements
            test_cases = []
            
            for req in requirements:
                # Convert requirement to test cases
                for i, criteria in enumerate(req.acceptance_criteria):
                    test_case = TestCase(
                        id=f"{req.id}_test_{i}",
                        requirement_id=req.id,
                        title=f"Test: {criteria}",
                        description=f"Verify: {criteria}",
                        type=TestType.REGRESSION,
                        priority=req.priority.value,
                        test_steps=[
                            "Load website",
                            f"Verify: {criteria}",
                            "Check result"
                        ],
                        expected_result=criteria,
                        files_to_check=files_created
                    )
                    test_cases.append(test_case)
            
            if websocket:
                await websocket.send_json({
                    "type": "testing_progress",
                    "message": f"สร้าง test cases {len(test_cases)} รายการ กำลังทดสอบ...",
                    "test_count": len(test_cases),
                    "progress": 90
                })
            
            # Run regression tests
            project_slug = task_id.replace("task_", "myapp-")
            
            async with RegressionTester() as tester:
                test_results = await tester.run_all_tests(test_cases, project_slug)
                test_report = tester.generate_test_report(test_results)
            
            # Update requirement status based on test results
            passed_requirements = []
            failed_requirements = []
            
            for req in requirements:
                req_tests = [result for result in test_results.values() if result.requirement_id == req.id]
                req_passed = all(test.status.value == "passed" for test in req_tests)
                
                if req_passed:
                    self.requirement_tracker.update_requirement_status(req.id, RequirementStatus.VERIFIED)
                    passed_requirements.append(req.title)
                else:
                    self.requirement_tracker.update_requirement_status(req.id, RequirementStatus.IMPLEMENTED)
                    failed_requirements.append(req.title)
                
                # Add test results to requirement
                for test_result in req_tests:
                    test_case_data = {
                        "test_id": test_result.test_id,
                        "status": test_result.status.value,
                        "message": test_result.message,
                        "execution_time": test_result.execution_time
                    }
                    self.requirement_tracker.add_test_case(req.id, test_case_data)
            
            # Send final results
            if websocket:
                success_rate = test_report["summary"]["pass_rate"]
                
                if success_rate >= 80:
                    final_message = f"🎉 เว็บไซต์สร้างเสร็จและผ่านการทดสอบ {success_rate:.1f}% ของความต้องการทั้งหมด!"
                    status_type = "success"
                elif success_rate >= 60:
                    final_message = f"⚠️ เว็บไซต์สร้างเสร็จแล้ว แต่ผ่านการทดสอบเพียง {success_rate:.1f}% - กำลังปรับปรุง"
                    status_type = "partial_success"
                else:
                    final_message = f"❌ เว็บไซต์สร้างเสร็จแต่ผ่านการทดสอบเพียง {success_rate:.1f}% - ต้องแก้ไข"
                    status_type = "needs_improvement"
                
                await websocket.send_json({
                    "type": status_type,
                    "message": final_message,
                    "preview_url": preview_url,
                    "test_report": {
                        "summary": test_report["summary"],
                        "passed_requirements": passed_requirements,
                        "failed_requirements": failed_requirements,
                        "total_tests": len(test_cases),
                        "pass_rate": success_rate
                    },
                    "progress": 100
                })
                
                # If not fully successful, trigger improvement cycle
                if success_rate < 80 and failed_requirements:
                    await self._trigger_improvement_cycle(failed_requirements, test_results, websocket)
            
        except Exception as e:
            if websocket:
                await websocket.send_json({
                    "type": "testing_error",
                    "message": f"เกิดข้อผิดพลาดในการทดสอบ: {str(e)}",
                    "preview_url": preview_url,
                    "progress": 100
                })
    
    async def _trigger_improvement_cycle(self, failed_requirements: List[str], test_results: Dict, websocket: WebSocket):
        """Trigger automatic improvement cycle for failed tests"""
        
        if websocket:
            await websocket.send_json({
                "type": "improvement_start", 
                "message": f"เริ่มปรับปรุงอัตโนมัติสำหรับ {len(failed_requirements)} รายการที่ยังไม่ผ่าน",
                "failed_items": failed_requirements
            })
        
        # This would trigger the improvement agents
        # Implementation depends on the improvement agent system
        
        # For now, just notify that improvements are planned
        if websocket:
            await websocket.send_json({
                "type": "improvement_queued",
                "message": "การปรับปรุงถูกจัดคิวแล้ว จะแจ้งเมื่อเสร็จสิ้น",
                "estimated_time": "5-10 minutes"
            })
    
    async def _modify_design_immediately(self, intent: UserIntent, websocket: WebSocket) -> AgentResponse:
        """Modify design with immediate feedback"""
        
        if not self.active_project:
            return AgentResponse(
                message="ยังไม่มีเว็บไซต์ให้แก้ไขครับ ลองสร้างเว็บไซต์ใหม่ก่อนไหม?",
                action_taken=None
            )
        
        if websocket:
            await websocket.send_json({
                "type": "status",
                "message": "กำลังปรับแต่งดีไซน์ตามที่ขอ...",
                "progress": 20
            })
        
        # Execute modification
        modification_result = await self.agent_manager.modify_project(
            self.active_project, 
            intent.raw_text,
            intent.entities
        )
        
        if websocket:
            await websocket.send_json({
                "type": "completed",
                "message": "ปรับแต่งดีไซน์เสร็จแล้วครับ!",
                "preview_url": modification_result.get("preview_url"),
                "changes": modification_result.get("changes", [])
            })
        
        return AgentResponse(
            message="ปรับแต่งดีไซน์เสร็จแล้วครับ! ดูผลลัพธ์ได้เลย",
            action_taken="modify_design",
            preview_url=modification_result.get("preview_url")
        )
    
    async def _casual_chat_response(self, intent: UserIntent) -> AgentResponse:
        """Handle casual conversation"""
        
        casual_prompts = [
            "ครับ มีอะไรให้ช่วยเหลือไหม? ผมสามารถช่วยสร้างเว็บไซต์ได้นะครับ",
            "สวัสดีครับ! อยากให้ช่วยทำอะไรดีครับ?",
            "ครับผม พร้อมช่วยสร้างเว็บไซต์หรือปรับแต่งตามที่ต้องการครับ",
            "มีอะไรให้ช่วยไหมครับ? ลองบอกว่าอยากได้เว็บไซต์แบบไหนดูครับ"
        ]
        
        import random
        response_msg = random.choice(casual_prompts)
        
        # Add helpful suggestions based on conversation context
        suggestions = [
            "สร้างเว็บไซต์ร้านอาหาร",
            "ทำเว็บไซต์ portfolio",  
            "สร้างหน้าร้านค้าออนไลน์",
            "แก้ไขสีและดีไซน์"
        ]
        
        return AgentResponse(
            message=response_msg,
            suggestions=suggestions
        )
    
    def _get_conversation_context(self) -> str:
        """Get recent conversation context"""
        recent_messages = self.conversation_history[-5:] if len(self.conversation_history) > 5 else self.conversation_history
        context_parts = []
        
        for msg in recent_messages:
            context_parts.append(f"{msg.role}: {msg.content}")
            
        return " | ".join(context_parts)
    
    def _update_context(self, intent: UserIntent):
        """Update user context based on intent"""
        self.user_context.update({
            "last_intent": intent.intent.value,
            "last_entities": intent.entities,
            "timestamp": datetime.now().timestamp()
        })
        
        # Track user preferences
        if "preferences" not in self.user_context:
            self.user_context["preferences"] = {}
            
        if intent.entities.get("website_type"):
            self.user_context["preferences"]["website_type"] = intent.entities["website_type"]
            
        if intent.entities.get("color"):
            self.user_context["preferences"]["color"] = intent.entities["color"]