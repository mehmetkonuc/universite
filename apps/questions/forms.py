from django import forms
from apps.questions import models

class QuestionsAddForm(forms.ModelForm):

    class Meta:
        model = models.QuestionsModel
        fields = ['title', 'content', 'category']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }