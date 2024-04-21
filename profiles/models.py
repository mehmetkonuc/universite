from django.db import models
from django.conf import settings
import inputs.models as inputs

# Create your models here.
class EducationalInformationModel(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    Country = models.ForeignKey(inputs.CountriesModel,
                             on_delete=models.CASCADE)
    University = models.ForeignKey(inputs.UniversitiesModel,
                             on_delete=models.CASCADE)
    Department = models.ForeignKey(inputs.DepartmentsModel,
                             on_delete=models.CASCADE)
    Status = models.ForeignKey(inputs.StatusModel,
                             on_delete=models.CASCADE)
    # Grande = models.ForeignKey(inputs.GrandeModel,
    #                          on_delete=models.CASCADE)