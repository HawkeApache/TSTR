#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Classes to custom views in admin panel"""
from import_export import resources
from import_export.fields import Field
from .models import Student


class StudentResource(resources.ModelResource):
    """Class to custom view of students in admin panel"""
    last_name = Field(column_name='nazwisko', attribute='last_name')
    first_name = Field(column_name='imie', attribute='first_name')
    index = Field(column_name='index', attribute='index')
    username = Field(column_name='username', attribute='username')


class Meta:
    """Data to custom view in admin panel"""
    fields = ('index', 'is_active_USOS', 'nazwisko', 'imie', 'skreslony', 'rezygnacja')
    import_id_fields = ['index']
    exclude = ['imie2']
    model = Student
