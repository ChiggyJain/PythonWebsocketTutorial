import asyncio
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
connected_clients = set()

async def handler(websocket):
    print(f"Client connected and Memory-ID: {id(websocket)}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"From-Client-ID: {id(websocket)} and Received-Msg: {message}")
            await broadcast(f"To-Client-ID: {id(websocket)} and Sent-Msg: All-Good")
    except ConnectionClosedOK:
        print(f"[CLOSED] Client closed connection normally (1000), ID: {id(websocket)}")
    except ConnectionClosedError as e:
        print(f"[ERROR] Abnormal disconnect (1006). Details: {e}, ID: {id(websocket)}")
    except Exception as e:
        print(f"[SERVER ERROR] {e}, ID: {id(websocket)}")
    finally:
        print(f"[FINALLY] Cleanup. Close code: {websocket.close_code}, Reason: {websocket.close_reason}")
        connected_clients.remove(websocket)


async def broadcast(msg):
    print(f"Broadcasting msg to all connected-clients")
    if not connected_clients:
        print(f"No connected clients on websocket")
        return None
    # sending msg to all connected clients
    disconnected = []
    for websocket in connected_clients:
        try:
            await websocket.send(msg)
        except Exception as e:
            disconnected.append(websocket)
    # Cleanup any dead connections
    for websocket in disconnected:
        connected_clients.remove(websocket)
        

async def main():
    server = await websockets.serve(
        handler, "localhost", 9001, 
        # sending periodic pings to clients every 10 seconds, with a timeout of 5 seconds
        # data is sent as a ping control frame in websocket internally and end-user can see the messages on screen/console/logs etc 
        #ping_interval=10, 
        #ping_timeout=5
    )
    print("Server started ws://localhost:9001 and waiting for client-connection...")
    # keeping the server forever running
    await server.wait_closed()
    print("Server fully stopped")

asyncio.run(main())
