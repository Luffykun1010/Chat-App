import json,os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")
import django
django.setup()
from django.contrib.auth.models import User
from .models import Room,Messages

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print('Connected', event)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.send({
            'type':'websocket.accept'
        })
    async def websocket_receive(self,event):
        print('Recieved', event)
        data = json.loads(event['text'])
        msg = data.get('message')
        room = data.get('room')
        username = data.get('username')
        await self.save_message(username,room,msg)
        response = {
            'message' : msg,
            'room' : room,
            'username' : username
        }
        await self.send({
            'type':'websocket.send',
            'text': json.dumps(response)
        })
    async def websocket_disconnect(self,event):
        print('Disconnected', event)
    @sync_to_async
    def save_message(self,username,room,msg):
        user=User.objects.get(username=username)
        room=Room.objects.get(slug=room)
        Messages.objects.create(user=user,room=room,content=msg)
