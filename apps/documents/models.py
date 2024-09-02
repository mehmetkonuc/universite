from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from apps.blogs.utils import slugify_tr
from ckeditor_uploader.fields import RichTextUploadingField
from apps.comments.models import Comment
from apps.likes.models import Like
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.storage import default_storage


# Create your models here.
def upload_to(instance, filename):
    return f'documents/{now().year}/{now().month}/{filename}'


class DocumentsUploadModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    document = models.FileField(upload_to=upload_to)
    document_name = models.CharField(max_length=255, editable=False)  # Yeni alan

    def save(self, *args, **kwargs):
        if not self.document_name:
            self.document_name = self.document.name.split('/')[-1]
        super().save(*args, **kwargs)
        
        
@receiver(post_delete, sender=DocumentsUploadModel)
def delete_documents_file(sender, instance, **kwargs):
    if instance.document:
        if default_storage.exists(instance.document.name):
            default_storage.delete(instance.document.name)


class DocumentsFolderModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    
    def __str__(self):
        return self.name

class DocumentsModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    folder = models.ForeignKey(DocumentsFolderModel,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    documents = GenericRelation(DocumentsUploadModel)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)
    is_published = models.BooleanField(default=False)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Doküman"
        verbose_name_plural = "Dokümanlar"
        
@receiver(pre_save, sender=DocumentsModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)