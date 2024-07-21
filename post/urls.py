from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.PostView.as_view(), name='post'),
    path('delete/<int:PostID>/', views.DeletePost, name='DeletePost'),

]
