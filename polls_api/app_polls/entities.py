from .models import Quiz


class Quizzes:
    def __init__(self, title):
        quiz = Quiz.objects.get(title=title)
        self.title = quiz.title
        self.description = quiz.description
        self.started_at = quiz.started_at
        self.finished_at = quiz.finished_at
        self.questions_and_answers = self.get_questions_answers()

    def get_questions_answers(self):
        quiz = Quiz.objects.get(title=self.title)
        questions = []
        for question in quiz.get_questions():
            if question.question_type == 'Text':
                questions.append({'question_id': question.pk, question.text: ['Your answer']})
                continue
            answers = []
            for answer in question.get_answers():
                answers.append(answer.text)
            questions.append({'question_id': question.pk, question.text: answers})
        return questions

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'started_at': self.started_at,
            'finished_at': self.finished_at,
            'questions_and_answers': self.questions_and_answers,
        }
