from tstr.tstr_app.models import *


def recalculate_test_results():
    for answer in Answer.objects.all():
        if answer.is_correct:
            tr = TestResult.objects.get(student=answer.student, test=answer.test)
            tr.score = int(tr.score) + 1
            tr.save()
