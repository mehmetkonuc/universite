from django.db import models
from django.conf import settings
# from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from apps.inputs.models import CountriesModel, City, Currency
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from apps.blogs.utils import slugify_tr
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.storage import default_storage
from django.utils.timezone import now
from ckeditor.fields import RichTextField
# Create your models here.
def upload_to(instance, filename):
    return f'marketplace/{now().year}/{now().month}/{filename}'


class MarketPlaceImagesModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=MarketPlaceImagesModel)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        if default_storage.exists(instance.image.name):
            default_storage.delete(instance.image.name)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class MarketPlaceModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    images = GenericRelation(MarketPlaceImagesModel)
    description = RichTextField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(CountriesModel, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)

@receiver(pre_save, sender=MarketPlaceModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)