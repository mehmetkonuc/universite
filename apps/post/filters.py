import django_filters
from .models import PostsModel
from apps.inputs.models import UniversitiesModel, CountriesModel, DepartmentsModel, StatusModel
from django import forms
from apps.follow.models import Follow
from django.db.models import Q

class Filter(django_filters.FilterSet):

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
        queryset=CountriesModel.objects.all(),
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
        queryset=UniversitiesModel.objects.all(),
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
        queryset=DepartmentsModel.objects.all(),
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
        queryset=StatusModel.objects.all(),
        field_name='user__educational_information__status',
        label='Durum',
        help_text ='Yazarın Mezuniyet Durumu',
        empty_label='Tüm Durumlar',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
        }),
    )
  
    class Meta:
        model = PostsModel
        fields = ['following_only', 'country', 'university', 'department', 'status']

    def filter_following_choice(self, queryset, name, value):
        if value == 'following':
            # Takip edilen kullanıcılar ve kendisi
            # following_users = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
            following_users = Follow.objects.filter(follower=self.request.user).select_related('following').values_list('following', flat=True)

            queryset = queryset.filter(user__in=list(following_users) + [self.request.user])
        
        return queryset
    
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        # Her zaman gizlilik kontrolünü çalıştırmak için
        super().__init__(data, queryset, request=request, prefix=prefix)
        if request and hasattr(request, 'user'):
            # Takip edilen kullanıcıları filtrele
            following_users = Follow.objects.filter(follower=request.user).select_related('following').values_list('following', flat=True)
            
            # Profil gizli değil veya privacy kaydı yoksa (isnull) kullanıcıları göster
            self.queryset = self.queryset.filter(
                Q(user__privacy__is_private=False) | 
                Q(user__privacy__isnull=True) |  # privacy kaydı olmayan kullanıcılar
                Q(user__in=list(following_users) + [request.user])
            )
