from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from apps.profiles.models import ProfilePictureModel, EducationalInformationModel
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı Adı veya E-Posta Adresi")


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Adınız", required=True)
    last_name = forms.CharField(label="Soyadınız", required=True)

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', "username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kullanımda.")
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EducationalInformationForm(forms.ModelForm):
    
    class Meta:
        model = EducationalInformationModel
        fields = ['country', 'university', 'department', 'status']

        labels = {
            'country': 'Ülke',
            'university' : 'Üniversite',
            'department' : 'Bölüm',
            'status' : 'Mezuniyet Durumu',

        }

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePictureModel
        fields = ['profile_photo']