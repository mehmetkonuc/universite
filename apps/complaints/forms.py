# complaints/forms.py
from django import forms
from .models import Complaint
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'description']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Şikayet Kategorisi Seçiniz'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Şikayet detaylarınızı açıklayınız (maks. 1000 karakter)'
            }),
        }
        labels = {
            'category': 'Kategori',
            'description': 'Açıklama'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.content_object = kwargs.pop('content_object', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # Tekrar şikayet kontrolü
        if self.user and self.content_object:
            content_type = ContentType.objects.get_for_model(self.content_object)
            if Complaint.objects.filter(
                user=self.user,
                content_type=content_type,
                object_id=self.content_object.id
            ).exists():
                raise ValidationError("Bu içerik için daha önce şikayette bulundunuz.")
        return cleaned_data