#!/usr/bin/env python
# Test script to verify AI code generation capabilities

import requests
import json

def test_ai_mobile_generation():
    """Test if AI can actually generate mobile app code"""
    
    try:
        # Test mobile app generation using correct endpoint
        response = requests.post('http://localhost:8001/api/mobile-app', 
            headers={'Content-Type': 'application/json'},
            json={
                "message": "สร้าง mobile app ร้านกาแฟ สำหรับ order online ต้องมี หน้าเมนู หน้าตะกร้า หน้า payment ใช้ React Native",
                "app_type": "react_native",
                "features": ["เมนูสินค้า", "ตะกร้าสินค้า", "ระบบชำระเงิน", "การสั่งซื้อ"]
            })
        
        print("Status Code:", response.status_code)
        print("Response:", response.text[:500])
        
        if response.status_code == 200:
            result = response.json()
            print("Response Keys:", result.keys())
            
            if result.get('success') and result.get('files_created', 0) > 0:
                print("\n✅ AI Generated Real Mobile App!")
                print(f"App Type: {result.get('app_type')}")
                print(f"Project Name: {result.get('project_name')}")
                print(f"Files Created: {result.get('files_created')}")
                print(f"Project Path: {result.get('project_path')}")
                return True
            else:
                print("\n❌ Mobile App Generation Failed")
                print(f"Error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"\n❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ai_web_generation():
    """Test web app generation"""
    
    try:
        response = requests.post('http://localhost:8001/chat/ai', 
            headers={'Content-Type': 'application/json'},
            json={
                "message": "สร้างเว็บ e-commerce ขายเสื้อผ้า มี shopping cart, user login, payment gateway"
            })
        
        print("\n=== Web App Test ===")
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            result = response.json()
            print("Web Response Keys:", result.keys())
            
            if result.get('ok') and len(result.get('files', [])) > 0:
                print("✅ AI Generated Web App!")
                print(f"Slug: {result.get('slug')}")
                print(f"Web URL: {result.get('web_url')}")
                print(f"Files Created: {len(result.get('files'))}")
                print("Files:", result.get('files'))
                return True
            else:
                print("❌ Web App Generation Failed")
                return False
        else:
            print(f"❌ Web API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Web Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AI Code Generation Capabilities")
    print("=" * 50)
    
    # Test mobile generation
    mobile_success = test_ai_mobile_generation()
    
    # Test web generation  
    web_success = test_ai_web_generation()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"Mobile App Generation: {'✅ PASS' if mobile_success else '❌ FAIL'}")
    print(f"Web App Generation: {'✅ PASS' if web_success else '❌ FAIL'}")
    
    if mobile_success and web_success:
        print("\n🎉 AI CAN ACTUALLY CODE!")
    else:
        print("\n⚠️ AI CAPABILITIES LIMITED - NEEDS IMPROVEMENT")