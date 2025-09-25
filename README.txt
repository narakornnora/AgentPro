
AgentPro Feature Pack FULL (7 features)
--------------------------------------
Files:
- apps/web/chat.html
- apps/orchestrator/chat_api.py
- apps/orchestrator/uipolish_api.py
- apps/orchestrator/bug_guard.py
- apps/web/preview.html
- apps/orchestrator/github_api.py
- apps/orchestrator/tests_api.py
- apps/orchestrator/tracking_api.py
- apps/web/dashboard.html
- apps/web/tokens.css

Wire into orchestrator (apps/orchestrator/main.py):
from .chat_api import router as chat_router
from .uipolish_api import router as uipolish_router
from .bug_guard import router as bug_router
from .github_api import router as gh_router
from .tests_api import router as tests_router
from .tracking_api import router as tracking_router
app.include_router(chat_router)
app.include_router(uipolish_router)
app.include_router(bug_router)
app.include_router(gh_router)
app.include_router(tests_router)
app.include_router(tracking_router)

Rebuild:
docker compose build orchestrator web
docker compose up -d orchestrator web

Open:
- Chat:       http://localhost:8080/chat.html
- Preview:    http://localhost:8080/preview.html
- Dashboard:  http://localhost:8080/dashboard.html

Notes:
- GitHub export expects 'git' inside orchestrator image and repo URL with token embedded or interactive not required.
- UI polish / chat auto-edit are minimal safe stubs; extend rules as needed.
