import asyncio
import websockets


async def echo_handler(websocket):
    try:
        async for message in websocket:
            print(f"Received msg from client: {message}")
            rsp = f"Echo-{message}"
            await websocket.send(rsp)
            print(f"Sent msg to client: {rsp}")
    except Exception as e:
        pass
    finally:
        print(f"Connection handler finished")

async def main():
    # Start a WebSocket server on ws://localhost:8765
    async with websockets.serve(echo_handler, "localhost", 8765):
        print(f"Websocket server started at ws://localhost:8765")
        # Keep server running forever
        await asyncio.Future()




if __name__ == "__main__":
    asyncio.run(main())