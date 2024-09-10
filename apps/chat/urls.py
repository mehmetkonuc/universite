from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:chat_id>/', views.chat_view, name='chat_view'),
    path('start_chat/<int:user_id>/', views.start_chat, name='start_chat'),
    path('chats/', views.chat_list, name='chat_list'),
    path('users/', views.user_list, name='user_list'),
]
