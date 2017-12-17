from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.TextField()
    difficulty = models.IntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(1)])

    def __str__(self):
        return self.question_text


class OpenQuestion(Question):
    correct_answer = models.TextField()


class ClosedQuestion(Question):
    answers = models.TextField(
        help_text="Please insert answers separated by comma e.g.: answer1, answer")
    correct_answer = models.CharField(
        max_length=255,
        help_text="Please insert correct_answers separeted by comma as integers e.g.: 0,2")
    #todo add validator to check if field is python list


class WrapWordQuestion(Question):
    #todo inteligiente zostawianie miejsca
    correct_answer = models.CharField(max_length=255)


class Test(models.Model):
    test_name = models.CharField(max_length=255)
    open_questions = models.ManyToManyField(OpenQuestion)
    closed_questions = models.ManyToManyField(ClosedQuestion)
    wrap_word_question = models.ManyToManyField(WrapWordQuestion)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.test_name


class Student(User):
    is_active_USOS = models.BooleanField(default=True)
    index = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.index


class Group(models.Model):
    name = models.CharField(max_length=255)
    tests = models.ManyToManyField(Test)
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


# todo czy na pewno takie relacje??
class Answer(models.Model):
    student = models.ManyToManyField(Student)
    test = models.ManyToManyField(Test)
    question = models.ManyToManyField(Question)
    answer = models.IntegerField()
    position_in_test = models.IntegerField()
    time_of_answer = models.DateTimeField()
