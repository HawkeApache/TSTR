from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Question(models.Model):
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


class OpenQuestion(Question):
    correct_answer = models.TextField()
    difficulty = models.IntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(1)])


class ClosedQuestion(Question):
    answer1 = models.TextField()    #Todo lista mozliwych odpowiedzi
    answer2 = models.TextField()
    answer3 = models.TextField()
    answer4 = models.TextField()
    correct_answer = models.CharField(max_length=255) #todo kurwa lista poprawnych odpoweidzi


class WrapWordQuestion(Question):
    #todo inteligiente zostawianie miejsca
    correct_answer = models.CharField(max_length=255)


class Test(models.Model):
    test_name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)

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
