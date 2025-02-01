from rest_framework import serializers
from apps.profiles.models import EducationalInformationModel
from django.contrib.auth.models import User
from apps.profiles.models import ProfilePictureModel

class UserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_photo']

    def get_profile_photo(self, obj):
        request = self.context.get('request')
        if request and obj.profile_photo:
            return request.build_absolute_uri(obj.profile_photo.profile_photo.url)
        return None

# Eğitim bilgileri için serializer
class EducationalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalInformationModel
        fields = '__all__'
