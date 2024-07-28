from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.MembersView.as_view(), name='members'),

]
