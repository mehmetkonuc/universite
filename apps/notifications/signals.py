from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.comments.models import Comment
from apps.likes.models import Likes
from apps.notifications.models import Notification
from apps.chat.models import Message
from apps.follow.models import FollowRequest


#Takipleşme Bildirimleri
@receiver(post_save, sender=FollowRequest)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        follower = instance.follower
        following = instance.following

        #Takip Edilmek İstenen Kullanıcının Gizlilik Kontrolü
        is_private = following.privacy.is_private

        #Takip Etmek İsteyeninin Profil Fotoğraf Kontrolü
        try:
            profile_photo_url= follower.profile_photo.profile_photo.url
        except:
            profile_photo_url = None


        # Takip edilen kullanıcıya bildirim göndermek için gerekli veriler
        context = {
            'following_is_private' : is_private,
            'follower_user_id': follower.id,
            'follower_user_username': follower.username,
            'follower_user_first_name': follower.first_name,
            'follower_user_last_name': follower.last_name,
            'follower_user_university': str(follower.educational_information.university) if hasattr(follower, 'educational_information') else 'Bilinmiyor',
            'time': instance.created_at.strftime("%d %b %Y, %H:%M"),
            'profile_photo_url': profile_photo_url,
            'request_id' : instance.id,
        }

        # Bildirim gönderme
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'follower_{following.id}',  # Bildirim alıcısı (takip edilen kullanıcı)
            {
                'type': 'follower_notification',
                'message': context,
            }
        )


#Mesajlaşma Bildirimleri
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    try:
        profile_photo_url= instance.sender.profile_photo.profile_photo.url
    except:
        profile_photo_url = None

    context = Message.get_notifications_message_context(instance)
    context.update({
        'chat_id' : instance.chat.id,
        'sender_user_id': instance.sender.id,
        'sender_user_first_name': instance.sender.first_name,
        'sender_user_last_name' : instance.sender.last_name,
        'sender_user_university': str(instance.sender.educational_information.university),
        'last_message': instance.content,
        'time': instance.timestamp.strftime("%d %b %Y, %H:%M"),
        'profile_photo_url': profile_photo_url,
        })
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{instance.receiver.id}',  # Bildirim alıcısı
        {
            'type': 'message_notification',
            'message': context,
        }
    )

# Yorumlar Bildirimi
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    # Kullanıcıları ve bildirimleri göndermek için genel bir fonksiyon
    def send_notification(recipient, context):
        # Bildirimi oluştur
        notification = Notification.objects.create(
            user=recipient,
            action_user=instance.user,
            notification_type='comment',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )

        # Kullanıcı profili fotoğrafını al
        try:
            profile_photo_url = instance.user.profile_photo.profile_photo.url
        except AttributeError:
            profile_photo_url = None

        # Bildirim bağlamını güncelle
        context.update({
            'action_user_name': instance.user.username,
            'action_user_first_name': instance.user.first_name,
            'action_user_last_name': instance.user.last_name,
            'action_user_university': str(instance.user.educational_information.university),
            'profile_photo_url': profile_photo_url,
            'notification_id': notification.id,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime("%d %b %Y, %H:%M"),
        })

        # WebSocket bildirimi gönder
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{recipient.id}',
            {
                'type': 'send_notification',
                'message': context
            }
        )

    # Yorumun alt yorum olup olmadığını kontrol et ve uygun bildirimi gönder
    if created and instance.parent and instance.parent.user != instance.user:
        context = instance.get_notifications_comment_context()
        context['action_object_id'] = instance.parent.id
        send_notification(instance.parent.user, context)

    # Yorumun, içeriğin sahibine ait olup olmadığını kontrol et
    content_owner = instance.content_object.user
    if created and content_owner != instance.user:
        # Alt yorumların içeriğin sahibine bildirilmesini engelle
        try:
            is_parent = instance.parent.user
        except AttributeError:
            is_parent = None

        if is_parent != content_owner:
            context = instance.content_object.get_notifications_comment_context()
            comment_context = instance.get_notifications_comment_context()
            context['comment_title'] = comment_context['content_title']
            context['comment_url'] = comment_context['content_url']
            # context.update(instance.content_object.get_notifications_comment_context())  # İki bağlamı birleştir
            context['action_object_id'] = instance.content_object.id
            send_notification(content_owner, context)


@receiver(post_save, sender=Likes)
def create_like_notification(sender, instance, created, **kwargs):
    # İçeriğin sahibinin beğeniyi yapan kullanıcı olup olmadığını kontrol et
    if created and instance.content_object.user != instance.user:
        content_type = ContentType.objects.get_for_model(instance.content_object)
        context = instance.content_object.get_notifications_like_context()

        notification = Notification.objects.create(
            user=instance.content_object.user,  # Makale sahibi
            action_user=instance.user,  # Beğeniyi yapan kişi
            notification_type='like',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,  # Makale ID'si
        )

        # Profil Fotoğraf Kontrolü 
        try:
            profile_photo = notification.action_user.profile_photo.profile_photo.url
        except:
            profile_photo = None

        context.update({
            'action_user_name': instance.user.username,
            'action_user_first_name': instance.user.first_name,
            'action_user_last_name': instance.user.last_name,
            'action_user_university': str(instance.user.educational_information.university),
            'profile_photo_url': profile_photo,
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
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,  # Makale ID'si
        # action_object_id=instance.id,  # Yoruma ait ID
        # action_user=instance.user  # Yorumu yapan kişi
    ).delete()


# Beğeni geri çekildiğinde bildirimi silmek
@receiver(post_delete, sender=Likes)
def delete_like_notification(sender, instance, **kwargs):
    print('girdi')
    Notification.objects.filter(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,  # Makale ID'si
        # action_object_id=instance.id,  # Beğeniye ait ID
        # action_user=instance.user  # Beğeniyi yapan kişi
    ).delete()


