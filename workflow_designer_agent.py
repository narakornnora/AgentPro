#!/usr/bin/env python3
"""
🎯 AI Workflow Designer Agent
วิเคราะห์ความต้องการลูกค้า → ออกแบบ Workflow → สร้าง App Architecture
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WorkflowDesignerAgent:
    """AI Agent ที่ออกแบบ Workflow และ App Architecture"""
    
    def __init__(self):
        self.conversation_history = []
        
    def intelligent_project_analysis(self, customer_input: str) -> Dict[str, Any]:
        """🧠 Step 1: AI วิเคราะห์อัจฉริยะเพื่อแยกประเภทโครงการ"""
        
        analysis_prompt = f"""
คุณเป็น AI Project Analyzer ที่เชี่ยวชาญในการแยกแยะประเภทโครงการ

Customer Input: "{customer_input}"

วิเคราะห์และแยกประเภทโครงการพร้อมเหตุผล ส่งกลับ JSON:

{{
    "project_type_analysis": {{
        "primary_type": "mobile_app|web_app|website|desktop_app|api_service|system_integration",
        "confidence": 0.95,
        "reasoning": "เหตุผลที่เลือก type นี้",
        "alternative_types": ["ประเภทอื่นที่เป็นไปได้"],
        "keywords_detected": ["คำสำคัญที่ใช้ตัดสิน"]
    }},
    
    "platform_recommendations": {{
        "recommended_platform": "iOS + Android|Web Browser|Desktop|Cross-platform",
        "reasoning": "เหตุผลการเลือก platform",
        "considerations": ["ข้อพิจารณาเพิ่มเติม"]
    }},
    
    "business_analysis": {{
        "business_type": "ประเภทธุรกิจ (ecommerce, social, productivity, etc.)",
        "target_audience": ["กลุ่มเป้าหมายหลัก"],
        "main_objectives": ["วัตถุประสงค์หลัก"],
        "key_problems": ["ปัญหาที่ต้องแก้ไข"],
        "success_metrics": ["เมตริกวัดความสำเร็จ"]
    }},
    
    "technical_complexity": {{
        "complexity_level": "simple|medium|complex|enterprise",
        "estimated_screens": 5,
        "estimated_features": 8,
        "development_time": "2-4 weeks",
        "team_size": "1-3 developers"
    }},
    
    "immediate_questions": [
        "คำถามที่ควรถามลูกค้าเพิ่มเติม 1",
        "คำถามที่ควรถามลูกค้าเพิ่มเติม 2"
    ],
    
    "next_steps": [
        "ขั้นตอนถัดไป 1",
        "ขั้นตอนถัดไป 2"
    ]
}}

กฎการแยกประเภท:
- มี "แอป", "mobile", "ดาวน์โหลด", "App Store", "Google Play" → mobile_app
- มี "เว็บไซต์", "website", "หน้าเว็บ", "ประชาสัมพันธ์", "โชว์ผลงาน" → website  
- มี "ระบบ", "จัดการ", "dashboard", "admin", "web app", "ใช้งานผ่านเว็บ" → web_app
- มี "API", "เชื่อมต่อ", "integration", "service" → api_service
- มี "โปรแกรม", "desktop", "PC", "คอมพิวเตอร์" → desktop_app

