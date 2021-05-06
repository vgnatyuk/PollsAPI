from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Quiz, Result


class QuizLogin(LoginView):
    pass


class QuizListView(generic.ListView):
    model = Quiz
    context_object_name = 'quizzes'

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        print(request.COOKIES.get('sessionid', 'sessionid doesnot exists'))
        # response.set_cookie('sessionid', '486486saddf', max_age=60*60*24*14)
        return response


class QuizDetailView(generic.DetailView):
    model = Quiz
    context_object_name = 'quiz'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        quiz = Quiz.objects.get(pk=pk)
        questions = []
        for question in quiz.get_questions():
            answers = []
            for answer in question.get_answers():
                answers.append(answer.text)
            questions.append({question.text: answers})
        return render(request, 'app_polls/quiz_detail.html', context={'quiz': quiz, 'questions': questions})

    def post(self, request, *args, **kwargs):
        id = request.COOKIES['sessionid']
        post_data = dict(request.POST)
        pk = self.kwargs['pk']
        questions = Quiz.objects.get(pk=pk).get_questions()
        context = f'<p>{id}</p>'
        for question in questions:
            user_answers = post_data.get(question.text)
            if user_answers is None:
                Result.objects.update_or_create(user_id=id, question=question, defaults={'answer': 'not answered'})
                context += f'<p>{question} - not answered</p>'
                continue
            for answer in user_answers:
                if question.question_type == 'Text':
                    if answer.strip() == '':
                        answer = 'not answered'
                    context += f'<p>{question} - {answer}</p>'
                    continue
                answered = question.answer_set.all().filter(text=answer)[0]
                context += f'<p>{question} - {answered.text} - {answered.is_correct}</p>'
            Result.objects.update_or_create(user_id=id, question=question, defaults={'answer': ', '.join(user_answers)})
        return HttpResponse(context)


class UserStatsView(generic.ListView):
    model = Result

    def get(self, request, *args, **kwargs):
        id = request.GET['id']
        results = []
        user_results = list(Result.objects.all().filter(user_id=id))

        for res in user_results:
            answers = str(res).split('\n')[:-1]
            for answer in answers:
                results.append(answer)
        return render(request, 'app_polls/result_list.html', context={'results': results})
