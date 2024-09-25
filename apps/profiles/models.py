from django.db import models
from django.conf import settings
import apps.inputs.models as inputs
from django.contrib.auth.models import User

# Create your models here.

class ProfilePictureModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_photo')
    profile_photo = models.ImageField(
        upload_to='profile_photos', blank=True, null=True)


class PrivacyModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='privacy')
    # is_private = models.BooleanField(default=False)  # Profil gizlilik ayarı
    is_private = models.BooleanField(default=False, db_index=True)
    message_privacy = models.CharField(max_length=20, default='everyone')  # Choices yok


class EducationalInformationModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='educational_information')
    country = models.ForeignKey(inputs.CountriesModel,
                             on_delete=models.CASCADE)
    university = models.ForeignKey(inputs.UniversitiesModel,
                             on_delete=models.CASCADE)
    department = models.ForeignKey(inputs.DepartmentsModel,
                             on_delete=models.CASCADE)
    status = models.ForeignKey(inputs.StatusModel,
                             on_delete=models.CASCADE)
    

class AdditionalInformationModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='additional_information')
    about = models.TextField()