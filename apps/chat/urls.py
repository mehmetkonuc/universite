from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="chat_index"),
    path('get-messages/', views.get_messages, name='get_messages'),

    path('<int:chat_id>', views.chat, name="chat"),
    path('send-message/', views.send_message, name="send_message"),

    path('start/<int:second_user_id>', views.start_chat, name="start_chat"),
]
