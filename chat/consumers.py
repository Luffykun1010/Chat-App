import json,os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")
import django
django.setup()
from django.contrib.auth.models import User
from .models import ChatMessage,Thread
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('Connected', event)
        user = self.scope['user']
        chatroom = f'user_chatroom_{user.username}'
        self.chatroom = chatroom
        await self.channel_layer.group_add(
            self.chatroom,
            self.channel_name
        )
        await self.send({
            'type':'websocket.accept'
        })
    async def websocket_receive(self,event):
        print('Recieved', event)
        data = json.loads(event['text'])
        msg = data.get('message')
        msgto = data.get('msgto')
        username = data.get('username')
        userid = data.get('uid')
        threadid = data.get('threadid')
        await self.save_message(threadid,username,msgto,msg)
        response = {
            'message' : msg,
            'msgto' : msgto,
            'username' : username,
            'threadid' : threadid
        }
        other_user_chatroom=f'user_chatroom_{msgto}'
        await self.channel_layer.group_send(
            other_user_chatroom,
            {
                'type':'chat_message',
                'text': json.dumps(response)
            }
        )
        await self.channel_layer.group_send(
            self.chatroom,
            {
                'type':'chat_message',
                'text': json.dumps(response)
            }
        )
    async def chat_message(self,event):
        print('Chat Message', event)
        await self.send({
            'type':'websocket.send',
            'text': event['text']
        })
    async def websocket_disconnect(self,event):
        print('Disconnected', event)
    @sync_to_async
    def save_message(self,threadid,user,msgto,msg):
        thread=Thread.objects.get(id=threadid)
        user=User.objects.get(username=user)
        recieved=User.objects.get(username=msgto)
        ChatMessage.objects.create(sended_by=user,sended_to=recieved,thread=thread,message=msg)
