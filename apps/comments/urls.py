from django.urls import path, include
from . import views


urlpatterns = [
    path('delete/<int:comment_id>/', views.CommentView.delete_comment, name='delete_comment'),
    path('details/<int:comment_id>/', views.CommentCommentsView.as_view(), name='comment_detail'),

]
