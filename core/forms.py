from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.profiles import models as ProfilesModel


class RegisterForm(UserCreationForm):
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
        model = ProfilesModel.EducationalInformationModel
        fields = ['Country', 'University', 'Department', 'Status']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı Adı veya E-Posta Adresi")