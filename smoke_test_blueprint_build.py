import json, os
from pathlib import Path
from exciting_lovable_backend_clean import ExcitingLovableAI

ai = ExcitingLovableAI()
app_dir = Path('generated_apps') / 'test_blueprint'
app_dir.mkdir(parents=True, exist_ok=True)

plan = {
    "app_name": "Test Social",
    "app_type": "social_app",
    "description": "IG-like test",
    "features": ["feed", "explore", "create", "inbox", "notifications", "profile"]
}

info = ai.build_project(app_dir, plan)
print("BUILD_INFO:", json.dumps(info, ensure_ascii=False))

# Verify key files
expected = [
    app_dir / 'index.html',
    app_dir / 'styles.css',
    app_dir / 'app.js',
    app_dir / 'blueprint.json',
]
backend_expected = [
    app_dir / 'backend' / 'models.py',
    app_dir / 'backend' / 'schemas.py',
    app_dir / 'backend' / 'main.py',
    app_dir / 'backend' / 'requirements.txt',
    app_dir / 'start_backend.bat',
]

missing = [str(p) for p in expected+backend_expected if not p.exists()]
print("MISSING:", json.dumps(missing, ensure_ascii=False))

# Print short file sizes summary
summary = { str(p): (p.stat().st_size if p.exists() else 0) for p in expected+backend_expected }
print("SUMMARY:", json.dumps(summary, ensure_ascii=False))
