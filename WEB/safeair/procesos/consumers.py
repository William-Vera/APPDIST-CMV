import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChartConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept() 

    async def receive(self, text_data):
        data = json.loads(text_data)