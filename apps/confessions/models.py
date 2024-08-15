from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from apps.comments.models import Comment
from apps.likes.models import Like

# Create your models here.
class ConfessionsModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    description = RichTextUploadingField()
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    create_at = models.DateTimeField(auto_now_add=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)