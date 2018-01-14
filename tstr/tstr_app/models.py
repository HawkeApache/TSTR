import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    question_text = models.TextField()
    difficulty = models.IntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(1)])

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['id']


class OpenQuestion(Question):
    correct_answer = models.TextField()

    def __str__(self):
        return self.__class__.__name__ + " " + self.question_text


class ClosedQuestion(Question):
    answers = models.TextField(
        help_text="Please insert answers separated by & e.g.: answer1 & answer")
    correct_answer = models.CharField(
        max_length=255,
        help_text="Please insert correct answer(s) as integers separated by comma e.g.: 0, 2")

    def __str__(self):
        return self.__class__.__name__ + " " + self.question_text


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    test_name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.test_name


class Student(User):
    is_active_USOS = models.BooleanField(default=True)
    index = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.index + " " + self.first_name + " " + self.last_name


class TeachingGroup(models.Model):
    name = models.CharField(max_length=255)
    tests = models.ManyToManyField(Test)
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


# todo czy na pewno takie relacje??
class Answer(models.Model):
    student = models.ManyToManyField(Student) # ???
    test = models.ManyToManyField(Test)
    question = models.ManyToManyField(Question)
    answer = models.TextField()
    time_of_answer = models.DateTimeField()


class TestResult(models.Model):
    student = models.ManyToManyField(Student)
    test = models.ManyToManyField(Test)
    max_score = models.IntegerField()
    score = models.IntegerField()

    #check if student and test unique together
