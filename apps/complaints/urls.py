# complaints/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:app_name>/<str:model_name>/<int:object_id>/', views.create_complaint, name='create_complaint'),
    path('admin/', views.complaint_dashboard, name='complaint_dashboard'),
    path('admin/update/<int:pk>/', views.update_complaint_status, name='update_complaint_status'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('delete/<int:pk>/', views.delete_complaint, name='delete_complaint'),

]