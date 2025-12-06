import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:9001"
    async with websockets.connect(uri) as ws:
        print("🔗 Connected to server")
        await ws.send("Hey server!")
        print("📤 Sent message")
        response = await ws.recv()
        print(f"📩 Received: {response}")
        print("👋 Closing connection…")
        await ws.close()

asyncio.run(test_client())
