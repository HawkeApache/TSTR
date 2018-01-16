# -*- coding: utf-8 -*-
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from tstr.tstr_app.models import Question, ClosedQuestion, Test, Answer, TestResult, TestInProgress, Student, \
    TeachingGroup, User
from tstr.tstr_app.utils import precise_question_type
from .forms import CustomizedPasswordChange


def index(request):
    return render(request, "home/landing_page.html", {})


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
    if not request.user.is_superuser:
        index_nr = Student.objects.get(username=request.user.username).index
    else:
        index_nr = ""

    if request.method == 'POST':
        form = CustomizedPasswordChange(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Hasło zmienione!')
            return redirect('settings')
        else:
            messages.error(request, 'Wystąpił błąd. Popraw dane.')
    else:
        form = CustomizedPasswordChange(request.user)
    return render(request, 'home/settings.html', {
        'form': form, 'index_nr': index_nr
    })


@login_required
def users_groups(request):
    current_user = request.user.username
    current_student = User.objects.get(username=current_user).student
    tests = TestInProgress.objects.all().filter(student=current_student)
    if tests:
        return begin_tests(request)

    student_username = request.user.username
    group = TeachingGroup.objects.filter(student__username=student_username)
    return render(request, "home/groups.html", {"groups": group, "title": "Twoje grupy"})


@login_required
def tests_for_group(reguest, group_id):
    tests = Test.objects.filter(teachinggroup=group_id)
    student = User.objects.get(username=reguest.user.username)
    test_results = Test.objects.filter(testresult__student=student)
    current_time = timezone.now()

    for t in tests:
        if t in test_results:
            t.active = False
        else:
            if t.start_time <= current_time <= t.end_time:
                first_question = random.choice(Question.objects.all().filter(test=t))
                t.first_question = first_question.id
                t.active = True
            else:
                t.active = False

    return render(reguest, "home/tests.html", {"tests": tests, "title": "Testy dostępne dla twojej grupy"})


@login_required
def question(request, test_id, question_id):
    # get necessary information
    current_user = request.user.username
    current_student = User.objects.get(username=current_user).student
    current_test = Test.objects.get(id=test_id)

    # post handler
    if request.method == "POST":
        current_question = Question.objects.get(id=question_id)
        current_time = timezone.now()

        answer = Answer.objects.create(
            time_of_answer=current_time,
            question=current_question,
            test=current_test,
            student=current_student)

        nxt = ""

        if "open" in request.POST:
            user_answer = request.POST.get('question_input')
            answer.answer = user_answer
            answer.save()

            nxt = request.POST.get('open')
            if not nxt or current_test.end_time <= current_time:
                test_result = TestResult.objects.create(
                    max_score=Test.objects.get(id=test_id).questions.all().count(),
                    score=0,
                    student=current_student,
                    test=current_test)
                test_result.save()

                TestInProgress.objects.get(student=current_student, test=current_test).delete()

                return redirect("end")

        if "close" in request.POST:
            user_answer = request.POST.get("radio")
            answer.answer = user_answer
            answer.is_correct = str(user_answer) == str(current_question.closedquestion.correct_answer)
            answer.save()

            nxt = request.POST.get('close')
            if not nxt or current_test.end_time <= current_time:
                test_result = TestResult.objects.create(
                    max_score=Test.objects.get(id=test_id).questions.all().count(),
                    score=0,
                    student=current_student,
                    test=current_test)
                test_result.save()

                TestInProgress.objects.get(student=current_student, test=current_test).delete()

                return redirect("end")

        return redirect('test', test_id, nxt)

    # get index of current question and number of all questions
    number_of_questions = Test.objects.get(id=test_id).questions.all().count()
    index_of_current_question = Answer.objects.all().filter(test=current_test, student=current_student).count() + 1

    # get current question
    current_question = precise_question_type(Test.objects.get(id=test_id).questions.get(id=question_id))

    # get next question id randomly
    all_answers = Answer.objects.all().filter(test=current_test, student=current_student)
    questions_ids = [x.question.id for x in all_answers]
    questions_ids.append(question_id)

    try:
        available_questions = Test.objects.get(id=test_id).questions.all().exclude(id__in=questions_ids)
        next_question = random.choice(available_questions)
    except IndexError:
        next_question = ""

    # save current test state
    in_progress, created = TestInProgress.objects.get_or_create(student=current_student, test=current_test)
    in_progress.question = current_question
    in_progress.save()

    # prepare possible answers if ClosedQuestion
    answers = []
    if isinstance(current_question, ClosedQuestion):
        answers = current_question.answers.split("&")

    return render(request, "home/test.html",
                  {"number": index_of_current_question,
                   "all": number_of_questions,
                   "question": current_question,
                   "answers": answers,
                   "question_type": str(current_question.__class__.__name__),
                   "next_question_id": next_question if not next_question else next_question.id,
                   "test_id": test_id})


def end(request):
    return render(request, "home/end.html", {})


@login_required
def begin_tests(request):
    current_user = request.user.username
    current_student = User.objects.get(username=current_user).student

    tests = TestInProgress.objects.all().filter(student=current_student)

    return render(request, "home/begin_tests.html", {"tests": tests})


def error404(request):
    return render(request, "home/404.html", {})


def error500(request):
    return render(request, "home/500.html", {})


@login_required
def finished(request):
    student_username = request.user.username
    group = TeachingGroup.objects.filter(student__username=student_username)
    return render(request, "home/groups_fin.html", {"groups": group, "title": "Twoje grupy"})


@login_required
def closed_for_group(request, group_id):
    tests = Test.objects.filter(teachinggroup=group_id)
    student = User.objects.get(username=request.user.username)
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

    return render(request, "home/finished_tests.html", {"tests": tests,
                                                        "title": "Zakończone testy twojej grupy"
                                                        })


@login_required
def result(request, test_id):
    # get necessary information
    current_user = request.user.username
    current_student = User.objects.get(username=current_user).student
    current_test = Test.objects.get(id=test_id)
    current_test_name = current_test.test_name
    current_test_questions = current_test.questions.all()
    current_test_answers_all = Answer.objects.all().filter(test=current_test, student=current_student)
    current_result = TestResult.objects.get(student=current_student, test=test_id)
    number_of_questions = Test.objects.get(id=test_id).questions.all().count()

    return render(request, "home/result.html",
                  {"test_id": test_id, "test_name": current_test_name,
                   "test": current_test_questions,
                   "answers": current_test_answers_all,
                   "score": current_result.score,
                   "max_score": current_result.max_score,
                   "all": number_of_questions
                   })


