import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:9001"
    async with websockets.connect(uri) as ws:
        print(f"Client sender is connected to server and MY-ID: {id(ws)}")
        while True:
            msg = input("You: ")
            await ws.send(msg)

asyncio.run(test_client())
