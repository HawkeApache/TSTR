# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render
import django.db.models
from tstr.tstr_app.models import Student
from tstr.tstr_app.models import Question, OpenQuestion, ClosedQuestion
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomizedPasswordChange

def index(request):
    return render(request, "home/landing_page.html", {})


def questions(request):
    q = Question.objects.all()
    return render(request, "home/questions.html", {"questions": q})


def question(request, question_id):
    q = get_object_or_404(ClosedQuestion, id=question_id)
    print(isinstance(q, Question))
    answers_set = q.answers.split(",")
    correct = q.correct_answer.split(",")
    return render(request, "home/question.html", {"question": answers_set, "correct": correct})


@login_required
def menu(request):
    return render(request, "home/menu.html", {})


def login_user(request):
    errors = []
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    get_object_or_404(Student, auth=request.user)

                except:
                    url = reverse('menu', args=(),
                                  kwargs={})
                    return HttpResponseRedirect(url)
                url = reverse('menu', args=(),
                              kwargs={})
                return HttpResponseRedirect(url)
            else:
                errors.append('Nieaktywne konto')

        else:
            errors.append('Niepoprawne dane')
    return render(request, 'home/landing_page.html', {'errors': errors})


@login_required
def settings(request):

    if request.method == 'POST':
        form = CustomizedPasswordChange(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Hasło zmienione!')
            return redirect('menu')
        else:
            messages.error(request, 'Wystąpił błąd. Popraw dane.')
    else:
        form = CustomizedPasswordChange(request.user)
    return render(request, 'home/settings.html', {
        'form': form
    })
