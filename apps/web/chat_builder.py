from fastapi import APIRouter, Body
from pydantic import BaseModel
import httpx

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatIn(BaseModel):
    messages: list[Message]
    slug: str | None = None

@router.post("/chat/build")
def chat_build(body: ChatIn):
    # เอาข้อความ user ล่าสุดไปเป็น requirement
    prompt = ""
    for m in reversed(body.messages):
        if m.role == "user":
            prompt = m.content.strip()
            break
    if not prompt:
        return {"ok": False, "error": "no user prompt"}

    # โยนไปที่ /plan_build ให้สร้างเว็บ
    try:
        with httpx.Client(timeout=120.0) as client:
            r = client.post("http://localhost:8001/plan_build", json={"prompt": prompt, "slug": body.slug})
            data = r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

    msg = {"role": "assistant", "content": f"สร้างเว็บจากคำสั่ง: “{prompt}” เรียบร้อย"}
    return {
        "ok": True,
        "message": msg,
        "web_url": data.get("web_url"),
        "slug": data.get("slug") or (data.get("web_url","").split("/")[2] if data.get("web_url") else None)
    }
