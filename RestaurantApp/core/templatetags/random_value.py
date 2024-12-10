from django import template
import random

register = template.Library()

@register.filter
def random_image(path):
    return f"{path}/login{random.randint(1,6)}.svg"