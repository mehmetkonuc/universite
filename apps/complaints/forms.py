from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'placeholder': 'Şikayet nedeninizi buraya yazın...', 'rows': 5}),
        }
