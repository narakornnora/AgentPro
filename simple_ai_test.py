#!/usr/bin/env python
# Simple AI mobile app generation test

import requests
import json
import time

def test_ai_mobile_generation():
    """Test AI-powered mobile app generation"""
    
    # ให้เวลา backend เริ่มต้น
    print("🚀 Testing AI Mobile App Generation...")
    
    try:
        # ทดสอบ health check ก่อน
        health_response = requests.get('http://localhost:8001/health', timeout=5)
        if health_response.status_code != 200:
            print(f"❌ Backend not ready: {health_response.status_code}")
            return False
        
        print("✅ Backend is healthy")
        
        # ทดสอบ mobile app generation
        response = requests.post('http://localhost:8001/api/mobile-app', 
            headers={'Content-Type': 'application/json'},
            json={
                "message": "สร้าง app ร้านกาแฟ ออนไลน์ มี หน้าเมนู หน้าตะกร้า หน้าชำระเงิน",
                "app_type": "react_native",
                "features": ["เมนูสินค้า", "ตะกร้าสินค้า", "ระบบชำระเงิน"]
            },
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("🎉 AI Generated Mobile App Successfully!")
                print(f"App Type: {result.get('app_type')}")
                print(f"Project Path: {result.get('project_path')}")
                print(f"Files Created: {result.get('files_created')}")
                
                # ตรวจสอบไฟล์ที่สร้างขึ้น
                if result.get('project_path'):
                    import os
                    app_tsx_path = os.path.join(result['project_path'], 'App.tsx')
                    if os.path.exists(app_tsx_path):
                        with open(app_tsx_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if 'กาแฟ' in content or 'coffee' in content.lower():
                                print("✅ AI Generated Custom Content!")
                                print("Sample content:", content[:200] + "...")
                                return True
                            else:
                                print("⚠️ Content may be generic template")
                                return False
                    else:
                        print("❌ App.tsx file not found")
                        return False
                else:
                    print("❌ No project path returned")
                    return False
            else:
                print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_mobile_generation()
    
    if success:
        print("\n🎉 RESULT: AI สามารถสร้างโค้ดจริง ๆ ได้!")
    else:
        print("\n❌ RESULT: AI ยังไม่สามารถสร้างโค้ดที่ customize ได้จริง")