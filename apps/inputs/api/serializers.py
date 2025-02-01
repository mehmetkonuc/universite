from rest_framework import serializers
from apps.inputs.models import CountriesModel, UniversitiesModel, DepartmentsModel, StatusModel

# Ülke bilgileri için serializer
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountriesModel
        fields = '__all__'

# Üniversite bilgileri için serializer
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversitiesModel
        fields = '__all__'

# Bölüm bilgileri için serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentsModel
        fields = '__all__'

# Mezuniyet durumu bilgileri için serializer
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusModel
        fields = '__all__'