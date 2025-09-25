# apps/orchestrator/tracking_api.py
from fastapi import APIRouter, Body
from pathlib import Path
import os, json, time

router = APIRouter()
DATA_ROOT = Path(os.getenv("WEB_ROOT", "/usr/share/nginx/html/app")).resolve()

def _tasks(slug:str)->Path:
    p = DATA_ROOT/slug/"_meta"/"tasks.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

@router.get("/tracking/{slug}")
def get_board(slug:str):
    p = _tasks(slug)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"slug": slug, "columns": {"todo": [], "doing": [], "done": []}}

@router.post("/tracking/{slug}/add")
def add_task(slug:str, body:dict=Body(...)):
    title = (body.get("title") or "").strip()
    col = (body.get("column") or "todo").strip()
    if not title: return {"ok": False, "error":"title required"}
    data = get_board(slug)
    data["columns"].setdefault(col, [])
    item = {"id": int(time.time()*1000), "title": title, "ts": int(time.time())}
    data["columns"][col].append(item)
    _tasks(slug).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "item": item}

@router.post("/tracking/{slug}/move")
def move_task(slug:str, body:dict=Body(...)):
    tid = body.get("id")
    to = (body.get("to") or "doing").strip()
    data = get_board(slug)
    # remove
    found=None
    for c, arr in list(data["columns"].items()):
        for i, it in enumerate(arr):
            if it.get("id")==tid:
                found = it
                arr.pop(i)
                break
    if not found: return {"ok": False, "error": "not found"}
    data["columns"].setdefault(to, []).append(found)
    _tasks(slug).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True}
