from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.QuestionsView.as_view(), name='questions'),
    path('my/', views.MyQuestionsView.as_view(), name='my_questions'),
    path('draft/', views.DraftQuestionsView.as_view(), name='draft_questions'),
    path('<slug:slug>', views.QuestionsDetailsView.as_view(), name='question_details'),
    path('add/', views.QuestionsAddView.as_view(), name='questions_add'),
    path('edit/<slug:slug>', views.QuestionsEditView.as_view(), name='questions_edit'),
    path('delete/<slug:slug>', views.delete_questions, name='questions_delete'),
]
