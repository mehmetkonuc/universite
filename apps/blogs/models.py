from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from apps.photos.models import PhotosModel
from apps.comments.models import Comment
from apps.likes.models import Like
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.blogs.utils import slugify_tr

# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class ArticlesModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    content = RichTextUploadingField()
    futured_image = GenericRelation(PhotosModel)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    create_at = models.DateTimeField(auto_now_add=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=ArticlesModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)