from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver
from django.db.models.signals import pre_save
from apps.blogs.utils import slugify_tr
from ckeditor_uploader.fields import RichTextUploadingField
from apps.comments.models import Comment
from apps.likes.models import Like
from django.contrib.contenttypes.fields import GenericRelation

class FolderModel(MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

@receiver(pre_save, sender=FolderModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.name)


class DocumentsModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    folder = TreeForeignKey(FolderModel, null=True, blank=True, on_delete=models.CASCADE, related_name='documents')
    content = RichTextUploadingField()
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    
    def __str__(self):
        return self.title

@receiver(pre_save, sender=DocumentsModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)