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
        # sending the close frame to websocket server with normal closure code 1000 and reason
        await ws.close(code=1000, reason="Client task completed")

asyncio.run(test_client())
