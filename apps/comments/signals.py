from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from apps.post.models import PostsModel

@receiver(post_delete, sender=PostsModel)
def delete_related_comments(sender, instance, **kwargs):
    # İlgili ContentType'ı al
    content_type = ContentType.objects.get_for_model(instance)
    # Bu ContentType'a sahip tüm yorumları sil
    Comment.objects.filter(content_type=content_type, object_id=instance.id).delete()
