from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ArticlesView.as_view(), name='articles'),
    path('article/add', views.ArticleAddView.as_view(), name='article_add'),
    path('article/<int:article_id>', views.ArticlesDetailsView.as_view(), name='article_details'),
]
