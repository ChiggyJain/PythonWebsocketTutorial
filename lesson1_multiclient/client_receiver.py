import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:9001"
    async with websockets.connect(uri) as ws:
        print(f"Client receiver is connected to server and MY-ID: {id(ws)}")
        async for message in ws:
            print(f"Received-Msg: {message}")


asyncio.run(test_client())
