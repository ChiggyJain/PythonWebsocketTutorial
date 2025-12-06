import time
from typing import List
from redis.asyncio import Redis

class PresenceService:

    # own constructor
    def __init__(self, redis: Redis):
        self.redis = redis

    # Mark user as online
    async def set_online(self, username: str, role: str, room: str | None = None):

        # Add to global set
        await self.redis.sadd("presence:online_users", username)

        # Store user json details hash-set
        data = {
            "status": "online",
            "role": role,
            "last_seen": str(int(time.time())),
        }
        if room:
            data["room"] = room
        await self.redis.hset(f"presence:user:{username}", mapping=data)

        # Add to room set if provided
        if room:
            await self.redis.sadd(f"presence:room:{room}", username)

    # mark user as offline
    async def set_offline(self, username: str):

        # Remove from global set
        await self.redis.srem("presence:online_users", username)

        # Update hash (last_seen + status)
        await self.redis.hset(
            f"presence:user:{username}",
            mapping={
                "status": "offline",
                "last_seen": str(int(time.time())),
            }
        )

        # Remove from all room sets (we don't know which room, so scan)
        # For small demo it's fine. For big system you'd store user's rooms separately.
        async for key in self.redis.scan_iter("presence:room:*"):
            await self.redis.srem(key, username)

    async def move_to_room(self, username: str, new_room: str):
        """
        Mark user as being in a new room presence-wise.
        """
        # Update room field in user hash
        await self.redis.hset(f"presence:user:{username}", "room", new_room)
        # For simplicity, add to new room set (not removing from previous here)
        await self.redis.sadd(f"presence:room:{new_room}", username)

        
    async def get_online_users(self) -> List[str]:
        members = await self.redis.smembers("presence:online_users")
        # Redis returns bytes, convert to str
        return [m.decode("utf-8") for m in members]

    async def get_room_users(self, room: str) -> List[str]:
        members = await self.redis.smembers(f"presence:room:{room}")
        return [m.decode("utf-8") for m in members]

    async def get_user_presence(self, username: str) -> dict:
        data = await self.redis.hgetall(f"presence:user:{username}")
        return {k.decode("utf-8"): v.decode("utf-8") for k, v in data.items()}
