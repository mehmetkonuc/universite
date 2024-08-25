from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentsView.as_view(), name='documents'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('document/<slug:slug>', views.DocumentDetailsView.as_view(), name='document_details'),
    
    # path('document/<int:document_id>/view/', views.document_viewer, name='document_viewer'),
]
