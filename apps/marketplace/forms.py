from django import forms
from apps.marketplace.models import MarketPlaceModel

class MarketPlaceForm(forms.ModelForm):
    class Meta:
        model = MarketPlaceModel
        fields =['title', 'description', 'price', 'category', 'country', 'city', 'phone_number']