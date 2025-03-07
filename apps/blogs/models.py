from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from apps.comments.models import Comment
from apps.likes.models import Likes
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from apps.blogs.utils import slugify_tr
from django.core.files.storage import default_storage
from django.utils.timezone import now
import apps.inputs.models as inputs
from django.urls import reverse

# Create your models here.
def upload_to(instance, filename):
    return f'blogs/{now().year}/{now().month}/{filename}'


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class UserFilterModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs_filter')
    title = models.CharField(max_length=255, blank=True, null=True)
    following_only = models.CharField(max_length=255, blank=True, null=True)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(inputs.CountriesModel, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey(inputs.UniversitiesModel, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(inputs.DepartmentsModel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(inputs.StatusModel, on_delete=models.SET_NULL, null=True, blank=True)
    sort_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s filter"


class ArticlesModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=155)
    content = RichTextUploadingField()
    futured_image = models.ImageField(upload_to=upload_to)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Likes)
    create_at = models.DateTimeField(auto_now_add=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)

    def get_absolute_url(self):
        return reverse('article_details', kwargs={'slug': self.slug}) 
    
    def get_notifications_comment_context(self):
        context = {
        'message' : 'makalenize yorum yaptı.',
        'content_title' : self.title,
        'content_url' : reverse('article_details', kwargs={'slug': self.slug}),
        }
        return context

    def get_notifications_like_context(self):
        context = {
        'message' : 'makalenizi beğendi.',
        'content_title' : self.title,
        'content_url' : reverse('article_details', kwargs={'slug': self.slug}),
        }
        return context

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-create_at']

@receiver(pre_save, sender=ArticlesModel)
def handle_article_pre_save(sender, instance, **kwargs):
    # Slug oluşturma
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)

    # Eski resmi silme
    if instance.pk:
        try:
            old_instance = ArticlesModel.objects.get(pk=instance.pk)
        except ArticlesModel.DoesNotExist:
            old_instance = None

        if old_instance:
            old_image = old_instance.futured_image
            if old_image and old_image != instance.futured_image:
                if default_storage.exists(old_image.name):
                    default_storage.delete(old_image.name)


@receiver(post_delete, sender=ArticlesModel)
def delete_photo_file(sender, instance, **kwargs):
    if instance.futured_image:
        if default_storage.exists(instance.futured_image.name):
            default_storage.delete(instance.futured_image.name)