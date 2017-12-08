from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# todo abstract question!!!!!!
class OpenQuestion(models.Model):
    question_text = models.TextField()
    correct_answer = models.TextField()
    difficulty = models.IntegerField(default=10) # todo 1-10


class ClosedQuestion(models.Model):
    question_text = models.TextField()
    answer1 = models.TextField()    #Todo lista możliwych odpowiedzi
    answer2 = models.TextField()
    answer3 = models.TextField()
    answer4 = models.TextField()
    correct_answer = models.IntegerField() #todo kurwa lista poprawnych odpoweidzi


class WrapWordQuestion(models.Model):
    question_text = models.TextField() #todo inteligiente zostawianie miejsca
    answer = models.CharField(max_length=255)


class Test(models.Model):
    open_questions = models.ManyToManyField(OpenQuestion)
   # closed_questions = models.ManyToManyField(ClosedQuestion)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    index = models.CharField(max_length=7, unique=True)


class Group(models.Model):
    name = models.CharField(max_length=255)
    tests = models.ManyToManyField(Test)
    student = models.ManyToManyField(Student)


class Answer(models.Model):
    student = models.ManyToManyField(Student)
    test = models.ManyToManyField(Test)
    question = models.ManyToManyField(OpenQuestion) #todo abstract question
    answer = models.IntegerField()
    position_in_test = models.IntegerField()



#todo ładne wyswietlanie modeli w admin panel