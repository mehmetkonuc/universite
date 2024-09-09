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
import apps.inputs.models as inputs
from django.urls import reverse

# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class UserQuestionsFilterModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(inputs.CountriesModel, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey(inputs.UniversitiesModel, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(inputs.DepartmentsModel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(inputs.StatusModel, on_delete=models.SET_NULL, null=True, blank=True)
    sort_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s filter"


class QuestionsModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    content = RichTextUploadingField()
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    create_at = models.DateTimeField(auto_now_add=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)

    def __str__(self):
        return self.title

    def get_notifications_comment_context(self):
        context = {
        'message' : 'sorunuza cevap verdi.',
        'content_title' : self.title,
        'content_url' : reverse('question_details', kwargs={'slug': self.slug}),
        }
        return context

    def get_notifications_like_context(self):
        context = {
        'message' : 'sorunuzu beğendi.',
        'content_title' : self.title,
        'content_url' : reverse('question_details', kwargs={'slug': self.slug}),
        }
        return context

@receiver(pre_save, sender=QuestionsModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)