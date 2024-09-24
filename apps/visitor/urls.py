
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from apps.post.views import PostView


urlpatterns = [
    path('', PostView.as_view(), name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_step1, name='register'),
    path('register/step/2', views.register_step2, name='register_step2'),
    path('register/photo', views.profile_photo, name='profile_photo'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.CustomPasswordResetView.as_view(
        template_name='visitor/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='visitor/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='visitor/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='visitor/password_reset_complete.html'), name='password_reset_complete'),
]
