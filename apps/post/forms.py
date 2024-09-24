from django import forms
from . import models


class PostsForm(forms.ModelForm):
    class Meta:
        model = models.PostsModel
        fields = ['content']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False  # Content alanını opsiyonel hale getirdik


class FilterForm(forms.ModelForm):
    class Meta:
        model=models.PostsFilterModel
        fields= ['following_only', 'country', 'university', 'department', 'status']