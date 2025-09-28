#!/usr/bin/env python3
"""
🧪 Test Full-Stack App Generation
ทดสอบว่าระบบสร้าง Full-Stack App จริงหรือไม่
"""

import asyncio
import json
import requests
from pathlib import Path

async def test_fullstack_generation():
    """ทดสอบการสร้าง Full-Stack App"""
    
    print("🧪 Testing Full-Stack App Generation...")
    print("=" * 50)
    
    test_cases = [
        {
            "input": "สร้างร้านกาแฟออนไลน์ มี login สั่งกาแฟ ชำระเงิน",
            "expected_files": ["database.py", "main.py", "auth.py", "requirements.txt", "index.html", "start_app.bat"],
            "expected_features": ["SQLite Database", "Flask API", "Authentication", "CRUD Operations"]
        },
        {
            "input": "สร้างระบบคลินิก มี นัดหมาย คนไข้ หมอ",
            "expected_files": ["database.py", "main.py", "requirements.txt", "index.html"],
            "expected_features": ["Database", "Backend", "Frontend"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"📝 Input: {test['input']}")
        
        try:
            # Call backend API
            response = requests.post('http://localhost:8001/chat', json={
                "message": test['input'],
                "app_type": "auto",
                "framework": "auto"
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ API Response Success!")
                print(f"📁 App Name: {result.get('app_name', 'N/A')}")
                print(f"📂 App Path: {result.get('app_path', 'N/A')}")
                print(f"📄 Files Created: {result.get('files_created', 0)}")
                
                # Check if files actually exist
                if result.get('app_path'):
                    app_dir = Path(result['app_path'])
                    if app_dir.exists():
                        created_files = [f.name for f in app_dir.iterdir() if f.is_file()]
                        print(f"📋 Actual Files: {created_files}")
                        
                        # Check for expected files
                        missing_files = []
                        for expected_file in test['expected_files']:
                            if expected_file not in created_files:
                                missing_files.append(expected_file)
                        
                        if missing_files:
                            print(f"❌ Missing Files: {missing_files}")
                        else:
                            print(f"✅ All Expected Files Created!")
                            
                        # Check specific files content
                        database_file = app_dir / "database.py"
                        main_file = app_dir / "main.py"
                        
                        if database_file.exists():
                            content = database_file.read_text(encoding='utf-8')
                            if "CREATE TABLE" in content and "sqlite3" in content:
                                print("✅ database.py: Contains real SQL!")
                            else:
                                print("❌ database.py: No real SQL found!")
                        
                        if main_file.exists():
                            content = main_file.read_text(encoding='utf-8')
                            if "Flask" in content or "FastAPI" in content:
                                print("✅ main.py: Contains real backend!")
                            else:
                                print("❌ main.py: No real backend found!")
                                
                    else:
                        print(f"❌ App Directory Not Found: {app_dir}")
                else:
                    print("❌ No app_path returned!")
                    
            else:
                print(f"❌ API Error: HTTP {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Test Error: {e}")

    print("\n" + "=" * 50)
    print("🏁 Test Completed!")

if __name__ == "__main__":
    asyncio.run(test_fullstack_generation())