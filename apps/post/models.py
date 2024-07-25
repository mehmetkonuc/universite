from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from apps.likes.models import Like
from apps.comments.models import Comment


# Create your models here.
class PostsModel(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    Content = models.TextField(blank=True, null=True)  # Opsiyonel hale getirdik
    PublishDate = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    
    def total_likes(self):
        return self.likes.count()
    
    def user_has_liked(self, user):
        return self.likes.filter(user=user).exists()
    
    def __str__(self):
        return self.Content[:50]  # Özet gösterimi

class ImageModel(models.Model):
    Post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, related_name='images')
    Image = models.ImageField(upload_to='post_images/')
    UploadDate = models.DateTimeField(auto_now_add=True)

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # Kullanıcının aynı postu birden fazla beğenmesini engeller

    def __str__(self):
        return f"{self.user} liked {self.post}"