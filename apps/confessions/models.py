from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from apps.comments.models import Comment
from apps.likes.models import Like
from apps.inputs.models import UniversitiesModel, CountriesModel
from django.dispatch import receiver
from django.db.models.signals import pre_save
from apps.blogs.utils import slugify_tr
from django.urls import reverse


class UserConfessionsFilterModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.ForeignKey(CountriesModel, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey(UniversitiesModel, on_delete=models.SET_NULL, null=True, blank=True)
    sort_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s filter"


class ConfessionsModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    description = RichTextUploadingField()
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    create_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(CountriesModel,
                        on_delete=models.CASCADE)
    university = models.ForeignKey(UniversitiesModel,
                        on_delete=models.CASCADE)
    is_privacy = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=160, blank=True, editable=False)

    def get_notifications_comment_context(self):
        context = {
        'message' : 'itirafınıza yorum yaptı.',
        'content_title' : self.title,
        'content_url' : reverse('confession_details', kwargs={'slug': self.slug}),
        }
        return context

    def get_notifications_like_context(self):
        context = {
        'message' : 'itirafınızı beğendi.',
        'content_title' : self.title,
        'content_url' : reverse('confession_details', kwargs={'slug': self.slug}),
        }
        return context

@receiver(pre_save, sender=ConfessionsModel)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify_tr(instance.title)