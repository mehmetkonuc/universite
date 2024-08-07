from django.urls import path
from .views import like_object

urlpatterns = [
    path('like/', like_object, name='like_object'),
]