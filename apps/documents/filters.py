import django_filters
from .models import DocumentsModel
from django import forms
from apps.follow.models import Follow
from django.db.models import Q
from apps.inputs.helpers import get_cached_countries, get_cached_universities, get_cached_departments, get_cached_statuses


class UserFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Arama', help_text = 'Makale Başlıklarında Kelime Ara')

    # Takip edilen kullanıcıların paylaşımlarını filtrelemek için ChoiceField
    following_only = django_filters.ChoiceFilter(
        choices=[
            ('following', 'Sadece Takip Ettiklerim')
        ],
        method='filter_following_choice',
        label='Gösterim Seçeneği',
        empty_label='Herkes',
        widget=forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
        })
    )

    country = django_filters.ModelChoiceFilter(
        queryset=get_cached_countries(),
        field_name='user__educational_information__country',
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
        queryset = get_cached_universities(),
        field_name='user__educational_information__university',
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
        queryset=get_cached_departments(),
        field_name='user__educational_information__department',
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
        queryset=get_cached_statuses(),
        field_name='user__educational_information__status',
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
        model = DocumentsModel
        fields = ['sort_by', 'following_only', 'title', 'country', 'university', 'department', 'status']
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.filters["sort_by"].field.widget.attrs = {
    #         'class': 'selectpicker w-100',
    #         'data-style': 'btn-default',       
    #     }

    def filter_following_choice(self, queryset, name, value):
        if value == 'following':
            # Kullanıcının takip ettiği kişilerin ve kendisinin makaleleri filtreleniyor
            following_users = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
            return queryset.filter(user__in=list(following_users) + [self.request.user])
        return queryset  # Eğer 'all' seçiliyse, tüm makaleleri getir

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        # Her zaman gizlilik kontrolünü çalıştırmak için
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.filters["sort_by"].field.widget.attrs = {
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',       
        }
        if request and hasattr(request, 'user'):
            # Takip edilen kullanıcıları filtrele
            following_users = Follow.objects.filter(follower=request.user).select_related('following').values_list('following', flat=True)
            
            # Profil gizli değil veya privacy kaydı yoksa (isnull) kullanıcıları göster
            self.queryset = self.queryset.filter(
                Q(user__privacy__is_private=False) | 
                Q(user__privacy__isnull=True) |  # privacy kaydı olmayan kullanıcılar
                Q(user__in=list(following_users) + [request.user])
            )


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
        model = DocumentsModel
        fields = ['sort_by', 'title']
