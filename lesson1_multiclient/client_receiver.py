import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:9001"
    async with websockets.connect(uri, ping_interval=None) as ws:
        print("Client receiver is connected to server")
        async for message in ws:
            print(f"Received-Msg: {message}")


asyncio.run(test_client())