วิเคราะห์จาก context และคำศัพท์เพื่อให้ได้ความต้องการที่แท้จริง
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def design_user_journey(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: ออกแบบ User Journey และ Workflow"""
        
        journey_prompt = f"""
คุณเป็น UX Designer ที่เชี่ยวชาญในการออกแบบ User Journey

Requirements: {json.dumps(requirements, ensure_ascii=False, indent=2)}

โปรดออกแบบ User Journey ที่สมบูรณ์ใน JSON format:

{{
    "user_personas": [
        {{
            "name": "ชื่อ Persona",
            "description": "คำอธิบาย",
            "pain_points": ["จุดเจง 1", "จุดเจง 2"],
            "goals": ["เป้าหมาย 1", "เป้าหมาย 2"]
        }}
    ],
    "user_journeys": [
        {{
            "persona": "ชื่อ Persona",
            "scenario": "สถานการณ์การใช้งาน",
            "steps": [
                {{
                    "step": 1,
                    "action": "การกระทำ",
                    "screen": "หน้าจอที่เกี่ยวข้อง",
                    "emotions": "อารมณ์ของผู้ใช้",
                    "pain_points": ["ปัญหาที่อาจเกิด"],
                    "opportunities": ["โอกาสในการปรับปรุง"]
                }}
            ]
        }}
    ],
    "key_workflows": [
        {{
            "workflow_name": "ชื่อ Workflow",
            "description": "คำอธิบาย",
            "trigger": "สิ่งที่เริ่มต้น workflow",
            "steps": [
                {{
                    "step": 1,
                    "actor": "ใครเป็นคนทำ",
                    "action": "ทำอะไร",
                    "input": "ข้อมูลที่ต้องใส่",
                    "output": "ผลลัพธ์ที่ได้",
                    "validation": "การตรวจสอบ",
                    "error_handling": "จัดการข้อผิดพลาด"
                }}
            ],
            "success_criteria": ["เงื่อนไขความสำเร็จ"],
            "failure_scenarios": ["สถานการณ์ที่อาจล้มเหลว"]
        }}
    ]
}}

ออกแบบให้ครอบคลุมทุก use case และมีรายละเอียดที่ใช้งานได้จริง
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": journey_prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def design_app_architecture(self, requirements: Dict[str, Any], user_journey: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: ออกแบบ App Architecture และ Technical Specifications"""
        
        architecture_prompt = f"""
คุณเป็น Solution Architect ที่เชี่ยวชาญในการออกแบบระบบ

Requirements: {json.dumps(requirements, ensure_ascii=False, indent=2)}
User Journey: {json.dumps(user_journey, ensure_ascii=False, indent=2)}

โปรดออกแบบ App Architecture ใน JSON format:

{{
    "app_overview": {{
        "app_name": "ชื่อแอป",
        "app_type": "mobile/web/hybrid",
        "platform": ["iOS", "Android", "Web"],
        "tech_stack": {{
            "frontend": ["เทคโนโลยี frontend"],
            "backend": ["เทคโนโลจี backend"],
            "database": "ฐานข้อมูล",
            "cloud": "cloud services",
            "third_party": ["third party services"]
        }}
    }},
    "screens_structure": [
        {{
            "screen_name": "ชื่อหน้าจอ",
            "screen_type": "navigation/input/display/action",
            "description": "คำอธิบายหน้าจอ",
            "components": [
                {{
                    "component": "ชื่อ component",
                    "type": "button/input/list/card/etc",
                    "functionality": "ทำงานอะไร",
                    "data_needed": ["ข้อมูลที่ต้องใช้"],
                    "interactions": ["การโต้ตอบ"]
                }}
            ],
            "navigation": {{
                "from": ["มาจากหน้าไหนได้บ้าง"],
                "to": ["ไปหน้าไหนได้บ้าง"],
                "conditions": ["เงื่อนไขในการนำทาง"]
            }}
        }}
    ],
    "data_models": [
        {{
            "model_name": "ชื่อ Model",
            "description": "คำอธิบาย",
            "fields": [
                {{
                    "field": "ชื่อฟิลด์",
                    "type": "ประเภทข้อมูล",
                    "required": true/false,
                    "validation": "กฎการตรวจสอบ",
                    "description": "คำอธิบาย"
                }}
            ],
            "relationships": ["ความสัมพันธ์กับ model อื่น"]
        }}
    ],
    "api_endpoints": [
        {{
            "endpoint": "/api/path",
            "method": "GET/POST/PUT/DELETE",
            "description": "คำอธิบาย",
            "input": {{"field": "type"}},
            "output": {{"field": "type"}},
            "authentication": "required/optional/none",
            "validation": ["กฎการตรวจสอบ"]
        }}
    ],
    "features_priority": {{
        "mvp": ["ฟีเจอร์หลักที่จำเป็น"],
        "phase_2": ["ฟีเจอร์รุ่นที่ 2"],
        "nice_to_have": ["ฟีเจอร์เสริม"]
    }},
    "development_phases": [
        {{
            "phase": 1,
            "name": "ชื่อเฟส",
            "duration": "ระยะเวลา",
            "deliverables": ["สิ่งที่ส่งมอบ"],
            "dependencies": ["สิ่งที่ต้องรออะไรก่อน"],
            "risks": ["ความเสี่ยง"]
        }}
    ]
}}

ออกแบบให้ละเอียด สามารถนำไปพัฒนาได้จริง และมีลำดับความสำคัญที่ชัดเจน
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": architecture_prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def create_development_roadmap(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: สร้าง Development Roadmap และ Testing Strategy"""
        
        roadmap_prompt = f"""
คุณเป็น Project Manager และ QA Lead ที่มีประสบการณ์

Architecture: {json.dumps(architecture, ensure_ascii=False, indent=2)}

โปรดสร้าง Development Roadmap และ Testing Strategy ใน JSON format:

{{
    "development_roadmap": {{
        "total_timeline": "เวลารวม",
        "milestones": [
            {{
                "milestone": "ชื่อ milestone",
                "week": "สัปดาห์ที่",
                "deliverables": ["สิ่งที่ส่งมอบ"],
                "success_criteria": ["เกณฑ์ความสำเร็จ"],
                "demo_scenario": "สิ่งที่จะ demo"
            }}
        ]
    }},
    "testing_strategy": {{
        "unit_tests": [
            {{
                "component": "ส่วนที่ทดสอบ",
                "test_cases": ["test case 1", "test case 2"],
                "coverage_target": "เป้าหมาย coverage"
            }}
        ],
        "integration_tests": [
            {{
                "flow": "การทำงานที่ทดสอบ",
                "scenarios": ["สถานการณ์ทดสอบ"],
                "expected_results": ["ผลลัพธ์ที่คาดหวัง"]
            }}
        ],
        "user_acceptance_tests": [
            {{
                "user_story": "User story",
                "acceptance_criteria": ["เกณฑ์การยอมรับ"],
                "test_steps": ["ขั้นตอนการทดสอบ"]
            }}
        ]
    }},
    "deployment_plan": {{
        "environments": ["dev", "staging", "production"],
        "deployment_steps": ["ขั้นตอนการ deploy"],
        "rollback_plan": ["แผนการ rollback"],
        "monitoring": ["สิ่งที่ต้อง monitor"]
    }},
    "success_metrics": {{
        "technical": ["เมตริกทางเทคนิค"],
        "business": ["เมตริกทางธุรกิจ"],
        "user_experience": ["เมตริก UX"]
    }}
}}

วางแผนให้ครบถ้วน สามารถติดตามและควบคุมได้จริง
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": roadmap_prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def generate_complete_workflow(self, customer_input: str) -> Dict[str, Any]:
        """รวมทุกขั้นตอนเป็น Complete Workflow"""
        
        print("🔍 Step 1: Analyzing customer requirements...")
        requirements = self.analyze_customer_requirements(customer_input)
        
        print("🎯 Step 2: Designing user journey and workflows...")
        user_journey = self.design_user_journey(requirements)
        
        print("🏗️ Step 3: Creating app architecture...")
        architecture = self.design_app_architecture(requirements, user_journey)
        
        print("📋 Step 4: Building development roadmap...")
        roadmap = self.create_development_roadmap(architecture)
        
        # รวมทุกอย่างเป็น Complete Workflow
        complete_workflow = {
            "project_id": f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "customer_input": customer_input,
            "requirements_analysis": requirements,
            "user_journey_design": user_journey,
            "app_architecture": architecture,
            "development_roadmap": roadmap,
            "next_steps": [
                "Review และ approve workflow design",
                "เตรียม development environment",
                "เริ่มต้น Phase 1 development",
                "Setup CI/CD pipeline",
                "เริ่ม Unit testing"
            ]
        }
        
        return complete_workflow
    
    def save_workflow(self, workflow: Dict[str, Any], output_path: str = "workflows"):
        """บันทึก Workflow ลงไฟล์"""
        os.makedirs(output_path, exist_ok=True)
        
        project_id = workflow["project_id"]
        filename = f"{output_path}/{project_id}_complete_workflow.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Workflow saved to: {filename}")
        return filename

def main():
    """Test the Workflow Designer Agent"""
    
    # ตัวอย่างการใช้งาน
    agent = WorkflowDesignerAgent()
    
    customer_inputs = [
        "ต้องการสร้างแอป ร้านอาหาร ให้ลูกค้าสั่งอาหารออนไลน์ได้ และเจ้าของร้านดูออเดอร์",
        "สร้างระบบจัดการคลินิกสัตวแพทย์ มีนัดหมาย เวชระเบียน และบิล",
        "แอปฟิตเนส ให้คนออกกำลังกาย ติดตามผลการออกกำลังกาย และมี personal trainer"
    ]
    
    for i, customer_input in enumerate(customer_inputs, 1):
        print(f"\n{'='*50}")
        print(f"🚀 Example {i}: {customer_input}")
        print(f"{'='*50}")
        
        try:
            workflow = agent.generate_complete_workflow(customer_input)
            filename = agent.save_workflow(workflow)
            
            print(f"\n📊 Workflow Summary:")
            print(f"Project ID: {workflow['project_id']}")
            print(f"Business Type: {workflow['requirements_analysis']['business_type']}")
            print(f"App Type: {workflow['app_architecture']['app_overview']['app_type']}")
            print(f"Total Screens: {len(workflow['app_architecture']['screens_structure'])}")
            print(f"Development Phases: {len(workflow['development_roadmap']['development_roadmap']['milestones'])}")
            print(f"Saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()