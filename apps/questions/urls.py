from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.QuestionsView.as_view(), name='questions'),
    path('question/<slug:slug>', views.QuestionsDetailsView.as_view(), name='question_details'),
    path('add/', views.QuestionsAddView.as_view(), name='questions_add'),

]
