from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from auth import authenticate
from room_manager import RoomManager

app = FastAPI()
manager = RoomManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # accepting the websocket client connection
    await websocket.accept()

    # Extract token for authentication
    token = websocket.query_params.get("token")
    try:
        user = authenticate(token)
    except Exception as e:
        await websocket.send_text(f"Auth failed: {str(e)}")
        await websocket.close(code=4001)
        return

    username = user["username"]
    print(f"Authenticated user: {username}")

    joined_rooms = set()

    try:
        # Main WebSocket message loop
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            # JOIN ROOM
            if action == "join":
                room = data["room"]
                await manager.join_room(room, websocket)
                joined_rooms.add(room)
                await manager.broadcast(room, f"📢 {username} joined {room}")

            # LEAVE ROOM
            elif action == "leave":
                room = data["room"]
                await manager.leave_room(room, websocket)
                joined_rooms.remove(room)
                await manager.broadcast(room, f"👋 {username} left {room}")

            # SEND MESSAGE TO ROOM
            elif action == "send":
                room = data["room"]
                message = data["message"]
                await manager.broadcast(room, f"[{username}] {message}")

    except WebSocketDisconnect:
        print(f"❌ User disconnected: {username}")
    finally:
        # remove from all rooms
        await manager.disconnect(websocket)
        print(f"🏁 Cleanup done for {username}")
