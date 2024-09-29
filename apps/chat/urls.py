from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="chat_index"),
    path('get-messages/', views.get_messages, name='get_messages'),
    path('get-older-messages/', views.get_older_messages, name='get_older_messages'),
    path('<int:chat_id>/', views.chat, name="chat"),
    path('send-message/', views.send_message, name="send_message"),
    path('start/<str:username>', views.start_chat, name="start_chat"),
    path('messages/mark-all-as-read/', views.messages_mark_all_as_read, name='messages_mark_all_as_read'),
    path('delete/<int:chat_id>/', views.delete_chat, name='delete_chat'),

]
