from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
import profiles.models as models
import inputs.models as inputsModel

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = models.ProfilePictureModel
        fields = ['profile_photo']

class ProfileEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class EducationalInformationForm(forms.ModelForm):

    class Meta:
        model = models.EducationalInformationModel
        fields = ['Country', 'University', 'Department', 'Status']

class AdditionalInformationForm(forms.ModelForm):

    class Meta:
        model = models.AdditionalInformationModel
        fields = ['About']