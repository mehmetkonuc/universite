from django import forms
from apps.questions import models


class UserFilterForm(forms.ModelForm):
    class Meta:
        model=models.UserQuestionsFilterModel
        fields= ['following_only', 'category', 'country', 'university', 'department', 'status', 'sort_by' ]
        labels = {
            'category': 'Kategori',
        } 


class QuestionsAddForm(forms.ModelForm):
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
        model = models.QuestionsModel
        fields = ['title', 'content', 'category', 'is_published']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }

        labels = {
        'title': 'Başlık',
        'content': 'Soru',
        'category': 'Kategori',
    }
        help_texts = {
        'title': 'Sorunuzu özetleyen başlık yazın.',
        'content': 'Sorunuzu yazın.',
        'category': 'Katego seçin.',
    }