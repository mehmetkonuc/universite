from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from apps.photos.models import PhotosModel
from apps.inputs.models import CountriesModel, City, Currency
from django.dispatch import receiver
from django.db.models.signals import pre_save
from apps.blogs.utils import slugify_tr

# Create your models here.
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
    futured_image = GenericRelation(PhotosModel)
    description = RichTextUploadingField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(CountriesModel, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)

@receiver(pre_save, sender=MarketPlaceModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)

