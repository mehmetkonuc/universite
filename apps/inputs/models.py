from django.db import models

# Create your models here.
class CountriesModel(models.Model):
    Countries = models.CharField(max_length=255)
    
    def __str__(self):
        return self.Countries

class UniversitiesModel(models.Model):
    Countries = models.ForeignKey(CountriesModel, on_delete=models.CASCADE)
    Universities = models.CharField(max_length=255)
    
    def __str__(self):
        return self.Universities

class DepartmentsModel(models.Model):
    Universities = models.ManyToManyField(UniversitiesModel)
    Departments = models.CharField(max_length=255)

    def __str__(self):
        return self.Departments

class StatusModel(models.Model):
    Status = models.CharField(max_length=55)

    def __str__(self):
        return self.Status
    
# class GrandeModel(models.Model):
#     Grande = models.CharField(max_length=55)

#     def __str__(self):
#         return self.Grande