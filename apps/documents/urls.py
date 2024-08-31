from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentsView.as_view(), name='documents'),
    path('my-documents/', views.MyDocumentsView.as_view(), name='my_documents'),
    path('add/', views.DocumentsAddView.as_view(), name='documents_add'),
    path('edit/<slug:slug>/', views.DocumentsEditView.as_view(), name='documents_edit'),
    path('<slug:slug>/', views.DocumentDetailsView.as_view(), name='document_details'),
    path('folder/create/', views.create_folder, name='create_folder'),
    path('delete/<int:docuements_id>/', views.delete_documents, name='documents_delete'),
    
    # path('document/<int:document_id>/view/', views.document_viewer, name='document_viewer'),
]
