from rest_framework import generics
from .serializers import (
    CountrySerializer, UniversitySerializer, DepartmentSerializer, StatusSerializer,
)
from apps.inputs.models import CountriesModel, UniversitiesModel, DepartmentsModel, StatusModel
from rest_framework.permissions import AllowAny

# Ülke verilerini almak için View
class CountryListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = CountriesModel.objects.all()
    serializer_class = CountrySerializer

# Üniversite verilerini almak için View
class UniversityListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = UniversitiesModel.objects.all()
    serializer_class = UniversitySerializer

# Bölüm verilerini almak için View
class DepartmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = DepartmentsModel.objects.all()
    serializer_class = DepartmentSerializer

# Mezuniyet durumu verilerini almak için View
class StatusListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = StatusModel.objects.all()
    serializer_class = StatusSerializer