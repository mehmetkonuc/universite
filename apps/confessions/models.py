from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from apps.comments.models import Comment
from apps.likes.models import Like
from apps.inputs.models import UniversitiesModel
from django.dispatch import receiver
from django.db.models.signals import pre_save
from apps.blogs.utils import slugify_tr


# Create your models here.
class ConfessionsModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    description = RichTextUploadingField()
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    create_at = models.DateTimeField(auto_now_add=True)
    university = models.ForeignKey(UniversitiesModel,
                        on_delete=models.CASCADE)
    is_privacy = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)

@receiver(pre_save, sender=ConfessionsModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)