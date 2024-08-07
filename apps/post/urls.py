from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.PostView.as_view(), name='post'),
    path('delete/<int:PostID>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('details/<int:post_id>/', views.PostDetails.as_view(), name='post_detail'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
]
