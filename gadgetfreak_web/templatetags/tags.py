from django import template
from ..forms import LoginForm

register = template.Library()

@register.assignment_tag
def login_form():
    return LoginForm()

@register.filter
def get_subimage_url(dictionary, key):
    return dictionary.get(key).url
