import asyncio
import websockets
import json

# per room-name storage of ws connections
rooms = {}


async def get_room_connections(room_name):
    if room_name not in rooms:
        rooms[room_name] = set()
    return rooms[room_name]


async def broadcast_message(room_name, message):
    connections = await get_room_connections(room_name)
    if not connections:
        return
    if connections:
        disconnected = set()
        for ws in connections:
            try:
                await ws.send(message)
            except websockets.ConnectionClosed:
                disconnected.add(ws)
        connections.difference_update(disconnected)


async def handler(websocket):
    print(f"Client connected on websocket and ID: {id(websocket)}")
    joined_rooms = set()
    try:
        async for raw in websocket:
            print(f"Received raw data from client ID {id(websocket)}: {raw}")
            data = json.loads(raw)
            action = data.get("action")
            room_name = data.get("room")
            message = data.get("message", "")
            if action == "join":
                connections = await get_room_connections(room_name)
                connections.add(websocket)
                joined_rooms.add(room_name)
                await websocket.send(f"Client joined room: {room_name} and ID: {id(websocket)}")
            elif action == "leave":
                connections = await get_room_connections(room_name)
                connections.discard(websocket)
                joined_rooms.discard(room_name)
                await websocket.send(f"Client left room: {room_name} and ID: {id(websocket)}")
            elif action == "message":
                if room_name in joined_rooms:
                    await broadcast_message(room_name, message)
                else:
                    await websocket.send(f"Error: Not in room {room_name} and ID: {id(websocket)}")
    except Exception as e:
        pass
    finally:
        for room_name in joined_rooms:
            connections = await get_room_connections(room_name)
            connections.discard(websocket)
            joined_rooms.discard(room_name)
        print(f"Client disconnected from websocket ID: {id(websocket)}")


async def main():
    async with websockets.serve(handler, "localhost", 9007):
        print("Websocker server at ws://localhost:9007")
        # run forever
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())