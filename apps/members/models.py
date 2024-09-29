from django.db import models
from django.contrib.auth.models import User
import apps.inputs.models as inputs


# Create your models here.
class MembersFilterModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='members_filter')
    country = models.ForeignKey(inputs.CountriesModel, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey(inputs.UniversitiesModel, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(inputs.DepartmentsModel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(inputs.StatusModel, on_delete=models.SET_NULL, null=True, blank=True)