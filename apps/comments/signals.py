# from apps.post.models import PostsModel
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Comment
# from django.contrib.contenttypes.models import ContentType
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from apps.blogs.models import ArticlesModel
# from apps.post.models import PostsModel



# @receiver(post_delete, sender=PostsModel)
# def delete_related_comments(sender, instance, **kwargs):
#     # İlgili ContentType'ı al
#     content_type = ContentType.objects.get_for_model(instance)
#     # Bu ContentType'a sahip tüm yorumları sil
#     Comment.objects.filter(content_type=content_type, object_id=instance.id).delete()

# @receiver(post_save, sender=Comment)
# def send_comment_notification(sender, instance, created, **kwargs):
#     if created:
#         content_type = ContentType.objects.get_for_model(instance.content_object)
#         if content_type.model == 'articlesmodel':  # Yorum yapılan içerik bir makaleyse
#             article = instance.content_object
#             channel_layer = get_channel_layer()
#             notification_message = f'{instance.user.username} makalenize yorum yaptı.'
#             async_to_sync(channel_layer.group_send)(
#                 f'user_{article.user.id}',  # Bildirim gönderilecek makale sahibi
#                 {
#                     'type': 'send_notification',
#                     'message': notification_message
#                 }
#             )