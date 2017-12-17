from django.contrib import admin

# Register your models here.
from tstr.tstr_app.models import Student, OpenQuestion, Test, Group, ClosedQuestion, Answer, WrapWordQuestion


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('index', 'first_name', 'last_name')


@admin.register(OpenQuestion)
class OpenQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'start_time', 'end_time')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ClosedQuestion)
class ClosedQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text',)


@admin.register(WrapWordQuestion)
class WrapWordQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id',)
