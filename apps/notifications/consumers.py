import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
        # HTML formatındaki mesajı hazırlıyoruz
        message = f"""
            <li class="list-group-item list-group-item-action dropdown-notifications-item">
              <div class="d-flex">
                <div class="flex-shrink-0 me-3">
                <a href="/profile/{event['action_user_name']}/">
                  <div class="avatar">
                    <img src="{event['profile_photo_url'] or '/static/assets/img/avatars/1.png'}" alt class="rounded-circle" />
                  </div>
                  </a>
                </div>
                <div class="flex-grow-1">
                <a href="/profile/{event['action_user_name']}/">
                  <h6 class="small mb-1">{event['action_user']}<small class="text-muted"> {event['message']}</small></h6>
                  </a>
                  <a href="{event['content_url']}">
                 <h6 class="mb-1 d-block text-body">{event['content_title']}</h6>
                  </a>
                  <small class="text-muted">{event['created_at']}</small>
                </div>
                <div class="flex-shrink-0 dropdown-notifications-actions">
                  <a href="javascript:void(0)" class="dropdown-notifications-read"
                    ><span class="badge badge-dot" id="badge-notifications"></span
                  ></a>
                </div>
              </div>
            </li>
        """

        # Bildirimi WebSocket üzerinden gönderiyoruz
        await self.send(text_data=json.dumps({
            'html': message,
        }))
