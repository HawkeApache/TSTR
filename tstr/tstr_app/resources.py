#!/usr/bin/env python
# -*- coding: utf-8 -*-

from import_export import resources
from .models import Student
from import_export.fields import Field


class StudentResource(resources.ModelResource):
    last_name = Field(column_name='nazwisko', attribute='last_name')
    first_name = Field(column_name='imie', attribute='first_name')
    indeks = Field(column_name='indeks', attribute='indeks')
    password = Field(column_name='password', attribute='password')
    username = Field(column_name='username', attribute='username')

    class Meta:
        fields = ('indeks', 'is_active_USOS', 'nazwisko', 'imie', 'skreslony', 'rezygnacja')
        import_id_fields = ['indeks']
        exclude = ['imie2']
        model = Student
