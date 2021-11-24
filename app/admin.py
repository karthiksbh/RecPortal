from django.contrib import admin
from . import models
from .models import User, Domain, Question, Answer, QuestionsTags, Submission, Results


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'reg_no',
        'name',
    ]


@admin.register(Domain)
class DomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'domain_name',
        'quiz_time',
    ]


class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = [
        'option',
        'is_right'
    ]


class TagsInlineModel(admin.TabularInline):
    model = models.QuestionsTags
    fields = [
        'tags',
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'domain',
        'ques_type',
        'mark_each',
        'ques_main',
    ]
    inlines = [
        AnswerInlineModel,
        TagsInlineModel
    ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'option',
        'is_right',
        'question',
    ]


@admin.register(QuestionsTags)
class QuesTagsAdmin(admin.ModelAdmin):
    list_display = [
        'tags',
        'question',
    ]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'sub_student',
        'question',
        'submitted_time',
    ]


@admin.register(Results)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'domain',
        'Total',
    ]
