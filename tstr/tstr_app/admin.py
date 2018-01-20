# -*- coding: utf-8 -*-
"""Admin panel"""
import sys
import django

# Register your models here.
from django.contrib import admin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from import_export.admin import ImportExportModelAdmin
from tstr.tstr_app.models import (
    Student,
    OpenQuestion, Test, TeachingGroup,
    ClosedQuestion, Answer, TestResult
)
from .resources import StudentResource


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    """Import students"""
    resource_class = StudentResource
    list_display = ('index', 'first_name', 'last_name', 'is_active_USOS')
    from_encoding = 'utf-8'

    def import_action(self, request, *args, **kwargs):
        '''Action to import students list from csv format'''

        resource = self.get_import_resource_class()(
            **self.get_import_resource_kwargs(request, *args, **kwargs))
        context = self.get_import_context_data()

        import_formats = self.get_import_formats()
        form_type = self.get_import_form()
        form = form_type(import_formats,
                         request.POST or None,
                         request.FILES or None)

        tmpfile = open("passwords.txt", "wb")

        if request.POST and form.is_valid():

            import_file = form.cleaned_data['import_file']
            data = bytes()
            for chunk in import_file.chunks():
                data += chunk

            tab = data.split(b'\r\n')
            for index, line in enumerate(tab):
                if index == 0:
                    continue
                if len(line) == 0:
                    continue
                elem = str(line.decode(sys.getdefaultencoding())).split(";")
                first_name = elem[1].replace('"', '')
                last_name = elem[0].replace('"', '')
                is_active_usos = 1
                if elem[3].replace('"', '') == '1' or elem[4].replace('"', '') == '1':
                    is_active_usos = 0
                username = 's' + elem[5].replace('"', '')
                index = elem[5].replace('"', '')

                try:
                    student = Student.objects.get(index=index)
                except Student.DoesNotExist:
                    student = Student.objects.create_user(username=username, index=index)

                student.index = index
                student.username = username
                student.first_name = first_name
                student.last_name = last_name
                student.is_active_USOS = is_active_usos
                password = Student.objects.make_random_password(8)
                student.set_password(password)
                tmpfile.write((username + " "
                               + first_name + " "
                               + last_name + " "
                               + password + "\n").encode('utf8'))
                student.save()

            tmpfile.close()
            return redirect('/admin/tstr_app/student')

        if django.VERSION >= (1, 8, 0):
            context.update(self.admin_site.each_context(request))
        elif django.VERSION >= (1, 7, 0):
            context.update(self.admin_site.each_context())

        context['title'] = ("Import")
        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_user_visible_fields()]

        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name], context)


@admin.register(OpenQuestion)
class OpenQuestionAdmin(admin.ModelAdmin):
    """Display open questions for admin"""
    list_display = ('id', 'question_text',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Display tests for admin"""
    list_display = ('test_name', 'start_time', 'end_time')


@admin.register(TeachingGroup)
class GroupAdmin(admin.ModelAdmin):
    """Display groups for admin"""
    list_display = ('name',)


@admin.register(ClosedQuestion)
class ClosedQuestionAdmin(admin.ModelAdmin):
    """Display closed questions for admin"""
    list_display = ('id', 'question_text',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Display answers for admin"""
    list_display = ('student', 'test', 'is_correct')


def recalculate_test_results(modeladmin, request, queryset):
    """Automatically score answers for closed questions"""
    for query in queryset:
        query.score = 0
        query.save()
        answers = Answer.objects.all().filter(student=query.student, test=query.test)
        for answer in answers:
            if answer.is_correct:
                query.score = int(query.score) + 1
                query.save()


recalculate_test_results.short_description = "Recalculate test result"


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    """Display test results and possibility to recalculate it"""
    list_display = ('student', 'test', 'score', 'max_score')
    actions = [recalculate_test_results]
