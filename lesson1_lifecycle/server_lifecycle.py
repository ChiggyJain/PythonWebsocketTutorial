import asyncio
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

async def handler(websocket):
    print("🔌 [OPEN] Client connected")
    try:
        async for message in websocket:
            print(f"📩 [RECEIVED] {message}")
            response = f"Echo-{message}"
            await websocket.send(response)
            print(f"📤 [SENT] {response}")

    except ConnectionClosedOK:
        print("🔚 [CLOSED] Client closed connection normally (1000)")

    except ConnectionClosedError as e:
        print(f"⚠️ [ERROR] Abnormal disconnect (1006). Details: {e}")

    except Exception as e:
        print(f"🔥 [SERVER ERROR] {e}")

    finally:
        print("🏁 [FINALLY] Handler cleanup completed")


async def main():
    server = await websockets.serve(handler, "localhost", 9001)
    print("Server started ws://localhost:9001")
    await server.wait_closed()

asyncio.run(main())
