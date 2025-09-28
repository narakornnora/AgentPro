# 🧪 Complete Testing Guide - Lovable Clone System

## 🚀 Quick Start Testing (วิธีทดสอบง่าย ๆ ใน 5 นาที!)

### Step 1: Start the System 🟢
```powershell
# เข้าไปใน directory หลัก
cd C:\agent

# วิธีที่ 1: ใช้ Docker (แนะนำ)
docker-compose up -d

# วิธีที่ 2: รัน Python โดยตรง (ถ้า Docker ไม่ได้)
cd apps/orchestrator
python main.py
```

### Step 2: Test Landing Page 🎨
```powershell
# เปิดไฟล์ในเบราว์เซอร์
start lovable_landing.html
```
**คาดหวัง:** หน้า landing แบบ Lovable พร้อม gradient สวย ๆ

### Step 3: Test Chat Interface 💬
```powershell
# เปิดไฟล์ chat ในเบราว์เซอร์
start lovable_chat.html
```
**คาดหวัง:** หน้า chat split screen - ซ้าย chat, ขวา live preview

### Step 4: Test Live Communication 🔄
1. พิมพ์ในช่อง chat: "สร้าง landing page สำหรับร้านกาแฟ"
2. กด Enter หรือคลิก Send
3. **คาดหวัง:** ระบบตอบกลับและแสดงโค้ดใน preview panel

---

## 🔧 Troubleshooting (แก้ไขปัญหาต่าง ๆ)

### ปัญหา: Docker ไม่ทำงาน
```powershell
# ตรวจสอบ Docker service
docker --version

# หาก error: รัน Python โดยตรง
cd C:\agent\apps\orchestrator
python main.py
```

### ปัญหา: API ไม่เชื่อมต่อ
```powershell
# ตรวจสอบ FastAPI server
curl http://localhost:8001/health
# หรือเปิดในเบราว์เซอร์: http://localhost:8001/docs
```

### ปัญหา: Chat ไม่ส่งข้อความ
1. เปิด Developer Tools (F12)
2. ดูใน Console tab หา error
3. ตรวจสอบว่า API server รันอยู่ที่ port 8001

---

## 🧬 Advanced Testing (การทดสอบแบบละเอียด)

### Test 1: Multi-Agent Response 🤖
```
Input: "สร้าง todo app ที่มี authentication"
Expected: 
- Requirements Analysis Agent วิเคราะห์
- Architecture Agent ออกแบบ
- Code Generator สร้างโค้ด
- UI/UX Agent ออกแบบหน้าตา
- Security Agent เพิ่ม authentication
```

### Test 2: Real-time Preview 📱
```
Input: "แก้ไขสี navbar เป็นสีน้ำเงิน"
Expected:
- โค้ด CSS อัพเดททันที
- Preview panel แสดงผลใหม่ภายใน 2 วินาที
```

### Test 3: Code Quality 💎
```
Input: "ทำ API สำหรับ user management"
Expected:
- โค้ดมี error handling
- มี input validation
- มี security best practices
- มี documentation
```

---

## 📊 Performance Benchmarks

### Response Time Goals:
- **Simple UI changes:** < 3 seconds
- **Complex app generation:** < 30 seconds  
- **API integration:** < 10 seconds

### Quality Metrics:
- **Code accuracy:** > 95%
- **UI/UX compliance:** > 90%
- **Security standards:** 100%

---

## 🐛 Known Issues & Solutions

### Issue 1: Port Conflicts
```powershell
# หาก port 8001 ถูกใช้แล้ว
netstat -ano | findstr :8001
# Kill process และ restart
```

### Issue 2: Missing Dependencies
```powershell
# Install requirements
cd C:\agent\apps\orchestrator
pip install -r requirements.txt
```

### Issue 3: API Key Missing
```powershell
# เช็ค .env file
cat .env
# เพิ่ม OPENAI_API_KEY ถ้าไม่มี
```

---

## 💾 Important Files to Keep (ไฟล์สำคัญที่ต้องไม่ลืม!)

### Core System:
- `apps/orchestrator/main.py` - FastAPI server หลัก
- `apps/orchestrator/agents/` - Multi-agent system
- `lovable_landing.html` - Landing page หลัก  
- `lovable_chat.html` - Chat interface หลัก

### Configuration:
- `docker-compose.yml` - Container setup
- `.env` - Environment variables
- `apps/orchestrator/requirements.txt` - Python dependencies

### Documentation:
- `LOVABLE_README.md` - ข้อมูลระบบทั้งหมด
- `TESTING_GUIDE.md` - คู่มือทดสอบนี้
- `README.md` - Project overview

---

## 🎯 Success Criteria (เกณฑ์ความสำเร็จ)

### ✅ Landing Page Test:
- [ ] หน้าโหลดได้ไม่มี error
- [ ] Gradient background แสดงถูกต้อง
- [ ] ปุ่ม "Get Started" ทำงาน
- [ ] Responsive design บนมือถือ

### ✅ Chat System Test:
- [ ] Chat interface โหลดได้
- [ ] ส่งข้อความได้
- [ ] ได้รับ response จาก AI
- [ ] Preview panel แสดงโค้ด

### ✅ Multi-Agent Test:
- [ ] Agent ตอบสนองตามบทบาท
- [ ] Code generation ทำงาน  
- [ ] Quality assurance ตรวจสอบ
- [ ] Final output ถูกต้อง

---

## 🔄 Regular Maintenance

### Daily Checks:
1. ทดสอบ chat functionality
2. ตรวจสอบ agent responses
3. Monitor performance metrics

### Weekly Tasks:
1. Update dependencies
2. Backup important configs
3. Review and improve prompts

### Monthly Reviews:
1. Performance optimization
2. Feature enhancement
3. Security updates

---

## 📞 Emergency Recovery (กู้คืนแบบฉุกเฉิน)

หากระบบพัง ให้ทำตามนี้:

1. **Backup current state:**
```powershell
git add .
git commit -m "Emergency backup $(Get-Date)"
```

2. **Restart from scratch:**
```powershell
git reset --hard HEAD~1  # กลับไป 1 commit
# หรือ
git stash  # เก็บการเปลี่ยนแปลง
```

3. **Quick restore:**
```powershell
cd C:\agent
docker-compose down
docker-compose up -d --build
```

---

**🎉 Happy Testing! หากมีปัญหาอะไร ให้ดูใน guide นี้ก่อนนะครับ! 💪**