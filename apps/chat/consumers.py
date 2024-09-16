from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_group_name = f'chat_user_{self.user.id}'

        # Kullanıcıyı bir gruba ekle
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Kullanıcıyı gruptan çıkar
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat_id = data['chat_id']
        sender_id = data['sender_id']
        message = data['message']

        chat = await sync_to_async(Chat.objects.get)(id=chat_id)
        if int(sender_id) == int(chat.first_user_id):
            receiver_id = chat.second_user_id
        else:
            receiver_id = chat.first_user_id

        # Mesajı veritabanına kaydet
        await sync_to_async(Message.objects.create)(
            chat=chat,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=message
        )

    #     # Mesajı alıcıya gönder
    #     recipient_group_name = f'chat_user_{receiver_id}'
    #     await self.channel_layer.group_send(
    #         recipient_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message,
    #             'sender_id': sender_id,
    #         }
    #     )

    # async def chat_message(self, event):
    #     message = event['message']
    #     sender_id = event['sender_id']
    #     # Mesajı WebSocket üzerinden gönder
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'sender_id': sender_id
    #     }))
