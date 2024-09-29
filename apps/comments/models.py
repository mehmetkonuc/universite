from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from apps.likes.models import Likes
from apps.photos.models import PhotosModel
from django.urls import reverse
from django.utils.timezone import now
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


def upload_to(instance, filename):
    return f'comments/{now().year}/{now().month}/{filename}'


class CommentPhotos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_photos')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=CommentPhotos)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        if default_storage.exists(instance.image.name):
            default_storage.delete(instance.image.name)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(max_length=360)
    likes = GenericRelation(Likes)
    photos = GenericRelation(CommentPhotos)
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f'Comment by {self.user} on {self.content_object}'
    
    def is_parent(self):
        return self.parent is None

    def get_replies(self):
        return self.replies.all()

    def get_notifications_comment_context(self):
        context = {
        'message' : 'yorumunuza yorum yaptı.',
        'content_title' : self.text,
        'content_url' : reverse('comment_detail', kwargs={'comment_id': self.id}),
        }
        return context

    def get_notifications_like_context(self):
        context = {
        'message' : 'yorumunuzu beğendi.',
        'content_title' : self.text,
        'content_url' : reverse('comment_detail', kwargs={'comment_id': self.id}),
        }
        return context