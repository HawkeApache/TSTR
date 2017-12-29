from django.shortcuts import render
import django.db.models
from tstr.tstr_app.models import Student
from tstr.tstr_app.models import Question, OpenQuestion, ClosedQuestion, Test
from django.shortcuts import get_object_or_404


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


def menu(request):
    return render(request, "home/menu.html", {})


def tests(request):
    t = Test.objects.all()
    return render(request, "home/tests.html", {"tests": t, "title": "Aktywne kolokwia"})