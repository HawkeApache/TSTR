from django.shortcuts import render
import django.db.models
from tstr.tstr_app.models import Student, TeachingGroup
from tstr.tstr_app.models import Question, OpenQuestion, ClosedQuestion, Test
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "home/landing_page.html", {})


# def questions(request):
#     q = Question.objects.all()
#     return render(request, "home/questions.html", {"questions": q})


# def question(request, question_id):
#     q = get_object_or_404(ClosedQuestion, id=question_id)
#     print(isinstance(q, Question))
#     answers_set = q.answers.split(",")
#     correct = q.correct_answer.split(",")
#     return render(request, "home/question.html", {"question": answers_set, "correct": correct})


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


# wyswietlam grupy do ktorych nalezy student
@login_required
def users_groups(request):
    student_username = request.user.username
    group = TeachingGroup.objects.filter(student__username=student_username)
    return render(request, "home/groups.html", {"groups": group, "title": "Twoje grupy"})


@login_required
def tests_for_group(reguest, group_id):
    # todo sprawdzic czy zalogowany user na pewno ma dostep do tej grupy
    # w przecinwym przypadku 403

    tests = Test.objects.filter(teachinggroup=group_id)
    return render(reguest, "home/tests.html", {"tests": tests, "title": "Testy dostępne dla twojej grupy"})


@login_required
def test(request, test_id):
    #???????
    # jakby na jednej stronie html dalo sie to ogarnac to random bez problema pojdzie
    # todo sprawdzic czy zalogowany user na pewno moze wypelnic dany test(czy ma dostep i czy juz przypadkiem nie wypelnil)
    # w przecinwym przypadku 403

    open_questions = Test.objects.get(id=test_id).open_questions.all()
    print(open_questions)
    closed_questions = Test.objects.get(id=test_id).closed_questions.all()
    print(closed_questions)
    wrap_questions = Test.objects.get(id=test_id).wrap_word_question.all()
    print(wrap_questions)

    #todo handle post z odpowiezdiami do pytan
    #wszystkie pytania na raz wysylane ale po koleji wyswietlane w htmlu

    return render(request, "home/test.html", {"open": open_questions, "closed": closed_questions, "wrap": wrap_questions})


@login_required
def question(request, test_id, question_id):
    #todo handle post

    number_of_questions = Test.objects.get(id=test_id).questions.all().count()
    index_of_current_question = 0
    for index, item in enumerate(Test.objects.get(id=test_id).questions.all()):
        if str(item.id) == question_id:
            index_of_current_question = index+1

    question = Test.objects.get(id=test_id).questions.get(id=question_id)
    next_question = Test.objects.get(id=test_id).questions.filter(id__gt=question.id).first()

    question = precise_question_type(question)
    answers = []
    if isinstance(question, ClosedQuestion):
        answers = question.answers.split("&")

    question_type = str(question.__class__.__name__)

    return render(request, "home/test.html",
                  {"number": index_of_current_question,
                   "all": number_of_questions,
                   "question": question,
                   "answers": answers,
                   "question_type": question_type,
                   "next_question_id": next_question if not next_question else next_question.id,
                   "test_id": test_id})


def precise_question_type(question):
    try:
        return question.openquestion
    except AttributeError:
        try:
            return question.closedquestion
        except AttributeError:
                print("spierdoliło sie na amen")


def open_question(request):
    return render(request, "home/close_question.html", {})