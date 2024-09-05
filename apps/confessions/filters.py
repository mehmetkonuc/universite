import django_filters
from .models import ConfessionsModel
from apps.inputs.models import UniversitiesModel, CountriesModel 
from django import forms

class UserFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Arama', help_text = 'Makale Başlıklarında Kelime Ara')

    country = django_filters.ModelChoiceFilter(
        queryset=CountriesModel.objects.all(),
        label='Ülke',
        help_text ='Yazarın Ülkesi',
        empty_label='Tüm Ülkeler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )
    university = django_filters.ModelChoiceFilter(
        queryset=UniversitiesModel.objects.all(),
        label='Üniversite',
        help_text ='Yazarın Üniversitesi',
        empty_label='Tüm Üniversiteler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )

    # Define custom ordering choices
    sort_by = django_filters.OrderingFilter(
        choices=[
            ('-create_at', 'Yeniye Göre'),
            ('create_at', 'Eskiden Yeniye Göre'),
            ('-like_count', 'Beğeni Sayısına Göre'),
            ('like_count', 'Beğeni Sayısına Göre (Artan)'),
            ('-comment_count', 'Yorum Sayısına Göre'),
            ('comment_count', 'Yorum Sayısına Göre (Artan)')
        ],
        label='Sıralama',
        help_text ='Makalelerin Sıralamasını Seçin',
        empty_label='Varsayılan Sıralama',
        widget=forms.Select
    )
    
    class Meta:
        model = ConfessionsModel
        fields = ['sort_by', 'title', 'country', 'university']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["sort_by"].field.widget.attrs = {
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',       
        }


class MyFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Arama', help_text = 'Makale Başlıklarında Kelime Ara')
    
    # Define custom ordering choices
    sort_by = django_filters.OrderingFilter(
        choices=[
            ('-create_at', 'Yeniye Göre'),
            ('create_at', 'Eskiden Yeniye Göre'),
            ('-like_count', 'Beğeni Sayısına Göre'),
            ('like_count', 'Beğeni Sayısına Göre (Artan)'),
            ('-comment_count', 'Yorum Sayısına Göre'),
            ('comment_count', 'Yorum Sayısına Göre (Artan)')
        ],
        label='Sıralama',
        help_text ='Makalelerin Sıralamasını Seçin',
        empty_label='Varsayılan Sıralama'
    )
    
    class Meta:
        model = ConfessionsModel
        fields = ['sort_by', 'title']
