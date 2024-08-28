from django import forms
from apps.marketplace.models import MarketPlaceModel

class MarketPlaceForm(forms.ModelForm):
    STATUS_CHOICES = [
        (False, 'Taslaklara Kaydet'),
        (True, 'Yayınla'),
    ]

    is_published = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
            }),
        required=True,
        help_text='Makalenin yayımlanmasını mı yoksa taslak olarak mı kaydedileceğini seçin.',
        initial = True,
        label = 'Yayınlama Durumu',
    )
    class Meta:
        model = MarketPlaceModel
        fields =['title', 'description', 'price', 'category', 'country', 'city', 'phone_number', 'is_published']