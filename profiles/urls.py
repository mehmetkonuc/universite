
from django.urls import path, include
from . import views


urlpatterns = [
    path('settings/', views.ProfileSettingsView.as_view(), name='profileSettings'),
    path('delete/', views.ProfileDeleteView.as_view(), name='profileDelete'),
]
