from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.websocket import manager
from ..core.security import decode_token
import json

router = APIRouter()

@router.websocket("/ws/{workspace_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    workspace_id: str,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time collaboration"""
    
    # Authenticate via token
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        user_email = payload.get("email")
        
        if not user_id:
            await websocket.close(code=1008)
            return
    except:
        await websocket.close(code=1008)
        return
    
    # Connect
    connection_id = await manager.connect(websocket, workspace_id, user_id, user_email)
    
    # Send welcome message
    await manager.send_personal_message({
        "type": "connection_established",
        "connection_id": connection_id,
        "workspace_id": workspace_id,
        "online_users": manager.get_online_users(workspace_id)
    }, websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "document_update":
                # Broadcast document update to all users
                await manager.broadcast_to_workspace(workspace_id, {
                    "type": "document_updated",
                    "document_id": message.get("document_id"),
                    "document_type": message.get("document_type"),
                    "updated_by": user_email,
                    "changes": message.get("changes"),
                    "timestamp": message.get("timestamp")
                }, exclude_websocket=websocket)
            
            elif message_type == "typing":
                # Broadcast typing indicator
                await manager.broadcast_to_workspace(workspace_id, {
                    "type": "user_typing",
                    "user_email": user_email,
                    "location": message.get("location")
                }, exclude_websocket=websocket)
            
            elif message_type == "cursor_position":
                # Broadcast cursor position for collaborative editing
                await manager.broadcast_to_workspace(workspace_id, {
                    "type": "cursor_moved",
                    "user_email": user_email,
                    "position": message.get("position")
                }, exclude_websocket=websocket)
            
            elif message_type == "ping":
                # Keepalive ping
                await manager.send_personal_message({
                    "type": "pong"
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(connection_id)

@router.get("/realtime/online-users/{workspace_id}")
async def get_online_users(workspace_id: str):
    """Get currently online users (HTTP endpoint)"""
    return {
        "workspace_id": workspace_id,
        "count": len(manager.get_online_users(workspace_id)),
        "users": manager.get_online_users(workspace_id)
    }
