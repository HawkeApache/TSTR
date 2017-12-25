from __future__ import with_statement

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from tstr.tstr_app.models import Student, OpenQuestion, Test, Group, ClosedQuestion, Answer, WrapWordQuestion
from .resources import StudentResource


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('indeks', 'first_name', 'last_name')
    from_encoding = 'utf-8'


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
