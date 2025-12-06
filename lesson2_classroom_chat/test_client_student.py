import asyncio
import websockets
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNoaXJhZyIsInJvbGUiOiJzdHVkZW50In0.DD5qJH-mDtK2LBGKsTZKK31qFb7R32gupKAw3AVxt0w"

async def run():
    ws = await websockets.connect(f"ws://localhost:8000/ws?token={TOKEN}")
    await ws.send(json.dumps({"action": "join", "room": "Room1"}))
    async def listener():
        async for msg in ws:
            print("📩", msg)
    asyncio.create_task(listener())
    while True:
        msg = input("You: ")
        await ws.send(json.dumps({"action": "send", "room": "Room1", "message": msg}))

asyncio.run(run())
