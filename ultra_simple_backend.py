#!/usr/bin/env python3
"""
Ultra Simple Backend - No crash guaranteed!
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from pathlib import Path
import json
import uuid

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ROOT_DIR = Path("C:/agent")

class ChatMessage(BaseModel):
    message: str
    session_id: str = ""

@app.get("/")
async def root():
    try:
        interface_file = ROOT_DIR / "lovable_split_interface.html"
        if interface_file.exists():
            return FileResponse(str(interface_file))
        return {"message": "Ultra Simple Server Running!", "status": "ok"}
    except:
        return {"message": "Server OK", "status": "ok"}

@app.post("/chat")
async def chat():
    try:
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        return {
            "type": "start_building",
            "message": "เริ่มสร้างแอปเลย! 🚀",
            "session_id": session_id,
            "requirements": {
                "app_name": "Test App",
                "description": "Simple test app"
            }
        }
    except:
        return {"type": "error", "message": "Chat error"}

@app.get("/test")
async def test():
    return {"message": "Server is working!", "timestamp": "now"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Ultra Simple Server Starting...")
    print("📍 Server: http://localhost:8006")
    uvicorn.run(app, host="0.0.0.0", port=8006)