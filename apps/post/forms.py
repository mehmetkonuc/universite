from django import forms
from . import models


class PostsForm(forms.ModelForm):

    class Meta:
        model = models.PostsModel
        fields = ['Content']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Content'].required = False  # Content alanını opsiyonel hale getirdik