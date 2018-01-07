# -*- coding: utf-8 -*-
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
    errors = []
    if not request.user.is_superuser:
        index_nr = Student.objects.get(username=request.user.username).index
    else:
        index_nr = ""
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('settings')
        else:
            errors.append('Wystąpił błąd')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/settings.html', {'errors': errors, 'index_nr': index_nr}, {
        'form': form
    })
