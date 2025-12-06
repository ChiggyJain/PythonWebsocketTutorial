from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from auth import decode_token
from room_manager import RoomManager
from redis.asyncio import Redis
from presence_service import PresenceService
from fastapi.responses import JSONResponse


app = FastAPI()
manager = RoomManager()

# Create Redis client (default localhost:6379)
redis = Redis(host="localhost", port=6379, db=0)
presence = PresenceService(redis)


@app.on_event("shutdown")
async def shutdown():
    await redis.aclose()


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

    # Mark online globally
    await presence.set_online(username, role)

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
                # Update presence in Redis for room
                await presence.move_to_room(username, room)
                # broadcast to room
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
        # Update Redis presence as offline
        await presence.set_offline(username)


@app.get("/presence/online-users")
async def get_online_users():
    users = await presence.get_online_users()
    return {"online_users": users}

@app.get("/presence/room/{room_name}")
async def get_room_presence(room_name: str):
    users = await presence.get_room_users(room_name)
    return {"room": room_name, "online_users": users}

@app.get("/presence/user/{username}")
async def get_user_status(username: str):
    data = await presence.get_user_presence(username)
    if not data:
        return JSONResponse({"detail": "User not found"}, status_code=404)
    return data
