import datetime
import pytz

from django.shortcuts import render
import django.db.models
from tstr.tstr_app.models import Student, TeachingGroup, User
from tstr.tstr_app.models import Question, OpenQuestion, ClosedQuestion, Test, Answer, TestResult
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
    student = User.objects.get(username=reguest.user.username)
    test_results = Test.objects.filter(testresult__student=student)
    current_time = timezone.now()

    for t in tests:
        if t in test_results:
            t.active = False
        else:
            if t.start_time <= current_time <= t.end_time:
                t.active = True
            else:
                t.active = False



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
    # post handler
    if request.method == "POST":
        current_user = request.user.username
        current_student = User.objects.get(username=current_user).student
        current_test = Test.objects.get(id=test_id)
        current_question = Question.objects.get(id=question_id)
        current_time = timezone.now()

        answer = Answer.objects.create(time_of_answer=current_time)

        nxt = ""

        if "open" in request.POST:
            user_answer = request.POST.get('question_input')
            answer.answer = user_answer
            answer.save()

            answer.student.add(current_student)
            answer.test.add(current_test)
            answer.question.add(current_question)

            nxt = request.POST.get('open')
            if not nxt:
                test_result = TestResult.objects.create(max_score=Test.objects.get(id=test_id).questions.all().count(), score=0)
                test_result.save()
                test_result.student.add(current_student)
                test_result.test.add(current_test)
                return redirect("end")

        if "close" in request.POST:
            user_answer = request.POST.get("radio")
            answer.answer = user_answer
            answer.save()

            answer.student.add(current_student)
            answer.test.add(current_test)
            answer.question.add(current_question)

            nxt = request.POST.get('close')
            if not nxt:
                test_result = TestResult.objects.create(max_score=Test.objects.get(id=test_id).questions.all().count(), score=0)
                test_result.save()
                test_result.student.add(current_student)
                test_result.test.add(current_test)
                return redirect("end")

        return redirect('test', test_id, nxt)

    # get index of current question and number of all questions
    number_of_questions = Test.objects.get(id=test_id).questions.all().count()
    index_of_current_question = 0
    for index, item in enumerate(Test.objects.get(id=test_id).questions.all()):
        if str(item.id) == question_id:
            index_of_current_question = index+1

    # get current question
    question = precise_question_type(Test.objects.get(id=test_id).questions.get(id=question_id))
    next_question = Test.objects.get(id=test_id).questions.filter(id__gt=question.id).first()

    # if ClosedQuestion
    answers = []
    if isinstance(question, ClosedQuestion):
        answers = question.answers.split("&")

    return render(request, "home/test.html",
                  {"number": index_of_current_question,
                   "all": number_of_questions,
                   "question": question,
                   "answers": answers,
                   "question_type": str(question.__class__.__name__),
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


def end(request):
    return render(request, "home/end.html", {})
