from django.urls import path
from .views import file_complaint, view_complaints

urlpatterns = [
    path('file-complaint/<str:app_label>/<str:model>/<int:object_id>/', file_complaint, name='file_complaint'),
    path('view-complaints/', view_complaints, name='view_complaints'),
]
