from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from apps.likes.models import Likes
from apps.comments.models import Comment
from apps.photos.models import PhotosModel
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from apps.inputs import models as inputs
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.files.storage import default_storage

# Create your models here.
# Create your models here.
def upload_to(instance, filename):
    return f'posts/{now().year}/{now().month}/{filename}'


class PostsPhotos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_photos')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=PostsPhotos)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        if default_storage.exists(instance.image.name):
            default_storage.delete(instance.image.name)

class PostsModel(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Likes)
    photos = GenericRelation(PostsPhotos)

    def total_likes(self):
        return self.likes.count()
    
    def user_has_liked(self, user):
        return self.likes.filter(user=user).exists()
        
    def __str__(self):
        return self.content[:50]  # Özet gösterimi

    def get_notifications_comment_context(self):
        context = {
        'message' : 'gönderinize yorum yaptı.',
        'content_title' : self.content,
        'content_url' : reverse('comment_detail', kwargs={'comment_id': self.id}),
        }
        return context

    def get_notifications_like_context(self):
        context = {
        'message' : 'gönderinizi beğendi.',
        'content_title' : self.content[:50],
        'content_url' : reverse('post_detail', kwargs={'post_id': self.id}),
        }
        return context

@receiver(post_delete, sender=PostsModel)
def delete_related_photos(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    PhotosModel.objects.filter(content_type=content_type, object_id=instance.id).delete()


class PostsFilterModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='posts_filter')
    following_only = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(inputs.CountriesModel, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey(inputs.UniversitiesModel, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(inputs.DepartmentsModel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(inputs.StatusModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s filter"