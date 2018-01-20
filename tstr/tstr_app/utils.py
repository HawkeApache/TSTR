from tstr.tstr_app.models import *


def precise_question_type(q):
    """Check type of question - open or closed"""
    try:
        return q.openquestion
    except AttributeError:
        try:
            return q.closedquestion
        except AttributeError:
            print("Attribute error in precise question type")
