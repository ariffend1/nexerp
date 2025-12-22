from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import uuid
import json
from datetime import datetime

class ConnectionManager:
    """Manage WebSocket connections for real-time features"""
    
    def __init__(self):
        # workspace_id -> list of WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # connection_id -> user_info
        self.user_sessions: Dict[str, dict] = {}
    
    async def connect(self, websocket: WebSocket, workspace_id: str, user_id: str, user_email: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        connection_id = str(uuid.uuid4())
        
        # Store connection
        if workspace_id not in self.active_connections:
            self.active_connections[workspace_id] = []
        self.active_connections[workspace_id].append(websocket)
        
        # Store user session
        self.user_sessions[connection_id] = {
            "websocket": websocket,
            "workspace_id": workspace_id,
            "user_id": user_id,
            "user_email": user_email,
            "connected_at": datetime.now().isoformat()
        }
        
        # Notify others of new connection
        await self.broadcast_to_workspace(workspace_id, {
            "type": "user_connected",
            "user_id": user_id,
            "user_email": user_email,
            "timestamp": datetime.now().isoformat()
        }, exclude_websocket=websocket)
        
        return connection_id
    
    def disconnect(self, connection_id: str):
        """Remove WebSocket connection"""
        if connection_id in self.user_sessions:
            session = self.user_sessions[connection_id]
            workspace_id = session["workspace_id"]
            websocket = session["websocket"]
            
            # Remove from active connections
            if workspace_id in self.active_connections:
                self.active_connections[workspace_id].remove(websocket)
                
                if len(self.active_connections[workspace_id]) == 0:
                    del self.active_connections[workspace_id]
            
            # Notify others of disconnection
            self.broadcast_to_workspace_sync(workspace_id, {
                "type": "user_disconnected",
                "user_id": session["user_id"],
                "user_email": session["user_email"],
                "timestamp": datetime.now().isoformat()
            })
            
            del self.user_sessions[connection_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        await websocket.send_json(message)
    
    async def broadcast_to_workspace(self, workspace_id: str, message: dict, exclude_websocket: WebSocket = None):
        """Broadcast message to all connections in workspace"""
        if workspace_id in self.active_connections:
            for connection in self.active_connections[workspace_id]:
                if connection != exclude_websocket:
                    try:
                        await connection.send_json(message)
                    except:
                        pass  # Connection might be closed
    
    def broadcast_to_workspace_sync(self, workspace_id: str, message: dict):
        """Synchronous broadcast (for disconnect)"""
        import asyncio
        if workspace_id in self.active_connections:
            for connection in self.active_connections[workspace_id]:
                try:
                    asyncio.create_task(connection.send_json(message))
                except:
                    pass
    
    def get_online_users(self, workspace_id: str) -> List[dict]:
        """Get list of online users in workspace"""
        online_users = []
        for session_id, session in self.user_sessions.items():
            if session["workspace_id"] == workspace_id:
                online_users.append({
                    "user_id": session["user_id"],
                    "user_email": session["user_email"],
                    "connected_at": session["connected_at"]
                })
        return online_users

# Global connection manager instance
manager = ConnectionManager()
