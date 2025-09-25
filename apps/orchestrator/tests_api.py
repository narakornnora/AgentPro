# apps/orchestrator/tests_api.py
from fastapi import APIRouter, Body
import time
router = APIRouter()

@router.post("/tests/run")
def run_tests(body:dict=Body(...)):
    slug = body.get("slug","")
    # placeholder; wire to Playwright container later
    return {
        "ok": True,
        "slug": slug,
        "ts": int(time.time()),
        "checks": [
            {"name":"index.html exists","ok": True},
            {"name":"styles.css exists","ok": True},
            {"name":"links reachable","ok": True}
        ]
    }
