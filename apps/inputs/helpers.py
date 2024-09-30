from django.core.cache import cache
from .models import CountriesModel, UniversitiesModel, DepartmentsModel, StatusModel, City

def get_cached_countries():
    countries = cache.get('countries')
    if not countries:
        countries = CountriesModel.objects.all()
        cache.set('countries', countries, timeout=60*60)
    return countries

def get_cached_universities():
    universities = cache.get('universities')
    if not universities:
        universities = UniversitiesModel.objects.all()
        cache.set('universities', universities, timeout=60*60)
    return universities

def get_cached_departments():
    departments = cache.get('departments')
    if not departments:
        departments = DepartmentsModel.objects.all()
        cache.set('departments', departments, timeout=60*60)
    return departments

def get_cached_statuses():
    statuses = cache.get('statuses')
    if not statuses:
        statuses = StatusModel.objects.all()
        cache.set('statuses', statuses, timeout=60*60)
    return statuses

def get_cached_cities():
    cities = cache.get('cities')
    if not cities:
        cities = City.objects.all()
        cache.set('cities', cities, timeout=60*60)
    return cities