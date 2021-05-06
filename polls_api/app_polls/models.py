from random import shuffle

from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    started_at = models.DateTimeField(verbose_name='Дата начала')
    finished_at = models.DateTimeField(verbose_name='Дата окончания')

    class Meta:
        ordering = ['-started_at']
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title

    def get_questions(self):
        questions = list(self.question_set.all())
        shuffle(questions)
        return questions


class Question(models.Model):
    CHOICES = [
        ('Multi', 'Multiple selection'),
        ('Single', 'Single selection'),
        ('Text', 'Text answer')
    ]
    question_type = models.CharField(max_length=6, choices=CHOICES, default='Single', verbose_name='Тип вопроса')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Опрос')
    text = models.TextField(max_length=1000, verbose_name='Текст вопроса')

    def __str__(self):
        return self.text

    def get_answers(self):
        answers = list(self.answer_set.all())
        shuffle(answers)
        return answers


class Answer(models.Model):
    text = models.CharField(max_length=100, blank=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')

    def __str__(self):
        return f'{self.question.text} - {self.text} - {self.is_correct}'


class Result(models.Model):
    user_id = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)

    def __str__(self):
        answers = self.answer.split(', ')
        text_to_return = ''
        for answer in answers:
            if self.question.question_type == 'Text':
                text_to_return = f'{self.question.text} - {self.answer}\n'
            else:
                is_correct = self.question.answer_set.get(text=answer).is_correct
                text_to_return += f'{self.question.text} - {answer} - {is_correct}\n'
        return text_to_return

    def to_dict(self):
        answers = self.__str__().split('\n')[:-1]

        return {self.user_id: answers}
