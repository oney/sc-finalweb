from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from django.db.models import F
from .helpers import jwt_encode, jwt_decode
from . import models


class Chatting(AsyncWebsocketConsumer):
    '''
    AsyncWebsocketConsumer to handle websocket connections
    '''
    async def connect(self):
        '''
        Connect
        '''
        q = parse_qs(self.scope['query_string'].decode())
        info = jwt_decode(q['token'][0])  # decode JWT token
        user_id = info['user_id']  # get user id

        self.user = await sync_to_async(models.User.objects.get)(pk=user_id)
        # If the email is not verified, close the connection
        if not self.user.email_verified:
            await self.close()
            return
        self.room_id = str(self.scope['url_route']['kwargs']['room'])
        self.room = "room" + self.room_id

        # Add this connection to "self.room" group
        await self.channel_layer.group_add(
            self.room,
            self.channel_name
        )

        # Accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        '''
        Disconnect
        '''
        # Remove the connection from "self.room" group
        await self.channel_layer.group_discard(
            self.room,
            self.channel_name
        )

    async def receive(self, text_data):
        '''
        Receive a message from the client

        **Parameters**

            text_data: *str*
                Text data

        '''
        data = json.loads(text_data)  # deserialize JSON string
        # Crate a message instance
        message = await sync_to_async(models.Message.objects.create)(
            room_id=self.room_id,
            user=self.user,
            content=data['content'])

        room = await sync_to_async(models.Room.objects.get)(pk=self.room_id)
        # Increase messages_count of the room
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

        # Broadcast this message to all members of the group
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'chat_message',
                'payload': payload
            }
        )

    async def chat_message(self, event):
        '''
        Get a message from the broadcast

        **Parameters**

            event: *dict*
                Event

        '''
        # Send serialized JSON string to the client
        await self.send(text_data=json.dumps(event['payload']))
