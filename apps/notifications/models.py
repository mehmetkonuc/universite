from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Makale sahibi
    action_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='action_user', on_delete=models.CASCADE)  # Beğenen/Yorum yapan
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    action_object_id = models.PositiveIntegerField()  # Yorum veya Beğeni ID'sini tutar

    def __str__(self):
        return self.message
