from django import forms
from apps.confessions.models import ConfessionsModel, UserConfessionsFilterModel


class UserFilterForm(forms.ModelForm):
    class Meta:
        model=UserConfessionsFilterModel
        fields= ['country', 'university', 'sort_by' ]


class ConfessionsForm(forms.ModelForm):
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
        model = ConfessionsModel
        fields = ['title', 'description', 'country', 'university', 'is_privacy', 'is_published']
        widgets = {
            'university': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }

        labels = {
        'title': 'Başlık',
        'description': 'Açıklama',
        'university': 'Üniversite',
        'is_privacy': 'Gizle',
    }
        help_texts = {
        'title': 'İtirafınızı özetleyen başlık giriniz. 150 harften fazla olamaz.',
        'description': 'İtirafınızı yazın.',
        'university': 'Üniversite seçin.',
        'is_privacy': 'Gizli yayınlamak istiyorsanız seçiniz.',
    }