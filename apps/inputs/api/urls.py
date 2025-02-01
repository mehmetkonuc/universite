from django.urls import path
from .views import (
    CountryListView, UniversityListView, DepartmentListView, StatusListView,
)

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='countries'),
    path('universities/', UniversityListView.as_view(), name='universities'),
    path('departments/', DepartmentListView.as_view(), name='departments'),
    path('statuses/', StatusListView.as_view(), name='statuses'),
]