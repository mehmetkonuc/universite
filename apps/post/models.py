from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from apps.likes.models import Like
from apps.comments.models import Comment
from apps.photos.models import PhotosModel
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


# Create your models here.
class PostsModel(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    Content = models.TextField(blank=True, null=True)
    PublishDate = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    photos = GenericRelation(PhotosModel)

    def total_likes(self):
        return self.likes.count()
    
    def user_has_liked(self, user):
        return self.likes.filter(user=user).exists()
        
    def __str__(self):
        return self.Content[:50]  # Özet gösterimi

    def get_notifications_comment_context(self):
        context = {
        'message' : 'gönderinize yorum yaptı.',
        'content_title' : self.Content,
        'content_url' : reverse('comment_detail', kwargs={'comment_id': self.id}),
        }
        return context

    def get_notifications_like_context(self):
        context = {
        'message' : 'gönderinizi beğendi.',
        'content_title' : self.Content,
        'content_url' : reverse('comment_detail', kwargs={'comment_id': self.id}),
        }
        return context

@receiver(post_delete, sender=PostsModel)
def delete_related_photos(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    PhotosModel.objects.filter(content_type=content_type, object_id=instance.id).delete()