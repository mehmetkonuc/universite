from django import forms
from apps.marketplace.models import MarketPlaceModel
from apps.inputs.models import Currency

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

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),  # Currency modelinden tüm seçenekleri alır
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 100px;'}),
        required=True,
    )

    price = forms.DecimalField(
        max_digits=10,  # Toplamda en fazla 10 basamak
        decimal_places=2,  # Virgülden sonra 2 basamak
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fiyat'}),
        required=True,
    )
    class Meta:
        model = MarketPlaceModel
        fields =['title', 'description', 'currency', 'price', 'category', 'country', 'city', 'phone_number', 'is_published']