import asyncio
import websockets
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNoaXJhZyJ9.Gff-Esi8_YMgcZVI-MYyxLroQZTiqHkdO4d5v7rVHwY"

async def run():
    ws = await websockets.connect(f"ws://localhost:9007/ws?token={TOKEN}")
    await ws.send(json.dumps({"action": "join", "room": "Room1"}))
    while True:
        msg = input("You: ")
        await ws.send(json.dumps({"action": "send", "room": "Room1", "message": msg}))

asyncio.run(run())
