from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path('notifications/mark-all-as-read/', views.notifications_mark_all_as_read, name='notifications_mark_all_as_read'),
    path('notifications/delete/', views.notifications_requests_delete, name='notifications_requests_delete'),

]
