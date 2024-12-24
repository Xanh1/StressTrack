from django.contrib import admin
from .models import CustomUser, Task, Question, Course, Answer, Test, Team

admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Course)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Team)