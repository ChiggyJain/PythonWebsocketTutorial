import asyncio
import websockets

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNoaXJhZyJ9.Gff-Esi8_YMgcZVI-MYyxLroQZTiqHkdO4d5v7rVHwY"

async def run():
    ws = await websockets.connect(f"ws://localhost:9007/ws?token={TOKEN}")
    await ws.send('{"action":"join","room":"Room1"}')
    async for message in ws:
        print("📩", message)

asyncio.run(run())
