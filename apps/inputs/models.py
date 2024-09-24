from django.db import models

# Create your models here.
class CountriesModel(models.Model):
    countries = models.CharField(max_length=255)
    
    def __str__(self):
        return self.countries

class UniversitiesModel(models.Model):
    countries = models.ForeignKey(CountriesModel, on_delete=models.CASCADE)
    universities = models.CharField(max_length=255)
    
    def __str__(self):
        return self.universities

class DepartmentsModel(models.Model):
    universities = models.ManyToManyField(UniversitiesModel)
    departments = models.CharField(max_length=255)

    def __str__(self):
        return self.departments

class StatusModel(models.Model):
    status = models.CharField(max_length=55)

    def __str__(self):
        return self.status

class City(models.Model):
    country = models.ForeignKey(CountriesModel, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.country.countries}"


class Currency(models.Model):
    currency = models.CharField(max_length=100)


    def __str__(self):
        return self.currency