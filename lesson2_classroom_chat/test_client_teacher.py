import asyncio
import websockets
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlYWNoZXIxIiwicm9sZSI6InRlYWNoZXIifQ.T6DlwudSbTWi-7bMgWUXOmoRDo75w53ypy4LM7nYrdU"

async def run():
    ws = await websockets.connect(f"ws://localhost:8000/ws?token={TOKEN}")
    await ws.send(json.dumps({"action": "join", "room": "Room1"}))
    async def listener():
        async for msg in ws:
            print("📩", msg)
    asyncio.create_task(listener())
    while True:
        msg = input("(Teacher) Message/Announcement: ")
        if msg.startswith("ann:"):
            announcement = msg.replace("ann:", "")
            await ws.send(json.dumps({"action": "announcement", "message": announcement}))
        else:
            await ws.send(json.dumps({"action": "send", "room": "Room1", "message": msg}))

asyncio.run(run())
