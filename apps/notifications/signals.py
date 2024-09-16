from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.comments.models import Comment
from apps.likes.models import Like
from apps.notifications.models import Notification
from apps.chat.models import Message


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    context = Message.get_notifications_message_context(instance)
    context.update({
        'sender_user_id': instance.sender.id,
        'sender_user': instance.sender.first_name + ' ' + instance.sender.last_name,
        'sender_user_university': str(instance.sender.educationalinformationmodel.University),
        'time': instance.timestamp.strftime("%d %b %Y, %H:%M"),
        'profile_photo_url': instance.sender.profilepicturemodel.profile_photo.url if instance.sender.profilepicturemodel.profile_photo else '/static/assets/img/avatars/1.png',
        })
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{instance.receiver.id}',  # Bildirim alıcısı
        {
            'type': 'message_notification',
            'message': context,
        }
    )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    # İçeriğin sahibinin yorumu yapan kullanıcı olup olmadığını kontrol et
    if created and instance.content_object.user != instance.user:
        content_type = ContentType.objects.get_for_model(instance.content_object)
        context = instance.content_object.get_notifications_comment_context()
        notification = Notification.objects.create(
            user=instance.content_object.user,  # Makale sahibi
            action_user=instance.user,  # Yorumu yapan kişi
            message=context['message'],
            content_type=content_type,
            object_id=instance.content_object.id,  # Makale ID'si
            action_object_id=instance.id  # Yoruma ait ID
        )

        context.update({
            'action_user_name': instance.user.username,
            'action_user': instance.user.first_name + ' ' + instance.user.last_name,
            'profile_photo_url': notification.action_user.profilepicturemodel.profile_photo.url if notification.action_user.profilepicturemodel.profile_photo else '/static/assets/img/avatars/1.png',
            'notification_id': notification.id,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime("%d %b %Y, %H:%M"),
        })
        
        # WebSocket bildirimi gönderiyoruz
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.content_object.user.id}',  # Bildirim alıcısı
            {
                'type': 'send_notification',
                'message': context
            }
        )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    # İçeriğin sahibinin beğeniyi yapan kullanıcı olup olmadığını kontrol et
    if created and instance.content_object.user != instance.user:
        content_type = ContentType.objects.get_for_model(instance.content_object)
        context = instance.content_object.get_notifications_like_context()
        notification = Notification.objects.create(
            user=instance.content_object.user,  # Makale sahibi
            action_user=instance.user,  # Beğeniyi yapan kişi
            message=context['message'],
            content_type=content_type,
            object_id=instance.content_object.id,  # Makale ID'si
            action_object_id=instance.id  # Beğeniye ait ID
        )

        context.update({
            'action_user_name': instance.user.username,
            'action_user': instance.user.first_name + ' ' + instance.user.last_name,
            'profile_photo_url': notification.action_user.profilepicturemodel.profile_photo.url if notification.action_user.profilepicturemodel.profile_photo else '/static/assets/img/avatars/1.png',
            'notification_id': notification.id,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime("%d %b %Y, %H:%M"),
        })
        # WebSocket bildirimi gönderiyoruz
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{instance.content_object.user.id}',  # Bildirim alıcısı makale sahibi
            {
                'type': 'send_notification',
                'message': context,
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


