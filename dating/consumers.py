from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Chatting(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = "room" + str(self.scope['url_route']['kwargs']['room'])

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
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=event['message'])