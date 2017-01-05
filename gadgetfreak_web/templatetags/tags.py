from django import template
from ..forms import LoginForm

register = template.Library()

@register.assignment_tag
def login_form():
    return LoginForm()
