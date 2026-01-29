from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ReviewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope["url_route"]["kwargs"]["product_id"]
        self.group_name = f"reviews_{self.product_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def review_created(self, event):
        await self.send(text_data=json.dumps(event["data"]))
