"""
Requirements Analysis Agent
Agent ที่เชี่ยวชาญในการวิเคราะห์และแปล natural language เป็น technical requirements
"""

import json
import re
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from openai import AsyncOpenAI

from .base_agent import BaseAgent, AgentTask, AgentResult
from .requirement_tracker import RequirementTracker, Requirement, RequirementType, Priority, RequirementStatus

class AnalysisType(Enum):
    INITIAL = "initial"           # วิเคราะห์ครั้งแรก
    REFINEMENT = "refinement"     # ปรับแต่งความต้องการ
    CLARIFICATION = "clarification" # ขอคำชี้แจง
    VALIDATION = "validation"     # ตรวจสอบความถูกต้อง

@dataclass
class RequirementAnalysis:
    requirements: List[Requirement]
    technical_specifications: Dict[str, Any]
    clarification_questions: List[str]
    implementation_plan: List[Dict[str, Any]]
    risk_assessment: List[str]
    estimated_complexity: int  # 1-10 scale

class RequirementsAnalysisAgent(BaseAgent):
    """Agent สำหรับวิเคราะห์ requirements จาก natural language"""
    
    def __init__(self, openai_client: AsyncOpenAI):
        super().__init__(
            name="RequirementsAnalyst",
            capabilities=[
                "natural_language_processing",
                "requirements_extraction", 
                "technical_specification",
                "complexity_estimation",
                "risk_assessment"
            ]
        )
        self.client = openai_client
        self.requirement_tracker = RequirementTracker("default_project")
        
        # Knowledge base for common patterns
        self.pattern_database = {
            "website_types": {
                "ร้านอาหาร": {
                    "features": ["menu", "contact", "location", "gallery"],
                    "complexity": 3,
                    "typical_pages": ["home", "menu", "about", "contact"]
                },
                "ร้านค้าออนไลน์": {
                    "features": ["product_catalog", "shopping_cart", "payment", "user_account"],
                    "complexity": 7,
                    "typical_pages": ["home", "products", "cart", "checkout", "account"]
                },
                "portfolio": {
                    "features": ["gallery", "about", "contact", "projects"],
                    "complexity": 4,
                    "typical_pages": ["home", "portfolio", "about", "contact"]
                },
                "blog": {
                    "features": ["articles", "categories", "search", "comments"],
                    "complexity": 5,
                    "typical_pages": ["home", "blog", "post", "about"]
                }
            },
            "ui_patterns": {
                "modern": ["clean", "minimal", "responsive", "mobile-first"],
                "professional": ["corporate", "trustworthy", "formal"],
                "creative": ["artistic", "unique", "expressive", "colorful"],
                "e-commerce": ["product-focused", "conversion-optimized", "trust-signals"]
            },
            "color_schemes": {
                "warm": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"],
                "cool": ["#74b9ff", "#6c5ce7", "#a29bfe", "#fd79a8"],
                "neutral": ["#636e72", "#2d3436", "#ddd", "#f1f2f6"],
                "business": ["#2c3e50", "#3498db", "#e74c3c", "#f39c12"]
            }
        }
    
    def can_handle(self, task: AgentTask) -> bool:
        """ตรวจสอบว่า agent นี้สามารถจัดการงานได้หรือไม่"""
        return task.type in [
            "analyze_requirements",
            "extract_specifications",
            "refine_requirements",
            "validate_requirements"
        ]
    
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute requirements analysis task"""
        
        try:
            if task.type == "analyze_requirements":
                return await self._analyze_initial_requirements(task)
            elif task.type == "extract_specifications":
                return await self._extract_technical_specifications(task)
            elif task.type == "refine_requirements":
                return await self._refine_requirements(task)
            elif task.type == "validate_requirements":
                return await self._validate_requirements(task)
            else:
                return AgentResult(
                    success=False,
                    data={},
                    issues=[f"Unsupported task type: {task.type}"]
                )
                
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                issues=[f"Task execution failed: {str(e)}"]
            )
    
    async def improve_result(self, result: AgentResult, feedback: Dict[str, Any]) -> AgentResult:
        """Improve analysis based on feedback"""
        
        if not result.needs_improvement:
            return result
        
        # Analyze feedback and improve
        improvement_prompt = f"""
        Based on the following feedback, improve the requirements analysis:
        
        Original Analysis: {json.dumps(result.data, indent=2)}
        Feedback: {json.dumps(feedback, indent=2)}
        Issues: {result.issues}
        
        Please provide an improved analysis addressing the feedback.
        """
        
        try:
            improved_analysis = await self._get_ai_analysis(improvement_prompt, "improvement")
            
            return AgentResult(
                success=True,
                data=improved_analysis,
                suggestions=["Analysis improved based on feedback"]
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data=result.data,
                issues=result.issues + [f"Improvement failed: {str(e)}"]
            )
    
    async def _analyze_initial_requirements(self, task: AgentTask) -> AgentResult:
        """วิเคราะห์ requirements เบื้องต้นจาก user input"""
        
        user_input = task.input_data.get("user_input", "")
        user_context = task.input_data.get("user_context", {})
        
        if not user_input:
            return AgentResult(
                success=False,
                data={},
                issues=["No user input provided"]
            )
        
        # Step 1: Extract basic information
        basic_analysis = await self._extract_basic_requirements(user_input)
        
        # Step 2: Identify website type and complexity
        website_analysis = self._analyze_website_type(user_input, basic_analysis)
        
        # Step 3: Extract functional requirements
        functional_reqs = await self._extract_functional_requirements(user_input, website_analysis)
        
        # Step 4: Extract non-functional requirements
        non_functional_reqs = await self._extract_non_functional_requirements(user_input)
        
        # Step 5: Generate technical specifications
        tech_specs = await self._generate_technical_specifications(
            functional_reqs, non_functional_reqs, website_analysis
        )
        
        # Step 6: Create implementation plan
        implementation_plan = self._create_implementation_plan(
            functional_reqs, non_functional_reqs, website_analysis
        )
        
        # Step 7: Assess risks and complexity
        risk_assessment = self._assess_risks(functional_reqs, non_functional_reqs)
        complexity_score = self._calculate_complexity(functional_reqs, non_functional_reqs, website_analysis)
        
        # Step 8: Generate clarification questions if needed
        clarifications = self._generate_clarification_questions(basic_analysis, user_input)
        
        # Step 9: Create requirement objects
        all_requirements = functional_reqs + non_functional_reqs
        requirement_objects = []
        
        for req_data in all_requirements:
            req_obj = Requirement(
                id=self.requirement_tracker._generate_requirement_id(req_data["title"]),
                type=RequirementType(req_data["type"]),
                title=req_data["title"],
                description=req_data["description"],
                user_input=user_input,
                acceptance_criteria=req_data["acceptance_criteria"],
                priority=Priority(req_data["priority"]),
                status=RequirementStatus.PENDING,
                created_at=time.time(),
                updated_at=time.time(),
                tags=set(req_data.get("tags", []))
            )
            requirement_objects.append(req_obj)
            self.requirement_tracker.requirements[req_obj.id] = req_obj
        
        analysis_result = RequirementAnalysis(
            requirements=requirement_objects,
            technical_specifications=tech_specs,
            clarification_questions=clarifications,
            implementation_plan=implementation_plan,
            risk_assessment=risk_assessment,
            estimated_complexity=complexity_score
        )
        
        return AgentResult(
            success=True,
            data={
                "analysis_type": "initial",
                "requirements": [req.to_dict() for req in requirement_objects],
                "technical_specifications": tech_specs,
                "implementation_plan": implementation_plan,
                "clarification_questions": clarifications,
                "risk_assessment": risk_assessment,
                "complexity_score": complexity_score,
                "website_analysis": website_analysis,
                "agent_name": self.name
            },
            suggestions=[
                "Requirements extracted and analyzed",
                "Ready for technical implementation",
                f"Estimated complexity: {complexity_score}/10"
            ]
        )
    
    async def _extract_basic_requirements(self, user_input: str) -> Dict[str, Any]:
        """Extract basic requirements using AI"""
        
        prompt = f"""
        Analyze the following user input and extract basic requirements:
        
        User Input: "{user_input}"
        
        Extract and return JSON with:
        {{
            "main_purpose": "primary goal of the website",
            "target_audience": "who will use this website",
            "key_features": ["list", "of", "features", "mentioned"],
            "content_type": "what type of content will be shown",
            "business_goals": ["business", "objectives"],
            "constraints": ["any", "limitations", "mentioned"],
            "preferences": {{
                "style": "design style preferences",
                "colors": ["color", "preferences"],
                "layout": "layout preferences"
            }}
        }}
        
        Respond in Thai and English as appropriate.
        """
        
        return await self._get_ai_analysis(prompt, "basic_extraction")
    
    def _analyze_website_type(self, user_input: str, basic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze website type based on patterns"""
        
        input_lower = user_input.lower()
        detected_types = []
        
        # Check against known patterns
        for website_type, config in self.pattern_database["website_types"].items():
            if any(keyword in input_lower for keyword in [website_type.lower()]):
                detected_types.append({
                    "type": website_type,
                    "confidence": 0.9,
                    "config": config
                })
        
        # AI-based analysis if no clear match
        if not detected_types:
            detected_types.append({
                "type": "custom",
                "confidence": 0.5,
                "config": {
                    "features": basic_analysis.get("key_features", []),
                    "complexity": 5,
                    "typical_pages": ["home", "about", "contact"]
                }
            })
        
        primary_type = max(detected_types, key=lambda x: x["confidence"])
        
        return {
            "primary_type": primary_type["type"],
            "confidence": primary_type["confidence"],
            "suggested_features": primary_type["config"]["features"],
            "estimated_complexity": primary_type["config"]["complexity"],
            "typical_pages": primary_type["config"]["typical_pages"],
            "all_detected_types": detected_types
        }
    
    async def _extract_functional_requirements(self, user_input: str, website_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract functional requirements"""
        
        suggested_features = website_analysis.get("suggested_features", [])
        
        prompt = f"""
        Extract functional requirements from the user input and website analysis:
        
        User Input: "{user_input}"
        Website Type: {website_analysis.get("primary_type", "unknown")}
        Suggested Features: {suggested_features}
        
        Return JSON array of functional requirements:
        [
            {{
                "type": "functional",
                "title": "Short title",
                "description": "Detailed description",
                "acceptance_criteria": ["criteria1", "criteria2", "criteria3"],
                "priority": 1-4 (1=low, 4=critical),
                "tags": ["relevant", "tags"],
                "estimated_effort": "hours or story points"
            }}
        ]
        
        Focus on what the website should DO, not how it looks.
        """
        
        return await self._get_ai_analysis(prompt, "functional_extraction")
    
    async def _extract_non_functional_requirements(self, user_input: str) -> List[Dict[str, Any]]:
        """Extract non-functional requirements (performance, usability, etc.)"""
        
        prompt = f"""
        Extract non-functional requirements from the user input:
        
        User Input: "{user_input}"
        
        Return JSON array of non-functional requirements covering:
        - Performance requirements
        - Usability requirements  
        - Accessibility requirements
        - SEO requirements
        - Browser compatibility
        - Security requirements
        
        Format:
        [
            {{
                "type": "performance|ui_ux|accessibility|business",
                "title": "Short title",
                "description": "Detailed description", 
                "acceptance_criteria": ["measurable", "criteria"],
                "priority": 1-4,
                "tags": ["relevant", "tags"],
                "metrics": "how to measure success"
            }}
        ]
        """
        
        return await self._get_ai_analysis(prompt, "non_functional_extraction")
    
    async def _generate_technical_specifications(self, functional_reqs: List[Dict], non_functional_reqs: List[Dict], website_analysis: Dict) -> Dict[str, Any]:
        """Generate technical specifications"""
        
        all_reqs = functional_reqs + non_functional_reqs
        
        prompt = f"""
        Generate technical specifications based on requirements:
        
        Functional Requirements: {json.dumps(functional_reqs, indent=2)}
        Non-Functional Requirements: {json.dumps(non_functional_reqs, indent=2)}
        Website Analysis: {json.dumps(website_analysis, indent=2)}
        
        Return JSON with technical specifications:
        {{
            "frontend": {{
                "framework": "recommended frontend approach",
                "libraries": ["required", "libraries"],
                "build_tools": ["build", "tools"],
                "responsive_strategy": "mobile-first approach"
            }},
            "backend": {{
                "required": true/false,
                "services": ["required", "services"],
                "database": "database requirements",
                "apis": ["required", "apis"]
            }},
            "infrastructure": {{
                "hosting": "hosting requirements",
                "performance": "performance requirements",
                "security": "security requirements",
                "monitoring": "monitoring needs"
            }},
            "file_structure": {{
                "html_files": ["required", "html", "files"],
                "css_files": ["required", "css", "files"],
                "js_files": ["required", "js", "files"],
                "assets": ["images", "fonts", "etc"]
            }}
        }}
        """
        
        return await self._get_ai_analysis(prompt, "technical_specs")
    
    def _create_implementation_plan(self, functional_reqs: List[Dict], non_functional_reqs: List[Dict], website_analysis: Dict) -> List[Dict[str, Any]]:
        """Create implementation plan with phases"""
        
        all_reqs = functional_reqs + non_functional_reqs
        
        # Group requirements by priority and dependencies
        phases = [
            {
                "phase": 1,
                "name": "Foundation & Structure",
                "description": "Basic HTML structure, core CSS, navigation",
                "requirements": [req for req in all_reqs if req.get("priority", 1) >= 3],
                "estimated_time": "2-4 hours",
                "deliverables": ["Basic website structure", "Navigation system", "Responsive layout"]
            },
            {
                "phase": 2,
                "name": "Content & Styling",
                "description": "Content integration, visual design, styling",
                "requirements": [req for req in all_reqs if req.get("type") == "ui_ux"],
                "estimated_time": "3-5 hours",
                "deliverables": ["Visual design", "Content integration", "Interactive elements"]
            },
            {
                "phase": 3,
                "name": "Features & Functionality", 
                "description": "Interactive features, forms, dynamic content",
                "requirements": [req for req in all_reqs if req.get("type") == "functional" and req.get("priority", 1) >= 2],
                "estimated_time": "4-8 hours",
                "deliverables": ["Interactive features", "Form handling", "Dynamic content"]
            },
            {
                "phase": 4,
                "name": "Optimization & Testing",
                "description": "Performance optimization, testing, final touches",
                "requirements": [req for req in all_reqs if req.get("type") in ["performance", "accessibility"]],
                "estimated_time": "2-3 hours",
                "deliverables": ["Performance optimization", "Accessibility compliance", "Cross-browser testing"]
            }
        ]
        
        return phases
    
    def _assess_risks(self, functional_reqs: List[Dict], non_functional_reqs: List[Dict]) -> List[str]:
        """Assess implementation risks"""
        
        risks = []
        
        # Check complexity indicators
        total_requirements = len(functional_reqs) + len(non_functional_reqs)
        if total_requirements > 15:
            risks.append("High number of requirements may increase complexity")
        
        # Check for complex features
        complex_features = ["payment", "user_account", "database", "api", "real-time"]
        mentioned_complex = []
        
        for req in functional_reqs:
            req_text = (req.get("description", "") + " " + req.get("title", "")).lower()
            for feature in complex_features:
                if feature in req_text:
                    mentioned_complex.append(feature)
        
        if mentioned_complex:
            risks.append(f"Complex features detected: {', '.join(set(mentioned_complex))}")
        
        # Check for conflicting requirements
        ui_requirements = [req for req in functional_reqs + non_functional_reqs if req.get("type") == "ui_ux"]
        if len(ui_requirements) > 5:
            risks.append("Multiple UI/UX requirements may create design conflicts")
        
        # Performance vs feature trade-offs
        performance_reqs = [req for req in non_functional_reqs if "performance" in req.get("tags", [])]
        if performance_reqs and mentioned_complex:
            risks.append("Performance requirements vs complex features may require trade-offs")
        
        return risks if risks else ["Low risk project - standard implementation"]
    
    def _calculate_complexity(self, functional_reqs: List[Dict], non_functional_reqs: List[Dict], website_analysis: Dict) -> int:
        """Calculate complexity score (1-10)"""
        
        base_complexity = website_analysis.get("estimated_complexity", 3)
        
        # Adjust based on number of requirements
        req_count_factor = min(2, len(functional_reqs + non_functional_reqs) / 10)
        
        # Adjust based on priority distribution
        high_priority_count = len([req for req in functional_reqs + non_functional_reqs if req.get("priority", 1) >= 3])
        priority_factor = min(2, high_priority_count / 5)
        
        # Adjust based on feature complexity
        complex_keywords = ["dynamic", "interactive", "database", "api", "user", "account", "payment"]
        complexity_mentions = 0
        
        for req in functional_reqs + non_functional_reqs:
            req_text = (req.get("description", "") + " " + req.get("title", "")).lower()
            complexity_mentions += sum(1 for keyword in complex_keywords if keyword in req_text)
        
        complexity_factor = min(2, complexity_mentions / 5)
        
        final_complexity = base_complexity + req_count_factor + priority_factor + complexity_factor
        return min(10, max(1, int(final_complexity)))
    
    def _generate_clarification_questions(self, basic_analysis: Dict[str, Any], user_input: str) -> List[str]:
        """Generate questions to clarify requirements"""
        
        questions = []
        
        # Check for missing information
        if not basic_analysis.get("target_audience"):
            questions.append("Who is your target audience for this website?")
        
        if not basic_analysis.get("key_features"):
            questions.append("What are the most important features you want on your website?")
        
        if not basic_analysis.get("preferences", {}).get("style"):
            questions.append("Do you have any preferences for the design style (modern, professional, creative, etc.)?")
        
        if not basic_analysis.get("preferences", {}).get("colors"):
            questions.append("Do you have preferred colors or color schemes?")
        
        # Check for vague requirements
        if "ดูดี" in user_input or "สวย" in user_input:
            questions.append("Can you be more specific about what 'good looking' or 'beautiful' means to you?")
        
        if "ง่าย" in user_input or "simple" in user_input.lower():
            questions.append("What does 'simple' mean to you - minimal design, easy navigation, or something else?")
        
        # Limit to most important questions
        return questions[:3] if questions else []
    
    async def _get_ai_analysis(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Get AI analysis with error handling"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert requirements analyst. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                timeout=30
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {analysis_type}: {e}")
            return self._get_fallback_analysis(analysis_type)
        except Exception as e:
            print(f"AI analysis error in {analysis_type}: {e}")
            return self._get_fallback_analysis(analysis_type)
    
    def _get_fallback_analysis(self, analysis_type: str) -> Dict[str, Any]:
        """Provide fallback analysis when AI fails"""
        
        fallbacks = {
            "basic_extraction": {
                "main_purpose": "Create a website",
                "target_audience": "General users",
                "key_features": ["home page", "navigation", "contact"],
                "content_type": "General content",
                "business_goals": ["Online presence"],
                "constraints": [],
                "preferences": {"style": "modern", "colors": [], "layout": "standard"}
            },
            "functional_extraction": [
                {
                    "type": "functional",
                    "title": "Basic Website Structure",
                    "description": "Create basic website with navigation",
                    "acceptance_criteria": ["Website loads", "Navigation works", "Pages are accessible"],
                    "priority": 3,
                    "tags": ["basic", "structure"],
                    "estimated_effort": "2-3 hours"
                }
            ],
            "non_functional_extraction": [
                {
                    "type": "ui_ux",
                    "title": "Responsive Design",
                    "description": "Website should work on all devices",
                    "acceptance_criteria": ["Mobile friendly", "Tablet compatible", "Desktop optimized"],
                    "priority": 3,
                    "tags": ["responsive", "ui"],
                    "metrics": "Works on devices 320px+"
                }
            ],
            "technical_specs": {
                "frontend": {
                    "framework": "HTML5, CSS3, JavaScript",
                    "libraries": ["No external libraries"],
                    "build_tools": ["None required"],
                    "responsive_strategy": "Mobile-first CSS"
                },
                "backend": {
                    "required": False,
                    "services": [],
                    "database": "None",
                    "apis": []
                },
                "infrastructure": {
                    "hosting": "Static hosting",
                    "performance": "Fast loading",
                    "security": "Basic security",
                    "monitoring": "Basic monitoring"
                },
                "file_structure": {
                    "html_files": ["index.html"],
                    "css_files": ["styles.css"],
                    "js_files": ["script.js"],
                    "assets": ["images folder"]
                }
            }
        }
        
        return fallbacks.get(analysis_type, {})