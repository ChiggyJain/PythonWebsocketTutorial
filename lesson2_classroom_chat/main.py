from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from auth import decode_token
from room_manager import RoomManager

app = FastAPI()
manager = RoomManager()


@app.websocket("/ws")
async def classroom_socket(ws: WebSocket):

    # accepting the websocket client connection
    await ws.accept()

    # Extract token for authentication
    token = ws.query_params.get("token")
    try:
        user = decode_token(token)
    except Exception as e:
        await ws.send_text(f"Auth Error: {str(e)}")
        await ws.close(code=4001)
        return

    username = user["username"]
    role = user["role"]
    print(f"User Connected → {username} ({role})")

    joined_rooms = set()

    try:
        # Main WebSocket message loop
        while True:
            data = await ws.receive_json()
            action = data.get("action")

            # JOIN ROOM
            if action == "join":
                room = data["room"]
                await manager.join_room(room, ws)
                joined_rooms.add(room)
                await manager.broadcast(room, f"📢 {username} joined {room}")

            # SEND MESSAGE
            elif action == "send":
                room = data["room"]
                message = data["message"]
                await manager.broadcast(room, f"[{username}] {message}")

            # TEACHER ANNOUNCEMENT (to all rooms)
            elif action == "announcement":
                if role != "teacher":
                    await ws.send_text("❌ Only teachers can send announcements")
                else:
                    for room_name in manager.rooms.keys():
                        await manager.broadcast(room_name, f"📣 Teacher {username}: {data['message']}")

            # LEAVE ROOM
            elif action == "leave":
                room = data["room"]
                await manager.leave_room(room, ws)
                joined_rooms.remove(room)
                await manager.broadcast(room, f"👋 {username} left {room}")

    except WebSocketDisconnect:
        print(f"❌ Disconnected: {username}")
    finally:
        await manager.disconnect(ws)
        print(f"🏁 Cleanup done for {username}")
