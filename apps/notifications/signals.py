from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail  # Örnek olarak e-posta gönderimi için kullanılabilir
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.comments.models import Comment
from apps.likes.models import Like
from apps.notifications.models import Notification

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        # İçeriğin sahibinin yorumu yapan kullanıcı olup olmadığını kontrol et
        if instance.content_object.user != instance.user:
            content_type = ContentType.objects.get_for_model(instance.content_object)
            notification_message = ' makalenize yorum yaptı.'
            content_url = instance.content_object.get_absolute_url()
            notification = Notification.objects.create(
                user=instance.content_object.user,  # Makale sahibi
                action_user=instance.user,  # Yorumu yapan kişi
                message=notification_message,
                content_type=content_type,
                object_id=instance.content_object.id,  # Makale ID'si
                action_object_id=instance.id  # Yoruma ait ID
            )
            
            # WebSocket bildirimi gönderiyoruz
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{instance.content_object.user.id}',  # Bildirim alıcısı
                {
                    'type': 'send_notification',
                    'message': notification_message,
                    'action_user_name': instance.user.username,
                    'action_user': instance.user.first_name + ' ' + instance.user.last_name,
                    'profile_photo_url': notification.action_user.profilepicturemodel.profile_photo.url if notification.action_user.profilepicturemodel.profile_photo else '/static/assets/img/avatars/1.png',
                    'content_title': instance.content_object.title,
                    'content_url': content_url,  # İçerik URL'si eklendi
                    'notification_id': notification.id,
                    'is_read': notification.is_read,
                    'created_at': notification.created_at.strftime("%d %b %Y, %H:%M")
                }
            )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        # İçeriğin sahibinin beğeniyi yapan kullanıcı olup olmadığını kontrol et
        if instance.content_object.user != instance.user:
            content_type = ContentType.objects.get_for_model(instance.content_object)
            notification_message = ' makalenizi beğendi.'
            content_url = instance.content_object.get_absolute_url()
            # Notification kaydına action_user alanı ekliyoruz
            notification = Notification.objects.create(
                user=instance.content_object.user,  # Makale sahibi
                action_user=instance.user,  # Beğeniyi yapan kişi
                message=notification_message,
                content_type=content_type,
                object_id=instance.content_object.id,  # Makale ID'si
                action_object_id=instance.id  # Beğeniye ait ID
            )
            # WebSocket bildirimi gönderiyoruz
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{instance.content_object.user.id}',  # Bildirim alıcısı makale sahibi
                {
                    'type': 'send_notification',
                    'message': notification_message,
                    'action_user_name': instance.user.username,
                    'action_user': instance.user.first_name + ' ' + instance.user.last_name,
                    'profile_photo_url': notification.action_user.profilepicturemodel.profile_photo.url if notification.action_user.profilepicturemodel.profile_photo else '/static/assets/img/avatars/1.png',
                    'content_title': instance.content_object.title ,
                    'content_url': content_url,  # İçerik URL'si eklendi
                    'notification_id': notification.id,
                    'is_read': notification.is_read,
                    'created_at': notification.created_at.strftime("%d %b %Y, %H:%M")
                }
            )

# Yorum silindiğinde bildirimi silmek
@receiver(post_delete, sender=Comment)
def delete_comment_notification(sender, instance, **kwargs):
    Notification.objects.filter(
        content_type=ContentType.objects.get_for_model(instance.content_object),
        object_id=instance.content_object.id,  # Makale ID'si
        action_object_id=instance.id,  # Yoruma ait ID
        action_user=instance.user  # Yorumu yapan kişi
    ).delete()

# Beğeni geri çekildiğinde bildirimi silmek
@receiver(post_delete, sender=Like)
def delete_like_notification(sender, instance, **kwargs):
    Notification.objects.filter(
        content_type=ContentType.objects.get_for_model(instance.content_object),
        object_id=instance.content_object.id,  # Makale ID'si
        action_object_id=instance.id,  # Beğeniye ait ID
        action_user=instance.user  # Beğeniyi yapan kişi
    ).delete()


