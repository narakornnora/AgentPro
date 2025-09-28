#!/usr/bin/env python
# Test AI Web Generation - Real-time testing

import requests
import json
import time
import os
import webbrowser
from pathlib import Path

def test_ai_web_generation():
    """Test AI web generation and open result"""
    
    print("🚀 Testing AI Web Generation...")
    
    try:
        # Test different types of websites
        test_cases = [
            {
                "name": "Coffee Shop",
                "message": "สร้างเว็บไซต์ร้านกาแฟ ใช้สีน้ำตาล ครีม มีหน้าเมนู แกลเลอรี่ ติดต่อ"
            },
            {
                "name": "Fashion Boutique", 
                "message": "สร้างเว็บไซต์ร้านเสื้อผ้า แฟชั่น สีชมพู ทอง มีหน้าสินค้า โปรโมชั่น"
            },
            {
                "name": "Tech Startup",
                "message": "สร้างเว็บไซต์บริษัทเทคโนโลยี สีน้ำเงิน เทา มี landing page about us services"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test {i}: {test_case['name']} ---")
            
            # Send request to AI
            response = requests.post('http://localhost:8001/chat/ai',
                headers={'Content-Type': 'application/json'},
                json={"message": test_case['message']},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Generated: {result.get('slug')}")
                print(f"📁 Files: {len(result.get('files', []))}")
                
                # Open in browser for visual inspection
                web_url = f"http://localhost:8001{result.get('web_url')}"
                print(f"🌐 Opening: {web_url}")
                
                # Wait a bit then open browser
                time.sleep(2)
                webbrowser.open(web_url)
                
                # Ask user to verify
                user_check = input(f"✋ Please check the website for {test_case['name']}. Is it a proper {test_case['name'].lower()} website? (y/n): ")
                
                if user_check.lower() == 'y':
                    print(f"✅ {test_case['name']} website passed!")
                else:
                    print(f"❌ {test_case['name']} website failed - needs improvement")
                    return False
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        
        print("\n🎉 All web generation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_mobile_app_generation():
    """Test mobile app generation"""
    
    print("\n🚀 Testing Mobile App Generation...")
    
    try:
        response = requests.post('http://localhost:8001/api/mobile-app',
            headers={'Content-Type': 'application/json'},
            json={
                "message": "สร้าง mobile app ร้านอาหาร มีหน้าเมนู ออเดอร์ ชำระเงิน แผนที่",
                "app_type": "react_native", 
                "features": ["เมนูอาหาร", "การสั่งซื้อ", "ชำระเงิน", "แผนที่ร้าน"]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print(f"✅ Mobile App Generated!")
                print(f"📱 Project: {result.get('project_name')}")
                print(f"📁 Path: {result.get('project_path')}")
                print(f"📄 Files: {result.get('files_created')}")
                
                # Check if files actually exist
                project_path = result.get('project_path')
                if project_path and os.path.exists(project_path):
                    print(f"✅ Project directory exists: {project_path}")
                    
                    # List created files
                    files = list(Path(project_path).iterdir())
                    print(f"📋 Created files: {[f.name for f in files]}")
                    
                    return True
                else:
                    print("❌ Project directory not found")
                    return False
            else:
                print(f"❌ Mobile generation failed: {result.get('error')}")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_health_check():
    """Test if backend is running"""
    try:
        response = requests.get('http://localhost:8001/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not running: {e}")
        return False

if __name__ == "__main__":
    print("🧪 AgentPro AI Generation Testing")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Backend not ready - exiting")
        exit(1)
    
    # Test 2: Web generation
    web_success = test_ai_web_generation()
    
    # Test 3: Mobile generation  
    mobile_success = test_mobile_app_generation()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"Web Generation: {'✅ PASS' if web_success else '❌ FAIL'}")
    print(f"Mobile Generation: {'✅ PASS' if mobile_success else '❌ FAIL'}")
    
    if web_success and mobile_success:
        print("\n🎉 ALL TESTS PASSED - AI CAN CREATE REAL APPS!")
    else:
        print("\n⚠️ SOME TESTS FAILED - SYSTEM NEEDS IMPROVEMENT")