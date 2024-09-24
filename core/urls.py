"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root' : settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root' : settings.STATIC_ROOT}),
    path('', include('apps.visitor.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #UYGULAMALARIM
    path('profile/', include('apps.profiles.urls')),
    path('post/', include('apps.post.urls')),
    path('comments/', include('apps.comments.urls')),
    path('members/', include('apps.members.urls')),
    path('blogs/', include('apps.blogs.urls')),
    path('likes/', include('apps.likes.urls')),
    path('marketplace/', include('apps.marketplace.urls')),
    path('confessions/', include('apps.confessions.urls')),
    path('questions/', include('apps.questions.urls')),
    path('documents/', include('apps.documents.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('chat/', include('apps.chat.urls')),
    path('follow/', include('apps.follow.urls')),
]
