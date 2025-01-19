from django import template
from django.conf import settings
import random, os

register = template.Library()

login_images_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'login')
login_images = len(os.listdir(login_images_dir))

@register.filter
def random_image(path):
    return f"{path}/login{random.randint(1, login_images)}.svg"

@register.filter
def is_integer(value):
    return isinstance(value, int)