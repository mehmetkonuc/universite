import django_filters
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from apps.inputs.helpers import get_cached_countries, get_cached_universities, get_cached_departments, get_cached_statuses


class MemberFilter(django_filters.FilterSet):

    name_or_username = django_filters.CharFilter(
        method='filter_by_name_or_username',
        label='Ad, Soyad veya Kullanıcı Adı',
        help_text='Ad, soyad veya kullanıcı adı içinde arama yap'
    )

    country = django_filters.ModelChoiceFilter(
        queryset = get_cached_countries(),
        field_name='educational_information__country',
        label='Ülke',
        help_text ='Üyenin Ülkesi',
        empty_label='Tüm Ülkeler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )

    university = django_filters.ModelChoiceFilter(
        queryset = get_cached_universities(),
        field_name='educational_information__university',
        label='Üniversite',
        help_text ='Üyenin Üniversitesi',
        empty_label='Tüm Üniversiteler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )

    department = django_filters.ModelChoiceFilter(
        queryset = get_cached_departments(),
        field_name='educational_information__department',
        label='Bölüm',
        help_text ='Üyenin Bölümü',
        empty_label='Tüm Bölümler',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )

    status = django_filters.ModelChoiceFilter(
        queryset = get_cached_statuses(),
        field_name='educational_information__status',
        label='Durum',
        help_text ='Üyenin Mezuniyet Durumu',
        empty_label='Tüm Durumlar',
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
        }),
    )

    class Meta:
        model = User
        fields = ['name_or_username', 'country', 'university', 'department', 'status']

    def filter_by_name_or_username(self, queryset, name, value):
        terms = value.split()
        
        if len(terms) == 2:
            first_term, second_term = terms
            query = (
                Q(first_name__icontains=first_term, last_name__icontains=second_term) |
                Q(first_name__icontains=second_term, last_name__icontains=first_term) |
                Q(username__icontains=value)
            )
        else:
            # Eğer iki terim yoksa, tüm olasılıkları değerlendir
            query = Q()
            for term in terms:
                query |= Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(username__icontains=term)
        
        return queryset.filter(query)