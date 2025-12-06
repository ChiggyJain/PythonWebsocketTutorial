import asyncio
import websockets
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNoaXJhZyIsInJvbGUiOiJzdHVkZW50In0.DD5qJH-mDtK2LBGKsTZKK31qFb7R32gupKAw3AVxt0w"

async def run():
    ws = await websockets.connect(f"ws://localhost:8000/ws?token={TOKEN}")
    await ws.send(json.dumps({"action": "join", "room": "Room1"}))
    
    async def listener(ws):
        async for msg in ws:
            print("📩", msg)

    async def sender(ws):
        while True:
            msg = await asyncio.to_thread(input, "You: ")
            await ws.send(json.dumps({"action": "send", "room": "Room1", "message": msg}))

    await asyncio.gather(
        listener(ws),
        sender(ws)
    )


asyncio.run(run())
