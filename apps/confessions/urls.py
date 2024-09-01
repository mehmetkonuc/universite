from django.urls import path
from apps.confessions.views import ConfessionsAddView, ConfessionsView, ConfessionDetailView, ConfessionsEditView, delete_confessions, MyConfessionsView, MyDraftConfessionsView
urlpatterns = [
    path('', ConfessionsView.as_view(), name='confessions'),
    path('my/', MyConfessionsView.as_view(), name='my_confessions'),
    path('draft/', MyDraftConfessionsView.as_view(), name='my_draft_confessions'),
    path('add/', ConfessionsAddView.as_view(), name='confessions_add'),
    path('edit/<slug:slug>', ConfessionsEditView.as_view(), name='confessions_edit'),
    path('<slug:slug>/', ConfessionDetailView.as_view(), name='confession_details'),
    path('delete/<int:confessions_id>', delete_confessions, name='confession_delete'),
]