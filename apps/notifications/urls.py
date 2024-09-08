from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path('delete_notifications/', views.delete_notifications, name='delete_notifications'),
    path('mark_notifications_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('notifications/mark-all-as-read/', views.notifications_mark_all_as_read, name='notifications_mark_all_as_read'),

]
