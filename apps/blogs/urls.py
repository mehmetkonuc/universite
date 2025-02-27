from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ArticlesView.as_view(), name='articles'),
    path('empty/', views.EmptyView.as_view(), name='empty'),

    path('my/', views.MyArticlesView.as_view(), name='my_articles'),
    path('draft/', views.DraftArticlesView.as_view(), name='my_draft_articles'),
    path('add/', views.ArticleAddView.as_view(), name='article_add'),
    path('<slug:slug>/', views.ArticlesDetailsView.as_view(), name='article_details'),
    path('edit/<slug:slug>/', views.ArticleEditView.as_view(), name='article_edit'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
]
