"""
Real-time Collaboration System
สำหรับการทำงานแบบ multi-user real-time เหมือน Figma/Lovable
"""

import asyncio
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import websockets
from datetime import datetime

@dataclass
class User:
    user_id: str
    name: str
    avatar: str
    cursor_position: Dict[str, Any]
    active_file: Optional[str]
    permissions: List[str]
    connected_at: float
    last_activity: float

@dataclass  
class LiveCursor:
    user_id: str
    file_path: str
    line: int
    column: int
    selection: Optional[Dict[str, Any]]
    timestamp: float

@dataclass
class FileChange:
    change_id: str
    user_id: str
    file_path: str
    change_type: str  # insert, delete, replace
    content: str
    position: Dict[str, Any]
    timestamp: float

@dataclass
class ChatMessage:
    message_id: str
    user_id: str
    content: str
    message_type: str  # text, code, suggestion, system
    timestamp: float
    reactions: Dict[str, List[str]]

@dataclass
class ProjectVersion:
    version_id: str
    author_id: str
    description: str
    files_changed: List[str]
    changes: List[FileChange]
    created_at: float

class RealTimeCollaborationSystem:
    """Real-time collaboration system for multi-user development"""
    
    def __init__(self, project_id: str, workspace_path: Path):
        self.project_id = project_id
        self.workspace = workspace_path
        
        # Collaboration state
        self.active_users: Dict[str, User] = {}
        self.live_cursors: Dict[str, LiveCursor] = {}
        self.file_changes: List[FileChange] = []
        self.chat_messages: List[ChatMessage] = []
        self.version_history: List[ProjectVersion] = []
        
        # WebSocket connections
        self.websocket_connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        
        # Real-time synchronization
        self.sync_queue: asyncio.Queue = asyncio.Queue()
        self.file_locks: Dict[str, str] = {}  # file_path -> user_id
        
        # Voice/Video chat (placeholder for future implementation)
        self.voice_rooms: Dict[str, Set[str]] = {}
        
    async def start_collaboration_server(self, port: int = 8765):
        """Start WebSocket server for real-time collaboration"""
        
        async def handle_client(websocket, path):
            try:
                await self.handle_new_connection(websocket)
            except websockets.exceptions.ConnectionClosed:
                pass
            except Exception as e:
                print(f"Collaboration error: {e}")
        
        server = await websockets.serve(handle_client, "localhost", port)
        print(f"Collaboration server started on ws://localhost:{port}")
        
        return server
    
    async def handle_new_connection(self, websocket):
        """Handle new user connection"""
        
        user_id = str(uuid.uuid4())
        self.websocket_connections[user_id] = websocket
        
        try:
            # Send initial project state
            await self.send_initial_state(websocket, user_id)
            
            # Handle messages from client
            async for message in websocket:
                await self.handle_client_message(user_id, json.loads(message))
                
        finally:
            # Clean up on disconnect
            await self.handle_user_disconnect(user_id)
    
    async def send_initial_state(self, websocket, user_id: str):
        """Send initial project state to new user"""
        
        initial_state = {
            "type": "initial_state",
            "project_id": self.project_id,
            "user_id": user_id,
            "active_users": [asdict(user) for user in self.active_users.values()],
            "file_structure": await self.get_file_structure(),
            "recent_changes": self.file_changes[-50:] if self.file_changes else [],
            "chat_messages": self.chat_messages[-100:] if self.chat_messages else [],
            "version_info": self.version_history[-1] if self.version_history else None
        }
        
        await websocket.send(json.dumps(initial_state))
    
    async def handle_client_message(self, user_id: str, message: Dict[str, Any]):
        """Handle incoming message from client"""
        
        message_type = message.get("type")
        
        if message_type == "user_join":
            await self.handle_user_join(user_id, message["data"])
        elif message_type == "cursor_move":
            await self.handle_cursor_move(user_id, message["data"])
        elif message_type == "file_change":
            await self.handle_file_change(user_id, message["data"])
        elif message_type == "chat_message":
            await self.handle_chat_message(user_id, message["data"])
        elif message_type == "file_lock":
            await self.handle_file_lock(user_id, message["data"])
        elif message_type == "voice_request":
            await self.handle_voice_request(user_id, message["data"])
    
    async def handle_user_join(self, user_id: str, data: Dict[str, Any]):
        """Handle user joining collaboration session"""
        
        user = User(
            user_id=user_id,
            name=data.get("name", f"User {user_id[:8]}"),
            avatar=data.get("avatar", ""),
            cursor_position={},
            active_file=None,
            permissions=data.get("permissions", ["read", "write"]),
            connected_at=time.time(),
            last_activity=time.time()
        )
        
        self.active_users[user_id] = user
        
        # Broadcast user join to all other users
        await self.broadcast_to_others(user_id, {
            "type": "user_joined",
            "data": asdict(user)
        })
    
    async def handle_cursor_move(self, user_id: str, data: Dict[str, Any]):
        """Handle user cursor movement"""
        
        cursor = LiveCursor(
            user_id=user_id,
            file_path=data["file_path"],
            line=data["line"],
            column=data["column"],
            selection=data.get("selection"),
            timestamp=time.time()
        )
        
        self.live_cursors[user_id] = cursor
        
        # Update user activity
        if user_id in self.active_users:
            self.active_users[user_id].last_activity = time.time()
            self.active_users[user_id].active_file = data["file_path"]
        
        # Broadcast cursor position to other users
        await self.broadcast_to_others(user_id, {
            "type": "cursor_update",
            "data": asdict(cursor)
        })
    
    async def handle_file_change(self, user_id: str, data: Dict[str, Any]):
        """Handle file content changes"""
        
        change = FileChange(
            change_id=str(uuid.uuid4()),
            user_id=user_id,
            file_path=data["file_path"],
            change_type=data["change_type"],
            content=data["content"],
            position=data["position"],
            timestamp=time.time()
        )
        
        self.file_changes.append(change)
        
        # Apply change to filesystem
        await self.apply_file_change(change)
        
        # Broadcast change to other users
        await self.broadcast_to_others(user_id, {
            "type": "file_changed",
            "data": asdict(change)
        })
        
        # Auto-save version if significant changes
        if len(self.file_changes) % 10 == 0:
            await self.create_auto_version(user_id)
    
    async def handle_chat_message(self, user_id: str, data: Dict[str, Any]):
        """Handle chat messages"""
        
        message = ChatMessage(
            message_id=str(uuid.uuid4()),
            user_id=user_id,
            content=data["content"],
            message_type=data.get("type", "text"),
            timestamp=time.time(),
            reactions={}
        )
        
        self.chat_messages.append(message)
        
        # Broadcast message to all users
        await self.broadcast_to_all({
            "type": "chat_message",
            "data": asdict(message)
        })
        
        # Handle AI assistance requests
        if message.content.startswith("/ai "):
            await self.handle_ai_assistance_request(user_id, message.content[4:])
    
    async def handle_file_lock(self, user_id: str, data: Dict[str, Any]):
        """Handle file locking for exclusive editing"""
        
        file_path = data["file_path"]
        action = data["action"]  # "lock" or "unlock"
        
        if action == "lock":
            if file_path not in self.file_locks or self.file_locks[file_path] == user_id:
                self.file_locks[file_path] = user_id
                success = True
            else:
                success = False
        else:  # unlock
            if file_path in self.file_locks and self.file_locks[file_path] == user_id:
                del self.file_locks[file_path]
                success = True
            else:
                success = False
        
        # Send lock status update
        await self.broadcast_to_all({
            "type": "file_lock_update",
            "data": {
                "file_path": file_path,
                "locked_by": self.file_locks.get(file_path),
                "success": success
            }
        })
    
    async def handle_voice_request(self, user_id: str, data: Dict[str, Any]):
        """Handle voice chat requests"""
        
        room_id = data.get("room_id", "default")
        action = data["action"]  # "join" or "leave"
        
        if action == "join":
            if room_id not in self.voice_rooms:
                self.voice_rooms[room_id] = set()
            self.voice_rooms[room_id].add(user_id)
        else:  # leave
            if room_id in self.voice_rooms:
                self.voice_rooms[room_id].discard(user_id)
                if not self.voice_rooms[room_id]:
                    del self.voice_rooms[room_id]
        
        # Broadcast voice room update
        await self.broadcast_to_all({
            "type": "voice_room_update",
            "data": {
                "room_id": room_id,
                "participants": list(self.voice_rooms.get(room_id, []))
            }
        })
    
    async def handle_ai_assistance_request(self, user_id: str, prompt: str):
        """Handle AI assistance requests in chat"""
        
        # This would integrate with the AI system
        ai_response = await self.get_ai_suggestion(prompt)
        
        ai_message = ChatMessage(
            message_id=str(uuid.uuid4()),
            user_id="ai_assistant",
            content=ai_response,
            message_type="ai_suggestion",
            timestamp=time.time(),
            reactions={}
        )
        
        self.chat_messages.append(ai_message)
        
        await self.broadcast_to_all({
            "type": "chat_message",
            "data": asdict(ai_message)
        })
    
    async def handle_user_disconnect(self, user_id: str):
        """Handle user disconnection"""
        
        # Remove user from active users
        if user_id in self.active_users:
            del self.active_users[user_id]
        
        # Remove cursor
        if user_id in self.live_cursors:
            del self.live_cursors[user_id]
        
        # Release file locks
        locked_files = [path for path, locker in self.file_locks.items() if locker == user_id]
        for file_path in locked_files:
            del self.file_locks[file_path]
        
        # Remove from voice rooms
        for room_participants in self.voice_rooms.values():
            room_participants.discard(user_id)
        
        # Remove WebSocket connection
        if user_id in self.websocket_connections:
            del self.websocket_connections[user_id]
        
        # Broadcast user disconnect
        await self.broadcast_to_all({
            "type": "user_disconnected",
            "data": {"user_id": user_id}
        })
    
    async def broadcast_to_all(self, message: Dict[str, Any]):
        """Broadcast message to all connected users"""
        
        if not self.websocket_connections:
            return
        
        message_str = json.dumps(message)
        
        # Send to all connections
        disconnected = []
        for user_id, websocket in self.websocket_connections.items():
            try:
                await websocket.send(message_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected:
            await self.handle_user_disconnect(user_id)
    
    async def broadcast_to_others(self, sender_id: str, message: Dict[str, Any]):
        """Broadcast message to all users except sender"""
        
        message_str = json.dumps(message)
        
        disconnected = []
        for user_id, websocket in self.websocket_connections.items():
            if user_id != sender_id:
                try:
                    await websocket.send(message_str)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected:
            await self.handle_user_disconnect(user_id)
    
    async def apply_file_change(self, change: FileChange):
        """Apply file change to filesystem"""
        
        file_path = self.workspace / change.file_path
        
        try:
            if change.change_type == "create":
                # Create new file
                file_path.parent.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(file_path, "w") as f:
                    await f.write(change.content)
            
            elif change.change_type == "replace":
                # Replace entire file content
                async with aiofiles.open(file_path, "w") as f:
                    await f.write(change.content)
            
            elif change.change_type == "insert":
                # Insert content at position
                if file_path.exists():
                    async with aiofiles.open(file_path, "r") as f:
                        current_content = await f.read()
                    
                    lines = current_content.split("\\n")
                    line_num = change.position.get("line", 0)
                    col_num = change.position.get("column", 0)
                    
                    if line_num < len(lines):
                        line = lines[line_num]
                        lines[line_num] = line[:col_num] + change.content + line[col_num:]
                        
                        async with aiofiles.open(file_path, "w") as f:
                            await f.write("\\n".join(lines))
            
            elif change.change_type == "delete":
                # Delete content at position
                if file_path.exists():
                    async with aiofiles.open(file_path, "r") as f:
                        current_content = await f.read()
                    
                    # Apply deletion logic
                    # Implementation depends on specific deletion requirements
                    pass
        
        except Exception as e:
            print(f"Error applying file change: {e}")
    
    async def create_auto_version(self, author_id: str):
        """Create automatic version checkpoint"""
        
        recent_changes = self.file_changes[-10:] if self.file_changes else []
        files_changed = list(set(change.file_path for change in recent_changes))
        
        version = ProjectVersion(
            version_id=f"auto_{int(time.time())}",
            author_id=author_id,
            description=f"Auto-save checkpoint with {len(recent_changes)} changes",
            files_changed=files_changed,
            changes=recent_changes,
            created_at=time.time()
        )
        
        self.version_history.append(version)
        
        # Broadcast version creation
        await self.broadcast_to_all({
            "type": "version_created",
            "data": asdict(version)
        })
    
    async def get_file_structure(self) -> Dict[str, Any]:
        """Get current file structure"""
        
        def scan_directory(path: Path, relative_to: Path) -> Dict[str, Any]:
            structure = {}
            
            try:
                for item in path.iterdir():
                    relative_path = item.relative_to(relative_to)
                    
                    if item.is_file():
                        structure[str(relative_path)] = {
                            "type": "file",
                            "size": item.stat().st_size,
                            "modified": item.stat().st_mtime
                        }
                    elif item.is_dir() and not item.name.startswith("."):
                        structure[str(relative_path)] = {
                            "type": "directory",
                            "children": scan_directory(item, relative_to)
                        }
            except PermissionError:
                pass
            
            return structure
        
        return scan_directory(self.workspace, self.workspace)
    
    async def get_ai_suggestion(self, prompt: str) -> str:
        """Get AI suggestion for collaboration chat"""
        
        # This would integrate with the main AI system
        # For now, return a placeholder response
        return f"AI suggestion for: {prompt} (This would be implemented with actual AI integration)"
    
    async def export_collaboration_session(self) -> Dict[str, Any]:
        """Export entire collaboration session for analysis"""
        
        return {
            "project_id": self.project_id,
            "session_data": {
                "active_users": [asdict(user) for user in self.active_users.values()],
                "total_changes": len(self.file_changes),
                "chat_messages": len(self.chat_messages),
                "versions": len(self.version_history),
                "voice_rooms": {room: list(participants) for room, participants in self.voice_rooms.items()}
            },
            "statistics": {
                "most_active_user": max(self.active_users.keys(), key=lambda u: len([c for c in self.file_changes if c.user_id == u])) if self.file_changes else None,
                "most_edited_file": max(set(change.file_path for change in self.file_changes), key=lambda f: len([c for c in self.file_changes if c.file_path == f])) if self.file_changes else None,
                "collaboration_duration": time.time() - min([user.connected_at for user in self.active_users.values()]) if self.active_users else 0
            },
            "exported_at": time.time()
        }

# Factory function to create collaboration system
def create_collaboration_system(project_id: str, workspace_path: Path) -> RealTimeCollaborationSystem:
    """Create new real-time collaboration system for project"""
    return RealTimeCollaborationSystem(project_id, workspace_path)