from django.shortcuts import render
import django.db.models
from tstr.tstr_app.models import Student


def index(request):
    return render(request, "home/landing_page.html", {})


def menu(request):
    return render(request, "home/menu.html", {})