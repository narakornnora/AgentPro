# apps/orchestrator/chat_api.py
from fastapi import APIRouter, Body
from pathlib import Path
import os, json, re, time

router = APIRouter()
WEB_ROOT = Path(os.getenv("WEB_ROOT", "/usr/share/nginx/html/app")).resolve()

@router.post("/chat/send")
def chat_send(body:dict=Body(...)):
    slug = (body.get("slug") or "").strip()
    text = (body.get("text") or "").strip()
    if not slug or not text: return {"ok": False, "error": "slug and text required"}
    proj = WEB_ROOT/slug
    if not proj.exists(): return {"ok": False, "error": f"project not found: {proj}"}

    # Very small heuristic "auto edit": if contains keyword add button to index.html
    idx = proj/"index.html"
    if idx.exists():
        h = idx.read_text(encoding="utf-8", errors="ignore")
        if "เพิ่มตะกร้าสินค้า" in text or re.search(r"\b(cart|ตะกร้า)\b", text, re.I):
            if "id=\"cart-btn\"" not in h:
                h = h.replace("</body>", '<button id="cart-btn" style="position:fixed;right:16px;bottom:16px;padding:12px 16px;border-radius:999px;background:#2f80ed;color:#fff;border:0">ตะกร้า</button>\n</body>')
        if "โหมดมืด" in text or re.search(r"\bdark\s*mode\b", text, re.I):
            h = h.replace("</head>", "<style>body{background:#0b0d12;color:#e9eef5}</style></head>")
        idx.write_text(h, encoding="utf-8")

    return {"ok": True, "message": {"role": "assistant", "content": "ปรับให้แล้ว ลองรีเฟรชพรีวิวดูครับ"}}
