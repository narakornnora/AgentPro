# apps/orchestrator/bug_guard.py
from fastapi import APIRouter, Body
from pathlib import Path
import os, shutil, time

router = APIRouter()
WEB_ROOT = Path(os.getenv("WEB_ROOT", "/usr/share/nginx/html/app")).resolve()
BK_ROOT = Path(os.getenv("BACKUP_ROOT", "/usr/share/nginx/html/_backups")).resolve()

def _proj(slug): return WEB_ROOT/slug
def _bk_dir(slug): return BK_ROOT/slug

@router.post("/bug/backup")
def backup(body:dict=Body(...)):
    slug = (body.get("slug") or "").strip()
    if not slug: return {"ok": False, "error": "slug required"}
    src = _proj(slug)
    if not src.exists(): return {"ok": False, "error": "not found"}
    dst = _bk_dir(slug); dst.mkdir(parents=True, exist_ok=True)
    tag = time.strftime("%Y%m%d-%H%M%S")
    out = dst/f"{slug}-{tag}"
    shutil.copytree(src, out)
    return {"ok": True, "backup_path": str(out)}

@router.post("/bug/rollback")
def rollback(body:dict=Body(...)):
    slug = (body.get("slug") or "").strip()
    to = (body.get("backup_path") or "").strip()
    if not slug or not to: return {"ok": False, "error": "slug/backup_path required"}
    src = Path(to)
    if not src.exists(): return {"ok": False, "error": "backup not found"}
    dst = _proj(slug)
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return {"ok": True}
