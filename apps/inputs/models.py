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

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(CountriesModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.country.Countries}"


class Currency(models.Model):
    name = models.CharField(max_length=100)
# class GrandeModel(models.Model):
#     Grande = models.CharField(max_length=55)

#     def __str__(self):
#         return self.Grande