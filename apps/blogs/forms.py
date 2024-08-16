from django import forms
from . import models

class ArticleAddForm(forms.ModelForm):

    class Meta:
        model = models.ArticlesModel
        fields = ['title', 'content', 'category']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }