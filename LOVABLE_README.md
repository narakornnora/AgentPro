# 🚀 AgentPro Lovable Clone

> **คำเตือน**: การใช้งานระบบนี้ต้องมี OPENAI_API_KEY

## 🌟 ภาพรวม

AgentPro Lovable Clone เป็นระบบสร้างแอปและเว็บไซต์ผ่านการสนทนากับ AI แบบ real-time เหมือน Lovable.dev พร้อมระบบ multi-agent ที่ครบครัน

### ✨ Features หลัก

🎨 **Landing Page แบบ Lovable**
- Gradient background สวยงาม  
- Hero section ที่ดึงดูดใจ
- Quick examples และ feature showcase
- Responsive design ทุกหน้าจอ

💬 **Chat Interface แบบ Split Screen**  
- Chat panel ด้านซ้าย (40%)
- Live preview panel ด้านขวา (60%)
- Real-time code generation
- Code/Preview toggle

🤖 **Multi-Agent System**
- 25+ specialized AI agents
- Real-time collaboration
- Advanced testing และ optimization
- Universal deployment capabilities

⚡ **Live Preview**
- ดู preview ทันทีที่สร้าง
- Code view พร้อม syntax highlighting  
- Deploy button สำหรับ production

## 🛠️ การติดตั้ง

### 1. เตรียม Environment

```bash
# Clone หรือ download project
cd c:\\agent

# ติดตั้ง dependencies
pip install -r requirements.txt
pip install fastapi uvicorn python-multipart
pip install openai pathlib slugify

# ตั้ง OpenAI API Key
set OPENAI_API_KEY=your_openai_api_key_here
```

## 🧪 การทดสอบระบบ

### 🚀 Quick Test (5 นาทีเสร็จ!)

```powershell
# วิธีที่ 1: One-click testing 
double-click quick_test.bat

# วิธีที่ 2: Manual testing
cd C:\agent\apps\orchestrator
python main.py
# จากนั้นเปิด lovable_landing.html และ lovable_chat.html
```

### 🏥 Health Check

```powershell
# ตรวจสอบสุขภาพระบบ
python health_check.py

# ตรวจสอบ API server
curl http://localhost:8001/health
# หรือเปิดในเบราว์เซอร์: http://localhost:8001/docs
```

### 📋 Test Scenarios

**Test 1: สร้าง Landing Page**
```
Input: "สร้าง landing page สำหรับร้านกาแฟ"
Expected: HTML/CSS/JS สำหรับร้านกาแฟ พร้อม design ที่สวยงาม
```

**Test 2: สร้าง Full-stack App**  
```
Input: "สร้าง todo app ที่มี login system"
Expected: Frontend + Backend + Database + Authentication
```

**Test 3: UI Modifications**
```
Input: "เปลี่ยนสี navbar เป็นสีน้ำเงิน"
Expected: CSS อัพเดทและ preview แสดงผลใหม่ทันที
```

### 🐛 Troubleshooting

**ปัญหา: API ไม่ตอบสนอง**
```powershell
# ตรวจสอบ server status
netstat -ano | findstr :8001

# Restart server
cd C:\agent\apps\orchestrator  
python main.py
```

**ปัญหา: Chat ไม่ส่งข้อความ**
1. เปิด Developer Tools (F12)
2. ดู Console tab หา JavaScript errors
3. ตรวจสอบ CORS settings
4. ลองรีโหลดหน้าเว็บ

**ปัญหา: Docker ไม่ทำงาน**
```powershell
# ใช้ Python โดยตรงแทน
cd C:\agent\apps\orchestrator
python main.py
```

### 📊 Performance Metrics

- **Response time:** < 3 วินาที สำหรับ simple requests
- **Code generation:** < 30 วินาที สำหรับ complex apps  
- **Memory usage:** < 500MB ในการทำงานปกติ
- **CPU usage:** < 50% บนเครื่อง mid-range

### 🔧 Advanced Testing

ดูรายละเอียดเพิ่มเติมใน `TESTING_GUIDE.md` สำหรับ:
- การทดสอบ multi-agent system
- Performance benchmarking  
- Security testing
- Load testing scenarios

### 2. เริ่มระบบ

```bash
# วิธีที่ 1: เริ่ม API Server
python lovable_api.py

# วิธีที่ 2: เริ่ม Multi-Agent System (ถ้าต้องการ advanced features)  
cd apps\\orchestrator
python main.py
```

### 3. เข้าใช้งาน

- **Landing Page**: http://localhost:8000
- **Chat Interface**: http://localhost:8000/chat  
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 โครงสร้างไฟล์

```
c:\\agent\\
├── lovable_landing.html      # หน้า Landing Page
├── lovable_chat.html         # หน้า Chat Interface  
├── lovable_api.py           # Main API Server
├── lovable_clone.py         # Original implementation
├── README.md                # คู่มือนี้
└── apps\\
    ├── orchestrator\\       # Multi-agent system
    │   ├── main.py         # Main orchestrator
    │   ├── agents\\        # 25+ AI agents
    │   └── workspace\\     # Generated files
    └── web\\               # Web interfaces
```

## 🎯 วิธีใช้งาน

