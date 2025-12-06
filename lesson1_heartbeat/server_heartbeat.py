import asyncio
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

async def handler(websocket):
    print("🔌 [OPEN] Client connected")
    try:
        async for message in websocket:
            print(f"📩 [RECEIVED] {message}")
            response = message
            await websocket.send(response)
            print(f"📤 [SENT] {response}")
    except ConnectionClosedOK:
        print("🔚 [CLOSED] Client closed connection normally (1000)")

    except ConnectionClosedError as e:
        print(f"⚠️ [ERROR] Abnormal disconnect (1006). Details: {e}")

    except Exception as e:
        print(f"🔥 [SERVER ERROR] {e}")

    finally:
        print(f"🏁 [FINALLY] Cleanup. Close code: {websocket.close_code}, Reason: {websocket.close_reason}")


async def main():
    server = await websockets.serve(
        handler, "localhost", 9001, 
        # sending periodic pings to clients every 10 seconds, with a timeout of 5 seconds
        # data is sent as a ping control frame in websocket internally and end-user can see the messages on screen/console/logs etc 
        ping_interval=10, 
        ping_timeout=5
    )
    print("Server started ws://localhost:9001 abnd waiting for clients...")
    # keeping the server forever running
    await server.wait_closed()
    print("Server fully stopped")

asyncio.run(main())
