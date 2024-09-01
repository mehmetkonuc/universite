from django.urls import path
from apps.documents import views

urlpatterns = [
    path('', views.DocumentsView.as_view(), name='documents'),
    path('my/', views.MyDocumentsView.as_view(), name='my_documents'),
    path('draft/', views.MyDraftDocumentsView.as_view(), name='my_draft_documents'),
    path('my/folders/', views.MyFoldersView.as_view(), name='my_folders'),
    path('my/folder/details/<int:folder>/', views.MyFoldersDetailsView.as_view(), name='my_folder_details'),
    path('my/folder/add/', views.FolderAddView.as_view(), name='folder_add'),
    path('my/folder/edit/<int:folder_id>/', views.FolderEditView.as_view(), name='folder_edit'),
    path('add/', views.DocumentsAddView.as_view(), name='documents_add'),
    path('edit/<slug:slug>/', views.DocumentsEditView.as_view(), name='documents_edit'),
    path('folder/create/', views.create_folder, name='create_folder'),
    path('delete/<int:docuements_id>/', views.delete_documents, name='documents_delete'),
    path('delete/folder/<int:folder_id>/', views.delete_folder, name='folder_delete'),
    path('<slug:slug>/', views.DocumentDetailsView.as_view(), name='document_details'),
]

