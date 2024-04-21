from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
import profiles.models as models

class ProfileEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class EducationalInformationForm(forms.ModelForm):
    
    class Meta:
        model = models.EducationalInformationModel
        fields = ['Country', 'University', 'Department', 'Status']