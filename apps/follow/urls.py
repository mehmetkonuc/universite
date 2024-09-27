from django.urls import path
from . import views

urlpatterns = [
    path('toggle-follow/', views.toggle_follow, name='toggle_follow'),
    path('requests/', views.follow_requests_view, name='follow-requests'),
    path('follow-requestsaction/', views.follow_requests_action, name='follow_requests_action'),
    path('follow_requests_delete/', views.follow_requests_delete, name='follow_requests_delete'),
    path('followers/mark-all-as-read/', views.followers_mark_all_as_read, name='followers_mark_all_as_read'),
]