from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (CustomTokenObtainPairSerializer, UserCreateSerializer)
from rest_framework import status
from apps.profiles.api.serializers import (EducationalInformationSerializer)
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupStep1(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_data = request.data.get('user')
        if not user_data:
            return Response({'detail': 'Kullanıcı bilgileri gerekli.'}, status=status.HTTP_400_BAD_REQUEST)

        # E-posta kontrolü
        email = user_data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Bu e-posta adresi zaten kullanımda.'}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserCreateSerializer(data=user_data)
        if user_serializer.is_valid():
            # Veriler geçerli, session içinde saklanıyor
            request.session['user_data'] = user_serializer.validated_data
            return Response({'message': 'Kullanıcı bilgileri doğrulandı ve saklandı.'}, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupStep2(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Session içindeki kullanıcı verilerini alıyoruz
        user_data = request.session.get('user_data')
        if not user_data:
            return Response({'detail': 'Kullanıcı bilgileri mevcut değil.'}, status=status.HTTP_400_BAD_REQUEST)

        # Eğitim bilgilerini request'den alıyoruz
        education_data = request.data.get('education')
        if not education_data:
            return Response({'detail': 'Eğitim bilgileri gerekli.'}, status=status.HTTP_400_BAD_REQUEST)

        # Kullanıcı oluşturma
        user_serializer = UserCreateSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Eğitim bilgileri oluşturma
        education_data['user'] = user.id
        education_serializer = EducationalInformationSerializer(data=education_data)
        if education_serializer.is_valid():
            education_serializer.save()
        else:
            return Response(education_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Kullanıcı ve eğitim bilgileri başarıyla kaydedildi.'}, status=status.HTTP_201_CREATED)


# Kullanıcı ve Eğitim Bilgileri Oluşturmak için View
class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_data = request.data.get('user')
        education_data = request.data.get('education')

        # Kullanıcı oluşturma işlemleri
        user_serializer = UserCreateSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Eğitim bilgileri oluşturma işlemleri
        education_data['user'] = user.id
        education_serializer = EducationalInformationSerializer(data=education_data)
        if education_serializer.is_valid():
            education_serializer.save()
        else:
            return Response(education_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Kayıt başarılı'}, status=status.HTTP_201_CREATED)

