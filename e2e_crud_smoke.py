import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Use the main AI builder to generate a blueprint-driven app
from exciting_lovable_backend_clean import ExcitingLovableAI


def build_test_app(base_dir: Path) -> Path:
    ai = ExcitingLovableAI()
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    app_dir = base_dir / f'e2e_smoke_{ts}'
    app_dir.mkdir(parents=True, exist_ok=True)

    plan = {
        "app_name": "E2E Smoke Social",
        "app_type": "social_app",
        "description": "E2E CRUD smoke test",
        # Provide sample data so backend models are inferred deterministically
        "sample_data": {
            "posts": [
                {"content": "Hello", "author": "Alice"}
            ],
            "users": [
                {"username": "alice", "name": "Alice"}
            ]
        }
    }

    info = ai.build_project(app_dir, plan)
    print("BUILD_INFO:", json.dumps(info, ensure_ascii=False))
    return app_dir


def run_e2e_crud(app_dir: Path) -> bool:
    backend_dir = app_dir / 'backend'
    if not backend_dir.exists():
        print("ERROR: backend directory not found:", backend_dir)
        return False

    # Ensure Python can import generated backend modules
    sys.path.insert(0, str(backend_dir))
    prev_cwd = os.getcwd()
    os.chdir(str(backend_dir))

    try:
        from fastapi.testclient import TestClient
        import importlib

        main = importlib.import_module('main')
        app = getattr(main, 'app', None)
        if app is None:
            print("ERROR: 'app' not found in backend main.py")
            return False

        ok = True
        with TestClient(app) as client:
            # Health check
            r = client.get('/health')
            print("HEALTH:", r.status_code, r.json())
            if r.status_code != 200:
                return False

            # Create a post
            post_body = {"content": "Smoke post", "author": "Tester"}
            r = client.post('/api/posts', json=post_body)
            print("POST /api/posts:", r.status_code, r.json())
            if r.status_code not in (200, 201):
                ok = False

            # List posts
            r = client.get('/api/posts')
            print("GET /api/posts:", r.status_code, r.json())
            if r.status_code != 200 or not isinstance(r.json(), list) or len(r.json()) < 1:
                ok = False

            # Create a user
            user_body = {"username": "tester", "name": "Smoke Tester"}
            r = client.post('/api/users', json=user_body)
            print("POST /api/users:", r.status_code, r.json())
            if r.status_code not in (200, 201):
                ok = False

            # List users
            r = client.get('/api/users')
            print("GET /api/users:", r.status_code, r.json())
            if r.status_code != 200 or not isinstance(r.json(), list) or len(r.json()) < 1:
                ok = False

        return ok
    finally:
        os.chdir(prev_cwd)


if __name__ == '__main__':
    base = Path('generated_apps')
    app_dir = build_test_app(base)
    success = run_e2e_crud(app_dir)
    print("E2E_SMOKE_PASS:", success)
    # Set process exit code accordingly
    sys.exit(0 if success else 1)
