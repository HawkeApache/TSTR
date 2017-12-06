from django.shortcuts import render
import django.db.models
from tstr.tstr_app.models import Student


def index(request):
    return render(request, "index.html", {})

