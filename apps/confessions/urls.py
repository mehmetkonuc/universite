from django.urls import path
from apps.confessions.views import ConfessionsAddView, ConfessionsView, ConfessionDetailView
urlpatterns = [
    path('', ConfessionsView.as_view(), name='confessions'),
    path('add/', ConfessionsAddView.as_view(), name='confessions_add'),
    path('confession/<slug:slug>', ConfessionDetailView.as_view(), name='confession_details'),
]