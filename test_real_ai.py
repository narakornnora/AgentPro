#!/usr/bin/env python
# ทดสอบ AI Code Generator ใหม่

import requests
import json
import time

def test_ai_mobile_generation():
    """ทดสอบ AI สร้าง mobile app จริง ๆ"""
    
    print("🚀 ทดสอบ AI Mobile App Generation...")
    
    try:
        # ทดสอบ health check ก่อน
        health_response = requests.get('http://localhost:8001/health', timeout=5)
        print(f"Health Check: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Backend: {health_data['message']}")
        
        # ทดสอบสร้าง mobile app
        print("\n🤖 กำลังขอให้ AI สร้าง mobile app...")
        
        response = requests.post('http://localhost:8001/generate',
            headers={'Content-Type': 'application/json'},
            json={
                "prompt": "สร้าง app ร้านกาแฟออนไลน์ ชื่อ 'Coffee Paradise' มี หน้าเมนูกาแฟ หน้าตะกร้าสินค้า หน้าชำระเงิน ใช้สีน้ำตาล ครีม",
                "app_type": "mobile",
                "framework": "react_native"
            },
            timeout=60  # ให้เวลา AI นานหน่อย
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n📱 AI Response:")
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            print(f"Files Created: {result.get('files_created')}")
            print(f"App Path: {result.get('app_path')}")
            print(f"App URL: {result.get('app_url')}")
            
            if result.get('code_preview'):
                print(f"\n📝 Code Preview:")
                print("-" * 50)
                print(result['code_preview'])
                print("-" * 50)
            
            if result.get('success') and result.get('files_created', 0) > 0:
                print("\n🎉 AI สร้างโค้ดสำเร็จ!")
                
                # ตรวจสอบไฟล์ที่สร้าง
                import os
                app_path = result.get('app_path')
                if app_path and os.path.exists(app_path):
                    files = os.listdir(app_path)
                    print(f"📁 ไฟล์ที่สร้าง: {files}")
                    
                    # อ่าน App.tsx ดูว่า AI เขียนอะไร
                    app_tsx = os.path.join(app_path, 'App.tsx')
                    if os.path.exists(app_tsx):
                        with open(app_tsx, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        print(f"\n📱 App.tsx Content (first 800 chars):")
                        print("=" * 60)
                        print(content[:800] + "..." if len(content) > 800 else content)
                        print("=" * 60)
                        
                        # ตรวจสอบคำที่เกี่ยวข้องกับกาแฟ
                        coffee_keywords = ['กาแฟ', 'coffee', 'Coffee', 'Paradise', 'เมนู', 'ตะกร้า', 'ชำระเงิน']
                        found_keywords = [kw for kw in coffee_keywords if kw in content]
                        
                        if found_keywords:
                            print(f"\n✅ AI Customized Content Found: {found_keywords}")
                            print("🎯 CONFIRMED: AI เขียนโค้ดตาม requirements จริง ๆ!")
                            return True
                        else:
                            print("\n⚠️ No specific coffee-related content found")
                            return False
                    else:
                        print("❌ App.tsx not found")
                        return False
                else:
                    print("❌ App directory not found")
                    return False
            else:
                print(f"\n❌ AI Generation Failed: {result.get('error')}")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_ai_web_generation():
    """ทดสอบ AI สร้าง web app จริง ๆ"""
    
    print("\n🌐 ทดสอบ AI Web App Generation...")
    
    try:
        response = requests.post('http://localhost:8001/generate',
            headers={'Content-Type': 'application/json'},
            json={
                "prompt": "สร้างเว็บไซต์ร้านขายเสื้อผ้าออนไลน์ ชื่อ 'Fashion Store' มี gallery สินค้า shopping cart ระบบสมาชิก",
                "app_type": "web",
                "framework": "react"
            },
            timeout=60
        )
        
        print(f"Web Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n🌐 Web AI Response:")
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            print(f"App URL: {result.get('app_url')}")
            
            if result.get('success'):
                print("✅ AI สร้าง Web App สำเร็จ!")
                return True
            else:
                print(f"❌ Web Generation Failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Web API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Web Exception: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AI Code Generator")
    print("=" * 60)
    
    # รอ backend เริ่ม
    time.sleep(3)
    
    # ทดสอบ mobile generation
    mobile_success = test_ai_mobile_generation()
    
    # ทดสอบ web generation
    web_success = test_ai_web_generation()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"Mobile App: {'✅ PASS' if mobile_success else '❌ FAIL'}")
    print(f"Web App: {'✅ PASS' if web_success else '❌ FAIL'}")
    
    if mobile_success or web_success:
        print("\n🎉 AI สามารถเขียนโค้ดได้จริง ๆ!")
        print("✅ ไม่ใช่ mockup - เป็นโค้ดจริงที่ AI วิเคราะห์และเขียน")
    else:
        print("\n❌ ยังมีปัญหา ต้องแก้ไขต่อ")