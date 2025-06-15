import json 
from channels.generic.websocket import AsyncWebsocketConsumer 


class MessageViewSet(AsyncWebsocketConsumer):
    async def connect(self):
        self.target_username = self.scope['url_route']['kwargs']['username']
        self.room_name       = f'message_{self.target_username}' 
        

        await super().connect()