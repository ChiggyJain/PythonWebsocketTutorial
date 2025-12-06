import asyncio
import websockets

async def run_client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print(f"Client connected to websocket server")
        # Send 3 messages to websocket server
        for i in range(1,4):
            # sending msg to websocket server
            msg = f"Hello-Msg-{i}"
            await websocket.send(msg)
            # receiving response from websocket server
            rsp = await websocket.recv()
            print(f"Response got from websocket server after sending msg to websocket server: {rsp}")
        print(f"Closing connection from the websocket server")

if __name__ == "__main__":
    asyncio.run(run_client())