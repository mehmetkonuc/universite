import django_filters
from .models import ArticlesModel, Category
from apps.inputs.models import UniversitiesModel, CountriesModel, DepartmentsModel, StatusModel
from django import forms

class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Arama', help_text = 'Makale Başlıklarında Kelime Ara')
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Kategori',
        help_text ='Makalenin Kategorisi',
        empty_label='Tüm Kategoriler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )
    
    country = django_filters.ModelChoiceFilter(
        queryset=CountriesModel.objects.all(),
        field_name='user__educationalinformationmodel__Country',
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
        field_name='user__educationalinformationmodel__University',
        label='Üniversite',
        help_text ='Yazarın Üniversitesi',
        empty_label='Tüm Üniversiteler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )

    department = django_filters.ModelChoiceFilter(
        queryset=DepartmentsModel.objects.all(),
        field_name='user__educationalinformationmodel__Department',
        label='Bölüm',
        help_text ='Yazarın Bölümü',
        empty_label='Tüm Bölümler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )

    status = django_filters.ModelChoiceFilter(
        queryset=StatusModel.objects.all(),
        field_name='user__educationalinformationmodel__Status',
        label='Durum',
        help_text ='Yazarın Mezuniyet Durumu',
        empty_label='Tüm Durumlar',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
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
        model = ArticlesModel
        fields = ['sort_by', 'title', 'category', 'country', 'university', 'department', 'status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["sort_by"].field.widget.attrs = {
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',       
        }


class MyArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Arama', help_text = 'Makale Başlıklarında Kelime Ara')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Kategori', help_text ='Makalenin Kategorisi', empty_label='Tüm Kategoriler')
    
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
        model = ArticlesModel
        fields = ['sort_by', 'title', 'category']
