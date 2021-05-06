from django.contrib import admin

from .models import Quiz, Answer, Question


class AnswerInLine(admin.TabularInline):
    model = Answer


class QuestionInLine(admin.TabularInline):
    model = Question


@admin.register(Quiz)
class PollAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine]

    class Meta:
        model = Quiz

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('started_at', )
        return self.readonly_fields


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]

    class Meta:
        model = Question


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    class Meta:
        model = Answer
