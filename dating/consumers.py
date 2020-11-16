from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from django.db.models import F
from .helpers import jwt_encode, jwt_decode
from . import models


class Chatting(AsyncWebsocketConsumer):
    async def connect(self):
        q = parse_qs(self.scope['query_string'].decode())
        info = jwt_decode(q['token'][0])

        self.user = await sync_to_async(models.User.objects.get)(pk=info['user_id'])
        if not self.user.email_verified:
            await self.close()
            return
        self.room_id = str(self.scope['url_route']['kwargs']['room'])
        self.room = "room" + self.room_id

        await self.channel_layer.group_add(
            self.room,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = await sync_to_async(models.Message.objects.create)(
            room_id=self.room_id,
            user=self.user,
            content=data['content'])
        
        room = await sync_to_async(models.Room.objects.get)(pk=self.room_id)
        room.messages_count = F('messages_count') + 1
        await sync_to_async(room.save)()

        payload = {
            'message': {
                'id': message.id,
                'content': message.content,
                'user': {
                    'id': self.user.id,
                    "name": self.user.name,
                }
            }
        }

        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'chat_message',
                'payload': payload
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['payload']))
