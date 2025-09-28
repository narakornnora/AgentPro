"""
Real-time WebSocket Chat Handler
Provides instant, streaming responses for natural conversation
"""

from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, Set, Optional
import json
import asyncio
import uuid
from datetime import datetime
from .simple_conversational_ai import SimpleConversationalAI
from .base_agent import AgentWorkflow  
from .simple_agent_manager import SimpleAgentManager
from pathlib import Path
import os

class ChatConnection:
    def __init__(self, websocket: WebSocket, user_id: str):
        self.websocket = websocket
        self.user_id = user_id
        self.session_id = str(uuid.uuid4())
        self.connected_at = datetime.now()
        self.active = True

class ChatManager:
    def __init__(self, openai_client):
        self.connections: Dict[str, ChatConnection] = {}
        self.user_sessions: Dict[str, ConversationalAI] = {}
        self.openai_client = openai_client
        
        # Initialize simple agent manager
        webroot = Path(os.getenv("WEBROOT", "/app/workspace/generated-app/apps/web"))
        self.agent_manager = SimpleAgentManager(webroot, openai_client)
        
        # Initialize agents (will be implemented)
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        # This will be implemented with actual agents
        pass
    
    async def connect(self, websocket: WebSocket, user_id: str = None) -> str:
        """Accept new WebSocket connection"""
        
        if not user_id:
            user_id = f"user_{str(uuid.uuid4())[:8]}"
        
        await websocket.accept()
        
        connection = ChatConnection(websocket, user_id)
        self.connections[connection.session_id] = connection
        
        # Create or get user's conversational AI session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = SimpleConversationalAI(
                self.openai_client,
                self.agent_manager
            )
        
        # Send welcome message
        await websocket.send_json({
            "type": "welcome",
            "session_id": connection.session_id,
            "user_id": user_id,
            "message": "สวัสดีครับ! ผมพร้อมช่วยสร้างเว็บไซต์ตามที่คุณต้องการ มีอะไรให้ช่วยไหมครับ?",
            "suggestions": [
                "สร้างเว็บไซต์ร้านอาหาร",
                "ทำเว็บไซต์ร้านค้าออนไลน์", 
                "สร้างเว็บไซต์ portfolio",
                "ทำหน้าเว็บบล็อก"
            ]
        })
        
        return connection.session_id
    
    async def disconnect(self, session_id: str):
        """Handle disconnection"""
        if session_id in self.connections:
            self.connections[session_id].active = False
            del self.connections[session_id]
    
    async def handle_message(self, session_id: str, message: Dict):
        """Handle incoming message from user"""
        
        if session_id not in self.connections:
            raise HTTPException(status_code=404, detail="Session not found")
        
        connection = self.connections[session_id]
        
        if not connection.active:
            raise HTTPException(status_code=400, detail="Connection inactive")
        
        try:
            # Get user's conversational AI
            conv_ai = self.user_sessions.get(connection.user_id)
            
            if not conv_ai:
                await connection.websocket.send_json({
                    "type": "error",
                    "message": "เซสชันหมดอายุ กรุณาเชื่อมต่อใหม่"
                })
                return
            
            # Show typing indicator
            await connection.websocket.send_json({
                "type": "typing",
                "message": "กำลังคิด..."
            })
            
            # Process message
            user_text = message.get("text", "").strip()
            
            if not user_text:
                await connection.websocket.send_json({
                    "type": "error",
                    "message": "กรุณาพิมพ์ข้อความ"
                })
                return
            
            # Process with conversational AI
            response = await conv_ai.process_message(user_text, connection.websocket)
            
            # Send immediate response
            response_data = {
                "type": "message",
                "role": "assistant", 
                "content": response.message,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "action_taken": response.action_taken,
                    "preview_url": response.preview_url
                }
            }
            
            if response.suggestions:
                response_data["suggestions"] = response.suggestions
            
            await connection.websocket.send_json(response_data)
            
            # If there's a preview URL, send it separately
            if response.preview_url:
                await connection.websocket.send_json({
                    "type": "preview",
                    "url": response.preview_url,
                    "message": "ดูตัวอย่างได้ที่นี่เลยครับ!"
                })
            
        except Exception as e:
            print(f"Error handling message: {e}")
            await connection.websocket.send_json({
                "type": "error",
                "message": f"เกิดข้อผิดพลาด: {str(e)}"
            })
    
    async def send_progress_update(self, user_id: str, update: Dict):
        """Send progress update to user"""
        
        # Find user's active connections
        user_connections = [
            conn for conn in self.connections.values()
            if conn.user_id == user_id and conn.active
        ]
        
        for connection in user_connections:
            try:
                await connection.websocket.send_json({
                    "type": "progress",
                    **update
                })
            except:
                # Connection might be closed
                connection.active = False
    
    async def broadcast_system_message(self, message: str):
        """Broadcast system message to all connected users"""
        
        system_msg = {
            "type": "system", 
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        for connection in list(self.connections.values()):
            if connection.active:
                try:
                    await connection.websocket.send_json(system_msg)
                except:
                    connection.active = False
    
    def get_active_users(self) -> int:
        """Get number of active users"""
        return len([conn for conn in self.connections.values() if conn.active])
    
    def get_user_sessions(self) -> Dict[str, Dict]:
        """Get summary of user sessions"""
        sessions = {}
        
        for user_id, conv_ai in self.user_sessions.items():
            active_connections = len([
                conn for conn in self.connections.values()
                if conn.user_id == user_id and conn.active
            ])
            
            sessions[user_id] = {
                "active_connections": active_connections,
                "conversation_length": len(conv_ai.conversation_history),
                "active_project": conv_ai.active_project,
                "last_activity": conv_ai.user_context.get("timestamp")
            }
        
        return sessions

# Global chat manager instance
chat_manager: Optional[ChatManager] = None

def get_chat_manager() -> ChatManager:
    """Get global chat manager instance"""
    global chat_manager
    if chat_manager is None:
        raise RuntimeError("Chat manager not initialized")
    return chat_manager

def initialize_chat_manager(openai_client):
    """Initialize global chat manager"""
    global chat_manager
    chat_manager = ChatManager(openai_client)