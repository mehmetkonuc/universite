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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='privacy', db_index=True)
    is_private = models.BooleanField(default=False, db_index=True)
    message_privacy = models.CharField(max_length=20, default='everyone')  # Choices yok


class EducationalInformationModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='educational_information', db_index=True)
    country = models.ForeignKey(inputs.CountriesModel,
                             on_delete=models.CASCADE, db_index=True)
    university = models.ForeignKey(inputs.UniversitiesModel,
                             on_delete=models.CASCADE, db_index=True)
    department = models.ForeignKey(inputs.DepartmentsModel,
                             on_delete=models.CASCADE, db_index=True)
    status = models.ForeignKey(inputs.StatusModel,
                             on_delete=models.CASCADE, db_index=True)
    

class AdditionalInformationModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='additional_information', db_index=True)
    living_country = models.ForeignKey(inputs.CountriesModel,
                             on_delete=models.CASCADE, related_name='living_country', blank=True, null=True, db_index=True)
    living_city = models.ForeignKey(inputs.City,
                             on_delete=models.CASCADE, related_name='living_city', blank=True, null=True, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField(max_length=360, blank=True, null=True)