from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Quiz, Result, Question, Answer


class QuizSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=2000)
    started_at = serializers.DateTimeField()
    finished_at = serializers.DateTimeField()

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)


class QuizModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'question_type']


class AnswerField(serializers.RelatedField):
    queryset = Answer.objects.all()

    def to_representation(self, value):
        answers_list = []
        answers = value.split(', ')
        for answer in answers:
            try:
                answer_obj = str(get_object_or_404(Answer.objects.all(), text=answer))
                answer_obj = answer_obj.split(' - ')[1:]
                answers_list.append(answer_obj)
            except Http404:
                answers_list.append([answer, 'True'])
        return answers_list


class ResultModelSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    answer = AnswerField()

    class Meta:
        model = Result
        fields = ['question', 'answer']
