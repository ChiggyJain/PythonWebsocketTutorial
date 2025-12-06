import asyncio
import websockets
import json

async def run():
    uri = "ws://localhost:9007"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to websocker server at {uri}")

        # Join a room
        room_name = "Room1"
        join_message = json.dumps({"action": "join", "room": room_name})
        await websocket.send(join_message)
        response = await websocket.recv()
        print(f"Server response after room {room_name} joined: {response}")

        # Send a message to the room
        chat_message = json.dumps({"action": "message", "room": room_name, "message": "Hello, Room!"})
        await websocket.send(chat_message)

        # Listen for messages from the server
        async def listener(websocket):
            async for message in websocket:
                print(f"Received message from server: {message}")

        # sending messages
        async def sender(ws):
            while True:
                msg = await asyncio.to_thread(input, "You: ")
                await ws.send(json.dumps({
                    "action": "message",
                    "room": "Room1",
                    "message": msg
                }))

        await asyncio.gather(
            listener(websocket),
            sender(websocket)
        )

asyncio.run(run())