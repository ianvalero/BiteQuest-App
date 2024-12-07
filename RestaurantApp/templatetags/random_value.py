from django import template
import random

register = template.Library()

@register.filter
def random_number():
    return random.randint(1,7)