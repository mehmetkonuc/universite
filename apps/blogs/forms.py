from django import forms
from apps.blogs.models import ArticlesModel, UserFilterModel
from django.core.exceptions import ValidationError


class UserFilterForm(forms.ModelForm):
    order_by = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('likes', 'Beğeni Sayısına Göre'),
            ('comments', 'Yorum Sayısına Göre'),
            ('create_at', 'Yayım Tarihine Göre'),
        ],
        required=False,
        label='Sırala'
    )
    search_query = forms.CharField(
        required=False,
        label='Arama',
        widget=forms.TextInput(attrs={'placeholder': 'Başlık veya içerikte ara'})
    )

    class Meta:
        model = UserFilterModel
        fields = ['search_query', 'order_by', 'category', 'country', 'university', 'department', 'status']
        widgets = {
            'category': forms.Select(attrs={'class': 'selectpicker w-100', 'data-style': 'btn-default', 'data-live-search': 'true'}),
            'country': forms.Select(attrs={'class': 'selectpicker w-100', 'data-style': 'btn-default', 'data-live-search': 'true'}),
            'university': forms.Select(attrs={'class': 'selectpicker w-100', 'data-style': 'btn-default', 'data-live-search': 'true'}),
            'department': forms.Select(attrs={'class': 'selectpicker w-100', 'data-style': 'btn-default', 'data-live-search': 'true'}),
            'status': forms.Select(attrs={'class': 'selectpicker w-100', 'data-style': 'btn-default', 'data-live-search': 'true'}),
        }
        labels = {
            'category': 'Kategori',
            'country': 'Yazarın Ülkesi',
            'university': 'Yazarın Üniversitesi',
            'department': 'Yazarın Bölümü',
            'status': 'Yazarın Durumu',
        }

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

