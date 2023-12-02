import json,os
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('Connected', event)
        await self.send({
            'type':'websocket.accept'
        })
    async def websocket_receive(self,event):
        print('Recieved', event)
        data = json.loads(event['text'])
        msg = data.get('message')
        response = {
            'message' : msg,
        }
        await self.send({
            'type':'websocket.send',
            'text': json.dumps(response)
        })
    async def websocket_disconnect(self,event):
        print('Disconnected', event)