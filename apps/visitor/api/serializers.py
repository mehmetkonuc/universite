from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = 'username_or_email'

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        # Kullanıcı adı veya e-posta kontrolü
        try:
            user = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
        except User.DoesNotExist:
            raise serializers.ValidationError('Giriş bilgileri geçersizdir.')

        # Kullanıcıyı authenticate et
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError('Giriş bilgileri geçersizdir.')

        # Eğer kullanıcı başarılı bir şekilde authenticate edildiyse
        refresh = self.get_token(user)
        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data



# Kullanıcı oluşturmak için serializer
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu e-posta adresi zaten kullanımda.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
