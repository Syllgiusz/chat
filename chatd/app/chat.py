from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter()
active_connections: Dict[int, List[WebSocket]] = {}

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")
            user_id = data.get("user_id")
            username = data.get("username", "")
            message = f"{username}: {content}"
            for conn in active_connections[room_id]:
                await conn.send_text(message)
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
