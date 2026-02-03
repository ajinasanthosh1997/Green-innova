from django import template

register = template.Library()

@register.filter(name='length_is')
def length_is(value, arg):
    return len(value) == int(arg)  # Fixes Django 5.1+ issue :cite[5]