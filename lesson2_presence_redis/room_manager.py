from fastapi import WebSocket
from typing import Dict, Set
from websockets.exceptions import ConnectionClosed

class RoomManager:

    # own constructor
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    # fetching all websocket connection for given respective room
    def get_room(self, room):
        if room not in self.rooms:
            self.rooms[room] = set()
        return self.rooms[room]

    # adding websocket connection to given room
    async def join_room(self, room, ws: WebSocket):
        self.get_room(room).add(ws)

    # leaving websocket connection from given room
    async def leave_room(self, room, ws: WebSocket):
        if ws in self.get_room(room):
            self.rooms[room].remove(ws)

    # sending text-message to all websocket connections in given room
    async def broadcast(self, room, message: str):
        room_set = self.get_room(room)
        dead = []
        for ws in room_set:
            try:
                await ws.send_text(message)
            except:
                dead.append(ws)
        for ws in dead:
            room_set.remove(ws)

    # removing websocket connection from all rooms
    async def disconnect(self, ws: WebSocket):
        for room_name, members in self.rooms.items():
            if ws in members:
                members.remove(ws)
