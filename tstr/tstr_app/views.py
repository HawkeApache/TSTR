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

    # altenatywa dla test
    # renderuje się zaraz po przejsciu z test_for_groups
    # link do pierwszego pytania z widoku tests_for_group i zaczynamy rozwiązywanie testu
    # w returnie pytanie, typ pytania i id następnego pytania(jak zrandomizowac???)
    # sprawdzamy czy jest next id z open jak tak to spoko jak nie to nierzemy closed a nastepnie wrap

    #case if we start test
    question_type = ""
    questions = []
    if question_id == "0":
        question_type = "open_question"
        questions = Test.objects.get(id=test_id).open_questions.all()
        if not questions:
            question_type = "closed_question"
            questions = Test.objects.get(id=test_id).closed_questions.all()
            if not questions:
                question_type = "wrap_question"
                questions = Test.objects.get(id=test_id).wrap_word_question.all()


    print(question_type)
    print(questions[0])
    return render(request, "home/test.html", {"q": question_id, "t": test_id})
