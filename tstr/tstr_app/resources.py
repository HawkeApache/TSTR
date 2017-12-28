#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

from django.http import HttpResponse
from import_export import resources
from .models import Student
from import_export.fields import Field
import random
from django.utils.encoding import force_text


class StudentResource(resources.ModelResource):
    last_name = Field(column_name='nazwisko', attribute='last_name')
    first_name = Field(column_name='imie', attribute='first_name')
    indeks = Field(column_name='indeks', attribute='indeks')
    password = Field(column_name='password', attribute='password')
    username = Field(column_name='username', attribute='username')

    def before_import(self, dataset, using_transactions, dry_run=False, **kwargs):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
        for data in dataset.dict:
            first_name = force_text(data['imie'], 'utf-8')
            last_name = force_text(data['nazwisko'], 'utf-8')
            is_active_usos = 1
            if data['rezygnacja'] == '1' or data['skreslony'] == '1':
                is_active_usos = 0
            username = 's' + force_text(data['indeks'], 'utf-8')
            index = force_text(data['indeks'], 'utf-8')
            password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

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

        return super(StudentResource, self).before_import(dataset, using_transactions, dry_run, **kwargs)


    class Meta:
        fields = ('indeks', 'is_active_USOS', 'nazwisko', 'imie', 'skreslony', 'rezygnacja')
        import_id_fields = ['indeks']
        exclude = ['imie2']
        model = Student
