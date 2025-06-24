from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache

class UserStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_storage = cache.get("online_users", set())
        user_storage.add(f"user_{self.scope['user'].pk}")
        cache.set("online_user", user_storage)
        cache.set(f"user_{self.scope['user'].pk}", "online", timeout = 30)
        await self.accept()
    
    async def receive(self, text_data: str):
        data = json.loads(text_data)
        print("Pinged")
        if data['request'] == 'ping':
            user_storage = cache.get("online_users", set())
            user_storage.add(f"user_{self.scope['user'].pk}")
            cache.set("online_user", user_storage)
            cache.set(f"user_{self.scope['user'].pk}", "online", timeout = 30)
            await self.send(json.dumps({"request": "success"}))

    async def disconnect(self, code):
        user_storage = cache.get("online_users", set())
        user_storage.discard(f"user_{self.scope['user'].pk}")
        cache.set("online_user", user_storage)
        cache.delete(f"user_{self.scope['user'].pk}")
        return await super().disconnect(code)