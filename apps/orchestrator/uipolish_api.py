# apps/orchestrator/uipolish_api.py
from fastapi import APIRouter, Body
from pathlib import Path
import os

router = APIRouter()
WEB_ROOT = Path(os.getenv("WEB_ROOT", "/usr/share/nginx/html/app")).resolve()

@router.post("/ui/polish")
def ui_polish(body:dict=Body(...)):
    slug = (body.get("slug") or "").strip()
    if not slug: return {"ok": False, "error": "slug required"}
    proj = WEB_ROOT/slug
    css = proj/"styles.css"
    # Add tokens + base font if missing
    base = ":root{--primary:#2f80ed;--bg:#0f1115;--text:#e9eef5}\nbody{font-family:system-ui,-apple-system,Segoe UI,Roboto,Prompt,sans-serif}"
    if css.exists():
        txt = css.read_text(encoding="utf-8", errors="ignore")
        if ":root" not in txt or "--primary" not in txt: txt = base + "\n" + txt
        css.write_text(txt, encoding="utf-8")
    else:
        css.write_text(base+"\n", encoding="utf-8")
    # Ensure index link includes tokens.css hint
    idx = proj/"index.html"
    if idx.exists():
        h = idx.read_text(encoding="utf-8", errors="ignore")
        if "styles.css" not in h:
            h = h.replace("</head>", '<link rel="stylesheet" href="styles.css"></head>')
        if "viewport" not in h:
            h = h.replace("<head>", '<head><meta name="viewport" content="width=device-width,initial-scale=1">')
        idx.write_text(h, encoding="utf-8")
    return {"ok": True}
