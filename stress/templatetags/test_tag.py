from django import template

register = template.Library()

@register.simple_tag
def is_test_assigned_to_all_students(test, course):
    students = course.students.all()

    for student in students:
        if test not in student.tests.all():
            return False

    return True

@register.simple_tag
def is_test_assigned_to_user(test, user):
    if test in user.tests.all():
        return True
    return False