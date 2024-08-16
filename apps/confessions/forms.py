from django import forms
from apps.confessions.models import ConfessionsModel

class ConfessionsForm(forms.ModelForm):
    class Meta:
        model = ConfessionsModel
        fields = ['title', 'description', 'university', 'is_privacy']
        widgets = {
            'university': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }