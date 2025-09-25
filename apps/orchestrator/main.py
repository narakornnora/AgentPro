import os, json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from slugify import slugify
from openai import OpenAI

WEBROOT = Path(os.getenv("WEBROOT", "/app/workspace/generated-app/apps/web"))
WEBROOT.mkdir(parents=True, exist_ok=True)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required (no fallback / no templates).")
client = OpenAI(api_key=API_KEY)

app = FastAPI(title="AgentPro Orchestrator (AI Mode Only)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatReq(BaseModel):
    message: str = Field(min_length=2)

class ChatResp(BaseModel):
    ok: bool
    slug: str
    web_url: str
    files: List[str]

SYSTEM = """
คุณคือ Codegen Orchestrator. หน้าที่คุณคือ สร้าง "ชุดไฟล์เว็บ" ตาม requirement สั้น ๆ เป็นภาษาไทย/อังกฤษ
**ตอบกลับเป็น JSON เท่านั้น** และต้องตรงสคีมนี้เป๊ะ:
{
  "slug": "myapp-YYYYMMDD-HHMMSS",
  "files": [
    {"path":"index.html","content":"<!doctype html>..."},
    {"path":"styles.css","content":"..."},
    {"path":"script.js","content":"..."},
    {"path":"menu.html","content":"..."},
    {"path":"contact.html","content":"..."}
  ]
}

ข้อกำหนด:
- "files" ต้องมีอย่างน้อย: index.html, styles.css
- HTML ทุกไฟล์ต้องอ้างอิงกันแบบ relative (เช่น <link rel="stylesheet" href="./styles.css">)
- ใส่ <meta charset="utf-8"> และ <meta name="viewport" ...> ครบ
- หากผู้ใช้ระบุประเภท (เช่น ร้านอาหาร, คาเฟ่, POS, Blog, Shop) ให้โครงสร้างเนื้อหาสอดคล้อง
- ห้ามอธิบาย, ห้ามใส่ข้อความนอก JSON, ห้าม markdown, ห้าม code fence
"""

def _ask_ai_to_plan(user_msg: str) -> Dict[str, Any]:
    rsp = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        response_format={"type":"json_object"},
        messages=[
            {"role":"system", "content": SYSTEM},
            {"role":"user", "content": user_msg}
        ],
    )
    txt = rsp.choices[0].message.content
    try:
        data = json.loads(txt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI returned non-JSON: {e}")

    # validate
    if "slug" not in data or "files" not in data or not isinstance(data["files"], list):
        raise HTTPException(status_code=422, detail="AI JSON missing required fields")

    # บังคับรูปแบบ slug
    slug = data["slug"].strip()
    if not slug or not slug.startswith("myapp-"):
        slug = "myapp-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        data["slug"] = slug

    # บังคับมี index.html + styles.css
    paths = { (f.get("path") or "").lower() for f in data["files"] if isinstance(f, dict) }
    if "index.html" not in paths or "styles.css" not in paths:
        raise HTTPException(status_code=422, detail="AI must provide at least index.html and styles.css")

    return data

def _write_files(plan: Dict[str, Any]) -> List[str]:
    slug = plan["slug"]
    outdir = WEBROOT / slug
    outdir.mkdir(parents=True, exist_ok=True)

    written: List[str] = []
    for f in plan["files"]:
        if not isinstance(f, dict): continue
        rel = (f.get("path") or "").lstrip("/").strip()
        content = f.get("content") or ""
        if not rel:
            continue
        p = outdir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        written.append(str(p))
    if not (outdir / "index.html").exists():
        raise HTTPException(status_code=500, detail="index.html missing after write")
    return written

@app.get("/health")
def health():
    return {"ok": True, "webroot": str(WEBROOT), "model": MODEL}

@app.post("/chat/ai", response_model=ChatResp)
def chat_ai(req: ChatReq):
    plan = _ask_ai_to_plan(req.message.strip())
    files = _write_files(plan)
    slug = plan["slug"]
    web_url = f"/app/{slug}/index.html"
    return ChatResp(ok=True, slug=slug, web_url=web_url, files=[f"/app/{slug}/{Path(f).name}" for f in files])
