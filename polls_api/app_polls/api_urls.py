from django.urls import path

from .api import *

urlpatterns = [
    path('quizzes/all/', QuizAPIView.as_view()),
    path('quizzes/<int:pk>/', QuizDetailAPIView.as_view()),
    path('quizzes/stats/', QuizStatsAPIView.as_view()),
]