### 1. เริ่มจาก Landing Page
1. เปิด http://localhost:8000
2. พิมพ์ที่อยากสร้างในช่อง chat
3. กด Enter หรือคลิก ไมค์
4. จะไปหน้า Chat Interface อัตโนมัติ

### 2. ใช้งาน Chat Interface
1. พิมพ์คำสั่งในช่อง chat เช่น:
   - "สร้าง landing page ร้านกาแฟ"
   - "ทำแอป todo list"  
   - "สร้าง dashboard analytics"
   - "ทำเว็บ portfolio"

2. ดู AI response และ live preview
3. สลับดู Code ได้ด้วยปุ่ม "💻 Code"
4. Deploy ได้ด้วยปุ่ม "🚀 Deploy"

### 3. Examples คำสั่งที่ใช้ได้

**Landing Pages:**
- "สร้าง landing page ร้านอาหาร"
- "ทำหน้าแรกบริษัทเทคโนโลยี"  
- "landing page สำหรับคาเฟ่"

**Mobile Apps:**
- "สร้างแอป social media"
- "ทำแอป e-commerce"
- "แอป productivity สำหรับทำงาน"

**Dashboards:**  
- "สร้าง admin dashboard"
- "ทำ analytics dashboard"
- "dashboard สำหรับร้านค้า"

**Websites:**
- "ทำเว็บ portfolio"
- "สร้างเว็บบล็อก"
- "เว็บร้านค้าออนไลน์"

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_api_key

# Optional  
OPENAI_MODEL=gpt-4o-mini    # หรือ gpt-4
WEBROOT=/app/workspace      # ที่เก็บไฟล์ที่สร้าง
```

### API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Landing page |
| `/chat` | GET | Chat interface |
| `/api/chat` | POST | Send message to AI |
| `/api/conversations` | GET | List conversations |
| `/generated/{slug}/` | GET | Serve generated apps |
| `/health` | GET | Health check |

## 🚀 Advanced Features

### Multi-Agent System
หากต้องการใช้ระบบ multi-agent แบบเต็ม:

```bash
cd apps\\orchestrator
python main.py
```

จะได้:
- 25+ specialized agents
- Real-time collaboration  
- Advanced testing
- Performance optimization
- Universal deployment

### WebSocket Chat
สำหรับ real-time chat:

```javascript  
const ws = new WebSocket('ws://localhost:8001/ws');
ws.send(JSON.stringify({
    type: 'chat_message',
    message: 'สร้าง landing page'
}));
```

## 🔍 Troubleshooting

### ปัญหาที่พบบ่อย

**1. API Key ไม่ทำงาน**
```bash
# ตรวจสอบ API key
echo $OPENAI_API_KEY

# ตั้งใหม่
set OPENAI_API_KEY=your_key_here
```

**2. Port ชนกัน**
```bash
# เปลี่ยน port
uvicorn lovable_api:app --port 8001
```

**3. Dependencies ขาด**
```bash
pip install -r apps\\orchestrator\\requirements.txt
```

**4. Permission Error**
```bash
# Run as administrator ใน Windows
```

### Debug Mode
```bash
# เปิด debug logs
python lovable_api.py --log-level debug
```

## 📊 Performance

- **Response time**: ~2-5 วินาที
- **Code generation**: ~3-10 วินาที  
- **Memory usage**: ~200-500MB
- **Concurrent users**: 10+ (ขึ้นกับ OpenAI rate limits)

## 🛡️ Security

- CORS enabled สำหรับ development
- Input validation สำหรับ user messages
- File path sanitization
- Rate limiting (ขึ้นกับ OpenAI)

## 🔄 Updates & Backup

### บันทึกการสนทนา
ระบบจะบันทึกการสนทนาใน memory (จะหายเมื่อ restart server)

### Generated Files  
ไฟล์ที่สร้างจะอยู่ใน:
- `workspace/generated-app/apps/web/` (multi-agent)
- `apps/orchestrator/workspace/` (API mode)

### Backup
```bash
# Backup generated files
xcopy workspace backup_folder /E /I
```

## 🎓 การพัฒนาต่อ

### เพิ่ม Agent ใหม่
1. สร้างไฟล์ใน `apps/orchestrator/agents/`
2. Inherit จาก `BaseAgent`  
3. เพิ่มใน agent manager

### Custom Templates
1. แก้ไข `SYSTEM` prompt ใน `main.py`
2. เพิ่ม templates ใน `templates/`

### New Features
1. เพิ่ม endpoint ใน `lovable_api.py`
2. อัปเดต frontend ใน `lovable_chat.html`

## 📞 Support

หากมีปัญหาหรือข้อสงสัย:

1. ตรวจสอบ logs ใน terminal
2. ดู `/health` endpoint  
3. ลองใส่ API key ใหม่
4. Restart server

## 🏆 Credits

พัฒนาโดย AgentPro Team  
Inspired by Lovable.dev  
Powered by OpenAI GPT-4

---

**หมายเหตุ**: ระบบนี้ใช้ OpenAI API ซึ่งเสียค่าใช้จ่ายตามการใช้งาน กรุณาตั้ง usage limits ใน OpenAI dashboard