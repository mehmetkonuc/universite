from django import forms
from . import models

class ArticleAddForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=models.Category.objects.all(), widget=forms.Select(attrs={
        'class': 'selectpicker w-100',
        'data-style': 'btn-default',
        'data-live-search': 'true'
    }))
    class Meta:
        model = models.ArticlesModel
        fields = ['title', 'content', 'category']