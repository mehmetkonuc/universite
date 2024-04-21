
from django.urls import path, include
from . import views


urlpatterns = [
    path('settings/', views.ProfileSettingsView.as_view(), name='profileSettings'),
    path('settings/education/', views.EducationSettingsView.as_view(), name='EducationSettings'),
    path('delete/', views.ProfileDeleteView.as_view(), name='profileDelete'),
    path('', views.ProfileView.as_view(), name='profile'),
]
