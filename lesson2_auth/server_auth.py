import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
import jwt
from jwt.exceptions import InvalidTokenError
from urllib.parse import urlparse, parse_qs

SECRET_KEY = "MY_SUPER_SECRET_KEY"

async def authenticate(websocket):
    # Parse URL: ws://localhost:9006/ws?token=ABC
    query = urlparse(websocket.path).query
    params = parse_qs(query)
    token = params.get("token", [None])[0]
    if not token:
        await websocket.close(code=4001, reason="Missing Token")
        raise ConnectionClosed(4001, "Missing Token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Auth success:", payload)
        return payload
    except InvalidTokenError:
        await websocket.close(code=4002, reason="Invalid Token")
        raise ConnectionClosed(4002, "Invalid Token")


async def handler(ws):
    try:
        # authenticate user
        user = await authenticate(ws)
        # Main message loop
        async for message in ws:
            print(f"📩 From {user['username']}: {message}")
            await ws.send(f"Hi {user['username']}, you said: {message}")
    except ConnectionClosed as e:
        print("Closed:", e.code, e.reason)
    finally:
        print("Cleanup done")


async def main():
    print("Websocket server starting on ws://localhost:9002")
    server = await websockets.serve(handler, "localhost", 9002)
    # forever running server
    await server.wait_closed()

asyncio.run(main())
