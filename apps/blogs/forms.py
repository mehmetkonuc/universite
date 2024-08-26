from django import forms
from apps.blogs.models import ArticlesModel
from django.core.exceptions import ValidationError

class ArticleAddForm(forms.ModelForm):

    class Meta:
        model = ArticlesModel
        fields = ['title', 'content', 'category', 'futured_image']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }

