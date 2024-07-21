from django import forms
from . import models


class PostsForm(forms.ModelForm):

    class Meta:
        model = models.PostsModel
        fields = ['Content']