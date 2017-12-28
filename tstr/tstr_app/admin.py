from __future__ import with_statement

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from tstr.tstr_app.models import Student, OpenQuestion, Test, Group, ClosedQuestion, Answer, WrapWordQuestion
from .resources import StudentResource


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('indeks', 'first_name', 'last_name')
    from_encoding = 'utf-8'

    def import_action(self, request, *args, **kwargs):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''

        print("import action!")
        resource = self.get_import_resource_class()(**self.get_import_resource_kwargs(request, *args, **kwargs))

        context = self.get_import_context_data()

        import_formats = self.get_import_formats()
        form_type = self.get_import_form()
        form = form_type(import_formats,
                         request.POST or None,
                         request.FILES or None)

        print("przed ifem")
        if request.POST and form.is_valid():
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            tmp_storage = self.get_tmp_storage_class()()
            data = bytes()
            for chunk in (import_file.chunks()):
                data += chunk

            import random
            import string
            from tstr.tstr_app.models import Student

            tab = data.split(b'\r\n')
            for index, line in enumerate(tab):
                if index == 0:
                    continue
                elem = str(line.decode('utf-8')).split(";")
                first_name = elem[1].replace('"', '')
                last_name = elem[0].replace('"', '')
                is_active_usos = 1
                if elem[3].replace('"', '') == '1' or elem[4].replace('"', '') == '1':
                    is_active_usos = 0
                username = 's' + elem[5].replace('"', '')
                index = elem[5].replace('"', '')
                password = ''.join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

                print(first_name, last_name, index, username, password, is_active_usos, sep=" ; ")

                try:
                    student = Student.objects.get(indeks=index)
                except Student.DoesNotExist:
                    student = Student.objects.create_user(username=username, indeks=index)

                student.indeks = index
                student.username = username
                student.first_name = first_name
                student.last_name = last_name
                student.is_active_USOS = is_active_usos
                student.password = password
                student.save()

            return redirect('/admin/tstr_app/student')


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
