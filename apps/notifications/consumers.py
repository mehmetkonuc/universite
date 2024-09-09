import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from django.template import Context, Template, loader
from django.template.loader import render_to_string

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f'user_{self.user.id}'

        # Kullanıcıya özel bir grup oluşturuyoruz
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Kullanıcı bağlantıyı keserse gruptan çıkarıyoruz
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Bildirim alındığında tetiklenecek fonksiyon
    async def send_notification(self, event):
        rendered_notification = render_to_string('partials/notifications.html', {'message': event['message']})

        # Bildirimi WebSocket üzerinden gönderiyoruz
        await self.send(text_data=json.dumps({
            'html': rendered_notification,
        }))
