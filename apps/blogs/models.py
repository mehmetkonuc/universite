from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from apps.photos.models import PhotosModel

# Create your models here.
class ArticlesModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    content = RichTextUploadingField()
    futured_image = GenericRelation(PhotosModel)
    create_at = models.DateTimeField(auto_now_add=True)
