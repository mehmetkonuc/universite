from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import post_delete


class PhotosModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    photo = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=PhotosModel)
def delete_photo_file(sender, instance, **kwargs):
    if instance.photo:
        if default_storage.exists(instance.photo.name):
            default_storage.delete(instance.photo.name)