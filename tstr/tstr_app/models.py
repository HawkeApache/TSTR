"""Django models"""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """Parent type for open and closed questions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    question_text = models.TextField()
    difficulty = models.IntegerField(default=10, validators=[MaxValueValidator(10),
                                                             MinValueValidator(1)])

    def __str__(self):
        """Override str function to return question text"""
        return self.question_text

    class Meta:
        """Set order in admin panel by id"""
        ordering = ['id']


class OpenQuestion(Question):
    """Open question - student has no possible answers,
    question for example to write some code"""
    correct_answer = models.TextField()

    def __str__(self):
        """Override str function to return OpenQuestion + question text"""
        return self.__class__.__name__ + " " + self.question_text


class ClosedQuestion(Question):
    """Closed question - student has to choose one of possible answers"""
    answers = models.TextField(
        help_text="Please insert answers separated by & e.g.: answer1 & answer")
    correct_answer = models.IntegerField(help_text="Please note that answers are indexing from 0")

    def __str__(self):
        """Override str function to return ClosedQuestion + question text"""
        return self.__class__.__name__ + " " + self.question_text


class Test(models.Model):
    """Collection of questions - with additional parameters like start_time, end_time,
     id and test_name"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    test_name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        """Override str function to return test name"""
        return self.test_name


class Student(User):
    """All data about student - username, first and last name, password,
    is active in USOS and index number. Most of data is inherited from User class."""
    is_active_USOS = models.BooleanField(default=True)
    index = models.CharField(max_length=7, unique=True)

    def __str__(self):
        """Override str function to return base info about student"""
        return self.index + " " + self.first_name + " " + self.last_name


class TeachingGroup(models.Model):
    """Class to store students in groups (like during lessons)
    with tests assigned to each group"""
    name = models.CharField(max_length=255)
    tests = models.ManyToManyField(Test)
    student = models.ManyToManyField(Student)

    def __str__(self):
        """Override str function to return group name"""
        return self.name


class Answer(models.Model):
    """Class to store students answers with additional parameters"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    answer = models.TextField()
    time_of_answer = models.DateTimeField()


class TestResult(models.Model):
    """Class to store students' scores in tests"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    max_score = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    class Meta:
        """Each pair (student, test) should be unique"""
        unique_together = ('student', 'test')


class TestInProgress(models.Model):
    """Class to mark actual student's position in test"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
