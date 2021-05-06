from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .entities import Quizzes
from .models import Quiz, Result, Question
from .serializers import QuizSerializer, QuizModelSerializer, ResultModelSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizAPIView(ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizModelSerializer


class QuizDetailAPIView(APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            quiz = Quiz.objects.get(pk=pk)
            quiz = Quizzes(title=quiz.title)
            return Response(quiz.to_dict())
        except Exception:
            return Response('Doesnt exists.')

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        id = request.data.get('id')
        questions = request.data.get('questions')

        for question_answer in questions:
            q_id, answers = list(question_answer.items())[0]
            q_id = int(q_id)
            question = Question.objects.get(pk=q_id)
            allowed_answers = [answer.text for answer in question.get_answers()]
            if not question.question_type == 'Text':
                answers = [answer for answer in answers if answer in allowed_answers]
            if answers:
                Result.objects.update_or_create(user_id=id, question_id=q_id, defaults={'answer': ', '.join(answers)})
        return Response('Received!')


class QuizStatsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('id')
        results = Result.objects.all().filter(user_id=user_id)
        user_results = ResultModelSerializer(results, many=True)
        return Response(user_results.data)

    # {
    #     "id": "new_id",
    #     "questions": [
    #         {"1": [
    #             "a3333"
    #         ]},
    #         {"3": [
    #             "My answer"
    #         ]},
    #         {"2": [
    #             "a111",
    #             "a222"
    #         ]}
    #     ]
    # }
