#!/usr/bin/env python3
"""
🧪 AI Expert Consultant Test Suite
ทดสอบการทำงานของระบบ AI Expert ในโหมดต่างๆ
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from ai_chat_backend import ai_expert_consultant

async def test_expert_recommendations():
    """ทดสอบการแนะนำ Libraries และ Tech Stack"""
    
    print("🧪 Testing Expert Recommendations...")
    
    test_cases = [
        {
            "input": "แนะนำ UI library สำหรับ React หน่อย",
            "expected_type": "recommendation"
        },
        {
            "input": "อยากได้ color palette สวยๆ สำหรับแอป E-commerce",  
            "expected_type": "design_advice"
        },
        {
            "input": "ช่วยดู React component นี้หน่อย",
            "expected_type": "code_review" 
        },
        {
            "input": "สร้างเว็บแอปร้านกาแฟ มี login order payment",
            "expected_type": "project_analysis"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {test['input']}")
        
        try:
            result = await ai_expert_consultant(test['input'], "analyze")
            
            print(f"✅ Success!")
            print(f"Consultation Type: {result.get('consultation_type', 'N/A')}")
            print(f"Response Mode: {result.get('response_mode', 'N/A')}")
            print(f"Ready to Build: {result.get('ready_to_build', False)}")
            print(f"Needs More Info: {result.get('needs_more_info', False)}")
            
            if result.get('expert_recommendations'):
                print("💡 Expert Recommendations:")
                for rec in result['expert_recommendations'][:3]:
                    print(f"  • {rec}")
            
            if result.get('expert_analysis', {}).get('modern_libraries'):
                print("📚 Modern Libraries:")
                for lib in result['expert_analysis']['modern_libraries'][:3]:
                    print(f"  • {lib}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_code_review():
    """ทดสอบการ Code Review"""
    
    print("\n🧪 Testing Code Review...")
    
    code_examples = [
        {
            "input": "ช่วยดู code นี้หน่อย: function add(a, b) { return a + b; }",
            "type": "simple_function"
        },
        {
            "input": "ช่วยปรับปรุง React component นี้ให้ดีกว่าเดิม",
            "type": "react_component"  
        }
    ]
    
    for example in code_examples:
        print(f"\nTesting: {example['type']}")
        try:
            result = await ai_expert_consultant(example['input'], "analyze")
            
            if result.get('code_suggestions'):
                suggestions = result['code_suggestions']
                print("🔧 Code Suggestions:")
                
                if suggestions.get('improvements'):
                    print("  Improvements:")
                    for imp in suggestions['improvements'][:2]:
                        print(f"    • {imp}")
                
                if suggestions.get('best_practices'):
                    print("  Best Practices:")
                    for bp in suggestions['best_practices'][:2]:
                        print(f"    • {bp}")
                        
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_ui_design_advice():
    """ทดสอบการแนะนำ Design"""
    
    print("\n🧪 Testing UI Design Advice...")
    
    design_questions = [
        "แนะนำสีสำหรับแอป Banking",
        "อยากได้ typography ที่ดูโมเดิร์น", 
        "ช่วยออกแบบ button สวยๆ"
    ]
    
    for question in design_questions:
        print(f"\nQuestion: {question}")
        try:
            result = await ai_expert_consultant(question, "analyze")
            
            if result.get('expert_analysis', {}).get('design_system'):
                design = result['expert_analysis']['design_system']
                print("🎨 Design System:")
                for key, value in design.items():
                    if isinstance(value, str):
                        print(f"  {key}: {value}")
                        
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """รันการทดสอบทั้งหมด"""
    
    print("🧠 AI Expert Consultant Test Suite")
    print("=" * 50)
    
    try:
        await test_expert_recommendations()
        await test_code_review() 
        await test_ui_design_advice()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        print("\n💡 Next Steps:")
        print("1. เปิด http://localhost:8000/ai_expert_demo.html")
        print("2. คลิก 'เริ่มคุยกับ AI Expert'")
        print("3. ลองพิมพ์คำถามต่างๆ")
        
    except Exception as e:
        print(f"\n❌ Test Suite Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())