from django.urls import path

from .views import *

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('stats/', UserStatsView.as_view(), name='user_stats'),
    path('login/', QuizLogin.as_view(), name='login'),
]
