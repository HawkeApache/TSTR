from django.http import HttpResponse
from django.shortcuts import render
import django.db.models
from tstr.tstr_app.models import Student
from tstr.tstr_app.models import Question, OpenQuestion, ClosedQuestion
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, "index.html", {})


def questions(request):
    q = Question.objects.all()
    return render(request, "home/questions.html", {"questions": q})


def question(request, question_id):
    q = get_object_or_404(ClosedQuestion, id=question_id)
    print(isinstance(q, Question))
    answers_set = q.answers.split(",")
    correct = q.correct_answer.split(",")
    return render(request, "home/question.html", {"question": answers_set, "correct": correct})
