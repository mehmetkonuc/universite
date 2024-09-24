
from django.urls import path, include
from . import views


urlpatterns = [
    path('photo/', views.profile_photo, name='profile_photo_upload'),
    path('settings/', views.ProfileSettingsView.as_view(), name='profile_settings'),
    path('upload_image/', views.PictureSettingsView.as_view(), name='upload_image'),
    path('settings/additional/', views.AdditionalInformationView.as_view(), name='additional_settings'),
    path('settings/privacy/', views.PrivacyView.as_view(), name='privacy_settings'),
    path('settings/education/', views.EducationSettingsView.as_view(), name='education_settings'),
    path('delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/posts/', views.PostsProfileView.as_view(), name='posts_profile'),
    path('<str:username>/articles/', views.ArticlesProfileView.as_view(), name='articles_profile'),
    path('<str:username>/marketplace/', views.MarketplaceProfileView.as_view(), name='marketplace_profile'),
    path('<str:username>/documents/', views.DocumentsProfileView.as_view(), name='documents_profile'),
    path('<str:username>/confessions/', views.ConfessionsProfileView.as_view(), name='confessions_profile'),
    path('<str:username>/questions/', views.QuestionsProfileView.as_view(), name='questions_profile'),
]
