# apps/orchestrator/github_api.py
from fastapi import APIRouter, Body
import os, subprocess, tempfile, shutil, time
from pathlib import Path

router = APIRouter()
WEB_ROOT = Path(os.getenv("WEB_ROOT", "/usr/share/nginx/html/app")).resolve()

@router.post("/github/export")
def export_repo(data:dict=Body(...)):
    slug = data.get("slug")
    repo = data.get("repo")  # e.g. https://<token>@github.com/user/myrepo.git
    if not slug or not repo:
        return {"ok": False, "error": "slug and repo required"}
    proj = WEB_ROOT/slug
    if not proj.exists():
        return {"ok": False, "error": f"project not found: {proj}"}
    tmp = Path(tempfile.mkdtemp(prefix="export-"))
    shutil.copytree(proj, tmp/"app", dirs_exist_ok=True)
    (tmp/"README.md").write_text(f"# {slug}\nExported by AgentPro at {time.ctime()}\n", encoding="utf-8")
    try:
        subprocess.check_call(["git","init"], cwd=tmp)
        subprocess.check_call(["git","config","user.email","agentpro@local"], cwd=tmp)
        subprocess.check_call(["git","config","user.name","AgentPro"], cwd=tmp)
        subprocess.check_call(["git","add","-A"], cwd=tmp)
        subprocess.check_call(["git","commit","-m","Export from AgentPro"], cwd=tmp)
        subprocess.check_call(["git","branch","-M","main"], cwd=tmp)
        subprocess.check_call(["git","remote","add","origin", repo], cwd=tmp)
        subprocess.check_call(["git","push","-u","origin","main","--force"], cwd=tmp)
        return {"ok": True, "pushed": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
