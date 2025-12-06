from typing import Dict, Set
from fastapi import WebSocket
from websockets.exceptions import ConnectionClosed

class RoomManager:

    # own constructor
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    # fetching all websocket connection for given respective room
    def get_room(self, room_name: str):
        if room_name not in self.rooms:
            self.rooms[room_name] = set()
        return self.rooms[room_name]

    # adding websocket connection to given room
    async def join_room(self, room_name: str, ws: WebSocket):
        room = self.get_room(room_name)
        room.add(ws)

    # leaving websocket connection from given room
    async def leave_room(self, room_name: str, ws: WebSocket):
        room = self.get_room(room_name)
        if ws in room:
            room.remove(ws)

    # sending text-message to all websocket connections in given room 
    async def broadcast(self, room_name: str, message: str):
        room = self.get_room(room_name)
        dead = []
        for ws in room:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            room.remove(ws)

    # removing websocket connection from all rooms
    async def disconnect(self, ws: WebSocket):
        # Remove from all rooms
        for room_name, room in self.rooms.items():
            if ws in room:
                room.remove(ws)
