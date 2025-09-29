# Revise Usage (HTTP and WebSocket)

Use revise to iterate on the app requirements and get a fresh build with your changes merged in.

## HTTP: POST /revise

Request JSON:
{
  "session_id": "optional-existing-session",
  "delta": {
    "app_name": "My Instagram+",
    "ui_theme": "dark",
    "routes": [
      { "path": "#/admin", "title": "Admin", "components": [
        { "type": "text", "value": "Admin tools" },
        { "type": "table", "collection": "posts", "columns": [
          {"header":"ID","field":"id"},
          {"header":"User","field":"user"},
          {"header":"Caption","field":"caption"}
        ] }
      ] }
    ]
  }
}

Response JSON:
{
  "success": true,
  "session_id": "...",
  "app_url": "file:///.../index.html",
  "http_url": "http://localhost:8001/apps/app_7/index.html",
  "download_url": "http://localhost:8001/apps/app_7.zip"
}

Notes:
- Fields in delta are deep-merged with your current session requirements.
- Arrays are merged by set-union order; duplicates are avoided.
- If data_models or sample_data add new collections, a backend is auto-generated.

## WebSocket: ws://localhost:8001/ws

Send JSON to revise an existing session and rebuild live:
{
  "action": "revise",
  "session_id": "optional-existing-session",
  "delta": {
    "routes": [
      { "path": "#/settings", "title": "Settings", "components": [
        {"type":"form","collection":"settings","fields":[{"name":"theme"},{"name":"language"}],"redirect":"#/"}
      ]}
    ]
  }
}

Events you’ll receive:
- status: progress updates
- file_start / typing_line / file_complete: live code streaming
- preview_ready: HTML content to show immediately
- build_complete: final http_url + download_url

Tip: Start the generated backend if present using start_backend.bat in the app folder to enable live API for tables/lists/forms.
