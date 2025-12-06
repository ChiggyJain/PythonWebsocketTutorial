import asyncio
import websockets

async def handler(ws):
    print("🔌 Client connected")
    try:
        while True:
            message = await ws.recv()
            print("📩 Received text:", message)
            response = message
            await ws.send(response)
            print(f"📤 [SENT] {response}")
    except websockets.ConnectionClosed as e:
        print(f"❌ Connection closed. Code: {e.code}, Reason: {e.reason}")
    finally:
        print("🏁 Cleanup complete")


async def heartbeat_monitor(ws):
    while True:
        print("📤 Sending PING manually")
        pong_waiter = await ws.ping()
        try:
            await asyncio.wait_for(pong_waiter, timeout=5)
            print("📥 Received PONG")
        except asyncio.TimeoutError:
            print("❌ Client did not respond to PING, closing...")
            await ws.close(code=1001, reason="No heartbeat")
            break
        await asyncio.sleep(10)


async def main_handler(ws):
    task1 = asyncio.create_task(handler(ws))
    task2 = asyncio.create_task(heartbeat_monitor(ws))
    await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)


async def main():
    async with websockets.serve(main_handler, "localhost", 9001):
        print("🚀 Server started ws://localhost:9001")
        # keeping the server forever running
        await asyncio.Future()

asyncio.run(main())
