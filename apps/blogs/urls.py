from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ArticlesView.as_view(), name='articles'),
    path('article/add', views.ArticleAddView.as_view(), name='article_add'),
    path('article/<slug:slug>', views.ArticlesDetailsView.as_view(), name='article_details'),
    path('article/edit/<slug:slug>', views.ArticleEditView.as_view(), name='article_edit'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
]
