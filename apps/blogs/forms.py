from django import forms
from . import models

class ArticleAddForm(forms.ModelForm):
    class Meta:
        model = models.ArticlesModel
        fields = ['title', 'content']