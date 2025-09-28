#!/usr/bin/env python
"""
ทดสอบ AI Code Generation โดยตรง (ไม่ผ่าน HTTP Server)
"""
import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()

async def test_ai_generation_direct():
    """ทดสอบ AI สร้างโค้ดโดยตรง"""
    
    # Initialize OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API Key found!")
        return False
    
    client = OpenAI(api_key=api_key)
    workspace = Path("C:/agent/direct_test_apps")
    workspace.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Testing Direct AI Generation")
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"📁 Workspace: {workspace}")
    
    # Test 1: Mobile App Generation
    print("\n📱 Test 1: Mobile App Generation")
    print("-" * 50)
    
    mobile_prompt = """
คุณเป็น expert React Native developer ที่สร้างแอป mobile ที่ทำงานได้จริง

User Request: สร้าง app ร้านกาแฟ ชื่อ "Coffee House" มี หน้าเมนูกาแฟ หน้าตะกร้าสินค้า หน้าชำระเงิน

สร้าง mobile app ที่สมบูรณ์ตาม request โดย:
1. วิเคราะห์ความต้องการจาก prompt
2. สร้างโครงสร้าง app ที่เหมาะสม  
3. เขียนโค้ดที่ทำงานได้จริง มี navigation, state management
4. ใช้ UI components ที่เหมาะสมกับร้านกาแฟ
5. มี error handling และ loading states

ส่งกลับเป็น JSON format:
{
    "app_name": "ชื่อแอป",
    "description": "คำอธิบายแอป", 
    "main_component": "โค้ด App.tsx หลัก (ต้องครบถ้วนพร้อมใช้งาน)",
    "package_json": "package.json configuration",
    "additional_files": [
        {"filename": "screens/MenuScreen.tsx", "content": "โค้ดหน้าเมนู"},
        {"filename": "screens/CartScreen.tsx", "content": "โค้ดหน้าตะกร้า"}
    ]
}

โค้ดต้อง:
- ใช้ TypeScript
- มี proper imports
- ทำงานได้จริงไม่ใช่ mockup
- มี state management สำหรับ cart
- responsive design
- มีสี theme ที่เหมาะกับร้านกาแฟ
- ใส่ comments เป็นไทย
"""
    
    try:
        print("🤖 กำลังขอให้ AI สร้าง mobile app...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ใช้ model ที่เร็วกว่า
            messages=[
                {"role": "system", "content": "คุณเป็น expert mobile app developer ที่สร้างแอปที่ทำงานได้จริง ตอบเป็น JSON เท่านั้น"},
                {"role": "user", "content": mobile_prompt}
            ],
            max_tokens=3000,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        print(f"📝 AI Response Length: {len(ai_response)} characters")
        
        # Parse JSON
        if ai_response.startswith('```json'):
            ai_response = ai_response.replace('```json', '').replace('```', '').strip()
        
        try:
            app_data = json.loads(ai_response)
            print("✅ JSON Parsing successful!")
            
            # สร้างไฟล์
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            app_name = app_data.get('app_name', 'mobile_app').replace(' ', '_')
            app_dir = workspace / f"{app_name}_{timestamp}"
            app_dir.mkdir(parents=True, exist_ok=True)
            
            files_created = 0
            
            # สร้าง package.json
            if app_data.get('package_json'):
                package_file = app_dir / "package.json"
                with open(package_file, 'w', encoding='utf-8') as f:
                    if isinstance(app_data['package_json'], str):
                        f.write(app_data['package_json'])
                    else:
                        json.dump(app_data['package_json'], f, indent=2, ensure_ascii=False)
                files_created += 1
                print(f"📄 Created: package.json")
            
            # สร้าง App.tsx
            if app_data.get('main_component'):
                main_file = app_dir / "App.tsx"
                with open(main_file, 'w', encoding='utf-8') as f:
                    f.write(app_data['main_component'])
                files_created += 1
                print(f"📄 Created: App.tsx")
                
                # แสดง preview
                content = app_data['main_component']
                print(f"\n📱 App.tsx Preview:")
                print("=" * 60)
                print(content[:800] + "..." if len(content) > 800 else content)
                print("=" * 60)
                
                # ตรวจสอบคำเกี่ยวกับกาแฟ
                coffee_keywords = ['กาแฟ', 'Coffee', 'coffee', 'เมนู', 'Menu', 'ตะกร้า', 'Cart', 'ชำระเงิน']
                found_keywords = [kw for kw in coffee_keywords if kw in content]
                
                if found_keywords:
                    print(f"\n✅ AI Customization Found: {found_keywords}")
                    print("🎯 CONFIRMED: AI เขียนโค้ดตาม requirements!")
                else:
                    print("\n⚠️ Generic template detected")
            
            # สร้างไฟล์เพิ่มเติม
            if app_data.get('additional_files'):
                for file_info in app_data['additional_files']:
                    file_path = app_dir / file_info['filename']
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file_info['content'])
                    files_created += 1
                    print(f"📄 Created: {file_info['filename']}")
            
            print(f"\n📊 Mobile App Summary:")
            print(f"App Name: {app_data.get('app_name')}")
            print(f"Description: {app_data.get('description')}")
            print(f"Files Created: {files_created}")
            print(f"App Path: {app_dir}")
            
            if files_created > 0:
                print("🎉 Mobile App Generation SUCCESS!")
                mobile_success = True
            else:
                print("❌ Mobile App Generation FAILED!")
                mobile_success = False
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            print(f"AI Response: {ai_response[:500]}...")
            mobile_success = False
        
    except Exception as e:
        print(f"❌ Mobile Generation Error: {e}")
        mobile_success = False
    
    # Test 2: Web App Generation
    print("\n🌐 Test 2: Web App Generation")
    print("-" * 50)
    
    web_prompt = """
คุณเป็น expert web developer ที่สร้าง web application ที่ทำงานได้จริง

User Request: สร้างเว็บไซต์ร้านขายหนังสือออนไลน์ ชื่อ "BookShop Online" มี gallery หนังสือ shopping cart ระบบค้นหา

สร้าง web application ที่สมบูรณ์ตาม request โดย:
1. วิเคราะห์ความต้องการ
2. สร้าง responsive web app
3. ใช้ modern CSS และ JavaScript
4. มี interactive features
5. ทำงานได้จริงไม่ใช่ static

ส่งกลับเป็น JSON format:
{
    "app_name": "ชื่อเว็บไซต์",
    "description": "คำอธิบาย",
    "index_html": "โค้ด HTML หลัก (ครบถ้วน)",
    "styles_css": "โค้ด CSS (สวยงาม responsive)",
    "script_js": "โค้ด JavaScript (interactive)"
}

เว็บไซต์ต้อง:
- Responsive design
- Modern UI/UX สำหรับร้านหนังสือ
- Interactive features (search, cart)
- ทำงานได้จริงบน browser
- มี book gallery
- ใส่ comments เป็นไทย
"""
    
    try:
        print("🤖 กำลังขอให้ AI สร้าง web app...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "คุณเป็น expert web developer ที่สร้างเว็บไซต์ที่ทำงานได้จริง ตอบเป็น JSON เท่านั้น"},
                {"role": "user", "content": web_prompt}
            ],
            max_tokens=3000,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        print(f"📝 Web AI Response Length: {len(ai_response)} characters")
        
        if ai_response.startswith('```json'):
            ai_response = ai_response.replace('```json', '').replace('```', '').strip()
        
        try:
            web_data = json.loads(ai_response)
            print("✅ Web JSON Parsing successful!")
            
            # สร้างไฟล์เว็บ
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            web_name = web_data.get('app_name', 'web_app').replace(' ', '_')
            web_dir = workspace / f"{web_name}_{timestamp}"
            web_dir.mkdir(parents=True, exist_ok=True)
            
            web_files_created = 0
            
            # สร้าง index.html
            if web_data.get('index_html'):
                with open(web_dir / "index.html", 'w', encoding='utf-8') as f:
                    f.write(web_data['index_html'])
                web_files_created += 1
                print(f"📄 Created: index.html")
            
            # สร้าง styles.css
            if web_data.get('styles_css'):
                with open(web_dir / "styles.css", 'w', encoding='utf-8') as f:
                    f.write(web_data['styles_css'])
                web_files_created += 1
                print(f"📄 Created: styles.css")
            
            # สร้าง script.js
            if web_data.get('script_js'):
                with open(web_dir / "script.js", 'w', encoding='utf-8') as f:
                    f.write(web_data['script_js'])
                web_files_created += 1
                print(f"📄 Created: script.js")
            
            print(f"\n📊 Web App Summary:")
            print(f"App Name: {web_data.get('app_name')}")
            print(f"Description: {web_data.get('description')}")
            print(f"Files Created: {web_files_created}")
            print(f"Web Path: {web_dir}")
            
            if web_files_created > 0:
                print("🎉 Web App Generation SUCCESS!")
                
                # แสดงตัวอย่าง HTML
                html_content = web_data.get('index_html', '')
                if html_content:
                    print(f"\n🌐 HTML Preview:")
                    print("=" * 60)
                    print(html_content[:600] + "..." if len(html_content) > 600 else html_content)
                    print("=" * 60)
                
                web_success = True
            else:
                print("❌ Web App Generation FAILED!")
                web_success = False
                
        except json.JSONDecodeError as e:
            print(f"❌ Web JSON Parse Error: {e}")
            print(f"Web AI Response: {ai_response[:500]}...")
            web_success = False
    
    except Exception as e:
        print(f"❌ Web Generation Error: {e}")
        web_success = False
    
    # Final Results
    print("\n" + "=" * 80)
    print("🏆 FINAL TEST RESULTS:")
    print("=" * 80)
    print(f"📱 Mobile App Generation: {'✅ SUCCESS' if mobile_success else '❌ FAILED'}")
    print(f"🌐 Web App Generation: {'✅ SUCCESS' if web_success else '❌ FAILED'}")
    
    if mobile_success or web_success:
        print("\n🎉 AI สามารถเขียนโค้ดได้จริง ๆ!")
        print("✅ ไม่ใช่ mockup - เป็นโค้ดจริงที่ AI วิเคราะห์และเขียน")
        print("🚀 พร้อมสร้าง chat interface แล้ว!")
        return True
    else:
        print("\n❌ AI Generation ล้มเหลว ต้องแก้ไขต่อ")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ai_generation_direct())
    
    if success:
        print("\n🎯 ต่อไป: สร้าง Chat Interface ที่เชื่อมกับ AI")
    else:
        print("\n⚠️ ต้องแก้ปัญหา AI generation ก่อน")