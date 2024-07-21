from django.db import models
from django.conf import settings

# Create your models here.
class PostsModel(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    Content = models.TextField()
    PublishDate = models.DateTimeField(auto_now_add=True)