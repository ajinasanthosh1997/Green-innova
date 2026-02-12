import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.message_id = self.scope['url_route']['kwargs']['message_id']
        self.room_group_name = f'chat_{self.message_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (we don't need client‑sent data for replies)
    async def receive(self, text_data):
        pass

    # Receive message from the channel layer (sent by admin)
    async def chat_reply(self, event):
        reply = event['reply']
        message_id = event['message_id']

        # Send reply to WebSocket
        await self.send(text_data=json.dumps({
            'reply': reply,
            'message_id': message_id
        }))