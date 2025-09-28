#!/usr/bin/env python
# Quick test of fixed backend

import requests
import json

def test_fixed_backend():
    """ทดสอบ backend ที่แก้ไข JSON parsing แล้ว"""
    
    try:
        # Test health check
        health = requests.get('http://localhost:8001/health')
        print(f"Health Status: {health.status_code}")
        
        if health.status_code == 200:
            print("✅ Backend is running")
            
            # Test mobile app generation
            print("\n🤖 Testing AI mobile app generation...")
            
            response = requests.post('http://localhost:8001/chat',
                headers={'Content-Type': 'application/json'},
                json={
                    "message": "สร้าง app ร้านขายกาแฟ ชื่อ Coffee Paradise มี หน้าเมนู หน้าตะกร้า หน้าชำระเงิน",
                    "app_type": "mobile",
                    "framework": "react_native"
                },
                timeout=60
            )
            
            print(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n📱 AI Response:")
                print(f"Success: {result.get('success')}")
                print(f"Message: {result.get('message')}")
                print(f"App Name: {result.get('app_name')}")
                print(f"Files Created: {result.get('files_created')}")
                
                if result.get('success'):
                    print("🎉 AI สร้างแอปสำเร็จ! JSON parsing ทำงานแล้ว")
                    
                    # Test web app too
                    print("\n🌐 Testing web app generation...")
                    
                    web_response = requests.post('http://localhost:8001/chat',
                        headers={'Content-Type': 'application/json'},
                        json={
                            "message": "สร้างเว็บไซต์ร้านขายหนังสือออนไลน์ มี search gallery cart",
                            "app_type": "web",
                            "framework": "react"
                        },
                        timeout=60
                    )
                    
                    if web_response.status_code == 200:
                        web_result = web_response.json()
                        print(f"Web Success: {web_result.get('success')}")
                        print(f"Web App: {web_result.get('app_name')}")
                        
                        if web_result.get('success'):
                            print("🎉 ทั้ง Mobile และ Web Apps สร้างได้แล้ว!")
                            return True
                        else:
                            print(f"❌ Web generation failed: {web_result.get('error')}")
                    else:
                        print(f"❌ Web request failed: {web_response.status_code}")
                else:
                    print(f"❌ Mobile generation failed: {result.get('error')}")
            else:
                print(f"❌ Mobile request failed: {response.status_code}")
                print(f"Response: {response.text}")
        else:
            print("❌ Backend not responding")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
    return False

if __name__ == "__main__":
    success = test_fixed_backend()
    
    if success:
        print("\n🎯 System is working! Go to http://localhost:8001 and try it!")
    else:
        print("\n⚠️ System needs more fixes")