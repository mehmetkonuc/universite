from django.db import models
from django.conf import settings

# Create your models here.
class PostsModel(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    Content = models.TextField()
    PublishDate = models.DateTimeField(auto_now_add=True)

class ImageModel(models.Model):
    Post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, related_name='images')
    Image = models.ImageField(upload_to='post_images/')
    UploadDate = models.DateTimeField(auto_now_add=True)