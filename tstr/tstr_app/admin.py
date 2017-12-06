from django.contrib import admin

# Register your models here.
from tstr.tstr_app.models import Student, OpenQuestion, Test, Group, ClosedQuestion, Answer, WrapWordQuestion

admin.site.register(Student)
admin.site.register(OpenQuestion)
admin.site.register(Test)
admin.site.register(Group)
admin.site.register(ClosedQuestion)
admin.site.register(Answer)
admin.site.register(WrapWordQuestion)



