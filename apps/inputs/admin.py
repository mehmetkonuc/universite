from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CountriesModel)
admin.site.register(models.UniversitiesModel)
admin.site.register(models.DepartmentsModel)
admin.site.register(models.StatusModel)
# admin.site.register(models.GrandeModel)

