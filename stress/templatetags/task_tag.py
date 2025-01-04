from django import template

register = template.Library()

@register.simple_tag
def is_group_assigned_to_test(test, group):
    return group in test.Team.all()