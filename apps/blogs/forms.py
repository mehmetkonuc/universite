from django import forms
from apps.blogs.models import ArticlesModel
from django.core.exceptions import ValidationError

class ArticleAddForm(forms.ModelForm):
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
        model = ArticlesModel
        fields = ['title', 'content', 'category', 'futured_image', 'is_published']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }
        
        labels = {
            'title': 'Makale Başlığı',
            'content': 'Makale İçeriği',
            'category': 'Kategori',
            'futured_image': 'Öne Çıkan Görsel',

        }
        help_texts = {
            'title': 'Makale başlığını yazınız. 150 harften fazla olamaz.',
            'content': 'Makalenin ana içeriğini buraya yazın.',
            'category': 'Makalenize uygun kategoriyi seçiniz.',
            'futured_image': 'Makaleyi temsil eden bir resim yükleyin.',
        }

