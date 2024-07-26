from django import forms
from .models import PhotosModel

class PhotosForm(forms.ModelForm):
    class Meta:
        model = PhotosModel
        fields = ['photo']