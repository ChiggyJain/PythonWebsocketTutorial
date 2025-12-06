import asyncio
import websockets

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNoaXJhZyJ9.Gff-Esi8_YMgcZVI-MYyxLroQZTiqHkdO4d5v7rVHwY"

async def run():
    ws = await websockets.connect(f"ws://localhost:9002/ws?token={TOKEN}")
    print("Connected")
    await ws.send("Hello!")
    print("Sent")
    response = await ws.recv()
    print("Received:", response)

asyncio.run(run())
