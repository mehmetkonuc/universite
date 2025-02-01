from django.urls import path
from .views import PostsApiView

urlpatterns = [
    path('posts/', PostsApiView.as_view(), name='posts_api'),
]
