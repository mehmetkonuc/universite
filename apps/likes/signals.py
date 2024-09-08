# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Like
# from django.contrib.contenttypes.models import ContentType
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from apps.blogs.models import ArticlesModel

# @receiver(post_save, sender=Like)
# def send_like_notification(sender, instance, created, **kwargs):
#     if created:
#         content_type = ContentType.objects.get_for_model(instance.content_object)
#         if content_type.model == 'articlesmodel':  # Beğenilen içerik bir makaleyse
#             article = instance.content_object
#             channel_layer = get_channel_layer()
#             notification_message = f'{instance.user.username} makalenizi beğendi.'
#             async_to_sync(channel_layer.group_send)(
#                 f'user_{article.user.id}',  # Bildirim gönderilecek makale sahibi
#                 {
#                     'type': 'send_notification',
#                     'message': notification_message
#                 }
#             )
