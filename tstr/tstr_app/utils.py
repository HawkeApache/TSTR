"""Helper functions"""
from tstr.tstr_app.models import *


def precise_question_type(question):
    """Check type of question - open or closed"""
    try:
        return question.openquestion
    except AttributeError:
        try:
            return question.closedquestion
        except AttributeError:
            print("Attribute error in precise question type")
