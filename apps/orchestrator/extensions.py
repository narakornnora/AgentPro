from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pathlib import Path
import os, json, time

router = APIRouter()

WEB_ROOT = Path(os.getenv("WEB_ROOT", "/usr/share/nginx/html/app")).resolve()

def _slug_dir(slug:str)->Path: return WEB_ROOT/slug
def _meta(slug:str, name:str)->Path:
    p = _slug_dir(slug)/"_meta"/name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def _read_json(p:Path, default):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except: return default

def _write_json(p:Path, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def _record(slug, step, status, msg="", extra=None):
    ev = {"ts": int(time.time()), "step": step, "status": status, "msg": msg, "extra": extra or {}}
    with _meta(slug,"events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False)+"\n")
    prog = _read_json(_meta(slug,"progress.json"), {"phase":"draft","steps":[]})
    prog["phase"]=step
    steps = {s["name"]: s for s in prog.get("steps",[])}
    steps[step] = {"name":step, "status":status, "ts":ev["ts"], "msg":msg}
    prog["steps"] = list(steps.values())
    _write_json(_meta(slug,"progress.json"), prog)

@router.get("/projects/{slug}/progress")
def get_progress(slug:str):
    preview_url = f"/app/{slug}/index.html"
    return {
        "project": slug,
        "phase": _read_json(_meta(slug,"progress.json"), {}).get("phase","draft"),
        "steps": _read_json(_meta(slug,"progress.json"), {}).get("steps", []),
        "preview": {"web_url": preview_url},
        "changelog": _meta(slug,"events.jsonl").read_text(encoding="utf-8") if _meta(slug,"events.jsonl").exists() else "",
        "tests": _read_json(_meta(slug,"tests.json"), {"ok": True, "issues": {}}),
        "bugs": _read_json(_meta(slug,"bugs.json"), []),
    }

@router.post("/projects/{slug}/events/{step}")
def add_event(slug:str, step:str, body:dict=Body(...)):
    _record(slug, step, body.get("status","info"), body.get("msg",""), body.get("extra"))
    return {"ok": True}

@router.post("/refine_live")from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pathlib import Path
import os, json, time

router = APIRouter()

WEB_ROOT = Path(os.getenv("WEB_ROOT", "/usr/share/nginx/html/app")).resolve()

def _slug_dir(slug:str)->Path: return WEB_ROOT/slug
def _meta(slug:str, name:str)->Path:
    p = _slug_dir(slug)/"_meta"/name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def _read_json(p:Path, default):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except: return default

def _write_json(p:Path, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def _record(slug, step, status, msg="", extra=None):
    ev = {"ts": int(time.time()), "step": step, "status": status, "msg": msg, "extra": extra or {}}
    with _meta(slug,"events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False)+"\n")
    prog = _read_json(_meta(slug,"progress.json"), {"phase":"draft","steps":[]})
    prog["phase"]=step
    steps = {s["name"]: s for s in prog.get("steps",[])}
    steps[step] = {"name":step, "status":status, "ts":ev["ts"], "msg":msg}
    prog["steps"] = list(steps.values())
    _write_json(_meta(slug,"progress.json"), prog)

@router.get("/projects/{slug}/progress")
def get_progress(slug:str):
    preview_url = f"/app/{slug}/index.html"
    return {
        "project": slug,
        "phase": _read_json(_meta(slug,"progress.json"), {}).get("phase","draft"),
        "steps": _read_json(_meta(slug,"progress.json"), {}).get("steps", []),
        "preview": {"web_url": preview_url},
        "changelog": _meta(slug,"events.jsonl").read_text(encoding="utf-8") if _meta(slug,"events.jsonl").exists() else "",
        "tests": _read_json(_meta(slug,"tests.json"), {"ok": True, "issues": {}}),
        "bugs": _read_json(_meta(slug,"bugs.json"), []),
    }

@router.post("/projects/{slug}/events/{step}")
def add_event(slug:str, step:str, body:dict=Body(...)):
    _record(slug, step, body.get("status","info"), body.get("msg",""), body.get("extra"))
    return {"ok": True}

@router.post("/refine_live")
def refine_live(body:dict=Body(...)):
    async def gen():
        yield 'event: phase\ndata: {"step":"plan"}\n\n'
        yield 'event: phase\ndata: {"step":"apply"}\n\n'
        yield 'event: phase\ndata: {"step":"done"}\n\n'
    return StreamingResponse(gen(), media_type="text/event-stream")

def install_extensions(app):
    app.include_router(router)
    app.state.record_event = _record
def refine_live(body:dict=Body(...)):
    async def gen():
        yield 'event: phase\ndata: {"step":"plan"}\n\n'
        yield 'event: phase\ndata: {"step":"apply"}\n\n'
        yield 'event: phase\ndata: {"step":"done"}\n\n'
    return StreamingResponse(gen(), media_type="text/event-stream")

def install_extensions(app):
    app.include_router(router)
    app.state.record_event = _record
