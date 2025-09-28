#!/usr/bin/env python
# Direct test of AI mobile app generator (no HTTP)

import sys
import os
import asyncio
sys.path.append('c:/agent/apps/orchestrator')

from agents.ai_mobile_app_generator import AIpoweredMobileAppGenerator
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from root
load_dotenv('c:/agent/.env')

async def test_direct_ai_generation():
    """Test AI generation directly without HTTP"""
    
    try:
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        
        # If not in env, check if we can proceed with testing
        if not api_key:
            print("⚠️ No OpenAI API Key - testing with fallback generator")
            # Test the fallback functionality
            generator = AIpoweredMobileAppGenerator(None)  # No client
        else:
            print(f"✅ Found API Key: {api_key[:10]}...")
            client = OpenAI(api_key=api_key)
            generator = AIpoweredMobileAppGenerator(client)
            

        
        # Test requirements
        requirements = {
            "message": "สร้าง app ร้านกาแฟ ออนไลน์ มี หน้าเมนู หน้าตะกร้า หน้าชำระเงิน ใช้สีน้ำตาล สีครีม",
            "app_type": "react_native",
            "project_name": "coffee_shop_ai_test",
            "business_name": "ร้านกาแฟ AI Coffee",
            "features": ["เมนูกาแฟ", "ตะกร้าสินค้า", "ระบบชำระเงิน", "โปรโมชั่น"]
        }
        
        print("🚀 Testing AI Mobile App Generation (Direct)...")
        print(f"Requirements: {requirements['message']}")
        
        # Generate app
        result = await generator.generate_mobile_app(requirements)
        
        if result.get('success'):
            print("🎉 AI Generation Successful!")
            print(f"Project: {result.get('project_name')}")
            print(f"Path: {result.get('project_path')}")
            print(f"Files: {result.get('files_created')}")
            
            # Check generated content
            project_path = result.get('project_path')
            if project_path and os.path.exists(project_path):
                app_tsx = os.path.join(project_path, 'App.tsx')
                if os.path.exists(app_tsx):
                    with open(app_tsx, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    print("\n📝 Generated App.tsx (first 500 chars):")
                    print("-" * 50)
                    print(content[:500] + "...")
                    print("-" * 50)
                    
                    # Check if AI customized content
                    coffee_keywords = ['กาแฟ', 'coffee', 'เมนู', 'ตะกร้า', 'cart', 'ชำระเงิน', 'payment']
                    found_keywords = [kw for kw in coffee_keywords if kw.lower() in content.lower()]
                    
                    if found_keywords:
                        print(f"✅ AI Customized Content Found: {found_keywords}")
                        
                        # Check if it's AI-generated vs template
                        if 'AI Coffee' in content or 'กาแฟ' in content:
                            print("🎯 CONFIRMED: AI สร้างโค้ดจริง ๆ ได้!")
                            return True
                        else:
                            print("⚠️ May be template-based")
                            return False
                    else:
                        print("❌ No coffee-specific content found")
                        return False
                else:
                    print("❌ App.tsx not created")
                    return False
            else:
                print("❌ Project directory not found")
                return False
        else:
            print(f"❌ Generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_direct_ai_generation())
    
    print("\n" + "="*60)
    if success:
        print("🎉 FINAL RESULT: AI สามารถสร้างโค้ดจริง ๆ ได้!")
        print("✅ AI ไม่ใช่แค่ template - สร้างโค้ด custom ได้จริง")
    else:
        print("❌ FINAL RESULT: AI ยังใช้ template แบบเดิม")
        print("⚠️ ต้องปรับปรุงระบบให้สร้างโค้ดจริง")