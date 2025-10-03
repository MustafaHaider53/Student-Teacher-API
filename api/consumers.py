from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        # Reject if no user or anonymous
        if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.close(code=4001)
            return

        # Reject if role not allowed
        if not hasattr(user, "role") or user.role not in ["student", "teacher"]:
            await self.close(code=4003)
            return

        # ✅ Setup room
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Add this channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Only discard if room_group_name exists (connection was accepted)
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )


    async def receive(self, text_data):
        message = None

        try:
            # Try to parse JSON
            data = json.loads(text_data)
            message = data.get("message")
        except json.JSONDecodeError:
            # If not JSON, treat as plain text
            message = text_data

        if not message:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": getattr(self.scope["user"], "name", self.scope["user"].email),
            }
        )



    
    async def chat_message(self, event):
        """
        Called when someone sends a message to the group
        """
        await self.send(text_data=json.dumps({
            "user": event["user"],
            "message": event["message"]
        }))
