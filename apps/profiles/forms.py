from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
import apps.profiles.models as models
import apps.inputs.models as inputsModel

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = models.ProfilePictureModel
        fields = ['profile_photo']

class ProfileEditForm(UserChangeForm):
    first_name = forms.CharField(label="Adınız", required=True)
    last_name = forms.CharField(label="Soyadınız", required=True)

    email = forms.EmailField(required=True)
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class EducationalInformationForm(forms.ModelForm):

    class Meta:
        model = models.EducationalInformationModel
        fields = ['country', 'university', 'department', 'status']


class PrivacyForm(forms.ModelForm):
    is_private = forms.BooleanField(label="Hesabı Gizle", help_text='Hesap gizliyken paylaşımlarınızı takipçileriniz dışında hiç kimse göremez.', required=False)

    class Meta:
        model = models.PrivacyModel
        fields = ['is_private']

class AdditionalInformationForm(forms.ModelForm):

    class Meta:
        model = models.AdditionalInformationModel
        fields = ['about']