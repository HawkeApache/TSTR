"""Tests for models in application"""
from datetime import datetime

from django.test import TestCase

from tstr.tstr_app.models import *


class QuestionTestCase(TestCase):
    """Tests to model object - question"""
    def setUp(self):
        """Set up objects to tests"""
        Question.objects.create(question_text="test question text", difficulty=8)
        Question.objects.create(question_text="test question text2")

    def test_question_difficulty(self):
        """Difficulty or default value should be correctly set"""
        first = Question.objects.get(question_text="test question text")
        second = Question.objects.get(question_text="test question text2")
        self.assertEqual(first.difficulty, 8)
        self.assertEqual(second.difficulty, 10)

    def test_question_default_id(self):
        """ID should be automatically set"""
        first = Question.objects.get(question_text="test question text")
        second = Question.objects.get(question_text="test question text2")
        self.assertIsNotNone(first.id)
        self.assertIsNotNone(second.id)

    def test_question_str(self):
        """Str function should be correctly override"""
        first = Question.objects.get(question_text="test question text")
        second = Question.objects.get(question_text="test question text2")
        self.assertEqual(str(first), "test question text")
        self.assertEqual(str(second), "test question text2")


class OpenQuestionTestCase(TestCase):
    """Tests to model object - openquestion"""
    def setUp(self):
        """Set up objects to tests"""
        OpenQuestion.objects.create(question_text="test open question text", difficulty=8)
        OpenQuestion.objects.create(question_text="test open question text2")

    def test_open_question_str(self):
        """Str function should be correctly override"""
        first = OpenQuestion.objects.get(question_text="test open question text")
        second = OpenQuestion.objects.get(question_text="test open question text2")
        self.assertEqual(str(first), "OpenQuestion test open question text")
        self.assertEqual(str(second), "OpenQuestion test open question text2")


class ClosedQuestionTestCase(TestCase):
    """Tests to model object - closedquestion"""
    def setUp(self):
        """Set up objects to tests"""
        ClosedQuestion.objects.create(question_text=
                                      "test closed question text", difficulty=8, correct_answer=1)
        ClosedQuestion.objects.create(question_text="test closed question text2", correct_answer=0)

    def test_closed_question_str(self):
        """Str function should be correctly override"""
        first = ClosedQuestion.objects.get(question_text="test closed question text")
        second = ClosedQuestion.objects.get(question_text="test closed question text2")
        self.assertEqual(str(first), "ClosedQuestion test closed question text")
        self.assertEqual(str(second), "ClosedQuestion test closed question text2")

    def test_closed_question_cor_answer(self):
        """ClosedQuestion object cannot be created with empty correct_answer field"""
        try:
            ClosedQuestion.objects.create(question_text="uncorrect")
            self.fail("ClosedQuestion cannot be created with empty correct_answer field")
        except Exception:
            pass


class TestTestCase(TestCase):
    """Tests to model object - test"""
    def setUp(self):
        """Set up objects to tests"""
        Test.objects.create(test_name="test", start_time=datetime.now(), end_time=datetime.now())
        Test.objects.create(test_name="test 2", start_time=datetime.now(), end_time=datetime.now())

    def test_test_str(self):
        """Str function should return test name"""
        first = Test.objects.get(test_name="test")
        second = Test.objects.get(test_name="test 2")
        self.assertEqual(str(first), "test")
        self.assertEqual(str(second), "test 2")

    def test_test_start_time(self):
        """Start_time field cannot be empty"""
        try:
            Test.objects.create(test_name="test", end_time=datetime.now())
            self.fail("Test cannot be created with empty start_time field")
        except Exception:
            pass

    def test_test_end_time(self):
        """End_time field cannot be empty"""
        try:
            Test.objects.create(test_name="test", start_time=datetime.now())
            self.fail("Test cannot be created with empty end_time field")
        except Exception:
            pass


class StudentTestCase(TestCase):
    """Tests to model object - Student"""
    def setUp(self):
        """Set up objects to tests"""
        Student.objects.create(index="123", first_name="test", last_name="test", username="abc")
        Student.objects.create(index="234", first_name="test",
                               last_name="test", is_active_USOS=False, username="abc1")

    def test_student_test_str(self):
        """Str function should return index + first_name + last_name of student"""
        student = Student.objects.get(index="123")
        self.assertEqual(str(student), "123 test test")

    def test_student_index_must_be(self):
        """Index field cannot be empty"""
        try:
            Student.objects.create(first_name="test", last_name="test")
            self.fail("Student cannot be created with empty index field")
        except Exception:
            pass

    def test_student_is_active(self):
        """Is active should be set automatically to true or to value from init param"""
        student = Student.objects.get(index="123")
        student2 = Student.objects.get(index="234")
        self.assertEqual(student.is_active_USOS, True)
        self.assertEqual(student2.is_active_USOS, False)

    def test_student_index_unique(self):
        """Index field in student object must be unique"""
        try:
            Student.objects.create(index="123", first_name="test",
                                   last_name="test", username="abc3")
            self.fail("Student cannot be created with non unique index field")
        except Exception:
            pass

    def test_student_username_unique(self):
        """Username field in student object must be unique"""
        try:
            Student.objects.create(index="1233", first_name="test",
                                   last_name="test", username="abc")
            self.fail("Student cannot be created with non unique username field")
        except Exception:
            pass


class TeachingGroupTestCase(TestCase):
    """Tests to model object - teaching group"""
    def setUp(self):
        """Set up objects to tests"""
        TeachingGroup.objects.create(name="group1")

    def test_teachinggroup_str(self):
        """Str function should return group name"""
        first = TeachingGroup.objects.get(name="group1")
        self.assertEqual(str(first), "group1")
