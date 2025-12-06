import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:9001"
    async with websockets.connect(uri, ping_interval=None) as ws:
        print("Client sender is connected to server")
        while True:
            msg = input("You: ")
            await ws.send(msg)

asyncio.run(test_client())
