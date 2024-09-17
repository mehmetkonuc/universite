import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from django.template import Context, Template, loader
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async
from apps.chat.models import Chat, Message
from django.contrib.auth.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.notification_group = f"notifications_{self.user.id}"
        self.chat_group = f"chat_{self.user.id}"
        self.follower_group = f"follower_{self.user.id}"

        # Bildirimler kanalına abone et
        await self.channel_layer.group_add(self.notification_group, self.channel_name)
        await self.channel_layer.group_add(self.chat_group, self.channel_name)
        await self.channel_layer.group_add(self.follower_group, self.channel_name)
        
        await self.accept()


    async def receive(self, text_data):
        data = json.loads(text_data)
        data_type = data.get('type')

        if data_type == "chat_message":
            chat_id = data['chat_id']
            sender_id = data['sender_id']
            message = data['message']

            chat = await sync_to_async(Chat.objects.get)(id=chat_id)
            if int(sender_id) == int(chat.first_user_id):
                receiver_id = chat.second_user_id
            else:
                receiver_id = chat.first_user_id

            # Mesajı veritabanına kaydet
            messages = await sync_to_async(Message.objects.create)(
                chat=chat,
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=message
            )

            profile_photo = messages.sender.profilepicturemodel.profile_photo.url
            sender_name = messages.sender.first_name + ' ' + messages.sender.last_name
            university = str(messages.sender.educationalinformationmodel.University)

            # Mesajı alıcıya gönder
            recipient_group_name = f'chat_{receiver_id}'
            await self.channel_layer.group_send(
                recipient_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'chat_id' :chat_id,
                    'sender_id': sender_id,
                    'sender_profile_photo':profile_photo,
                    'sender_name':sender_name,
                    'sender_university':university,
                }
            )


    async def disconnect(self, close_code):
        # Kullanıcı bağlantıyı keserse her iki gruptan da çıkarıyoruz
        await self.channel_layer.group_discard(self.notification_group, self.channel_name)
        await self.channel_layer.group_discard(self.chat_group, self.channel_name)


    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_profile_photo = event['sender_profile_photo']
        sender_name = event['sender_name']
        sender_university = event['sender_university']
        chat_id = event['chat_id']
        type = 'chat_message'
        # Mesajı WebSocket üzerinden gönder
        await self.send(text_data=json.dumps({
            'type': type,
            'message': message,
            'sender_id': sender_id,
            'sender_profile_photo': sender_profile_photo,
            'sender_name': sender_name,
            'sender_university': sender_university,
            'chat_id': chat_id,
        }))


    # Bildirim alındığında tetiklenecek fonksiyon
    async def send_notification(self, event):
        rendered_notification = render_to_string('notifications/header_notifications.html', {'message': event['message']})
        # Bildirimi WebSocket üzerinden gönderiyoruz
        await self.send(text_data=json.dumps({
            'type': 'send_notification',
            'html': rendered_notification,
        }))

    # Bildirim alındığında tetiklenecek fonksiyon
    async def message_notification(self, event):
        rendered_notification = render_to_string('notifications/header_messages.html', {'message': event['message']})
        # Bildirimi WebSocket üzerinden gönderiyoruz
        await self.send(text_data=json.dumps({
            'type': 'message_notification',
            'html': rendered_notification,
        }))
    

        # Bildirim alındığında tetiklenecek fonksiyon
    async def follower_notification(self, event):
        rendered_notification = render_to_string('notifications/header_follow.html', {'message': event['message']})
        # Bildirimi WebSocket üzerinden gönderiyoruz
        await self.send(text_data=json.dumps({
            'type': 'follower_notification',
            'html': rendered_notification,
        }))