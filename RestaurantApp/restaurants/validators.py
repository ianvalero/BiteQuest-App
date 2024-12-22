import magic
from django.core.exceptions import ValidationError

def validate_icon(icon):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(icon.read())
    icon.seek(0) # Volvemos al principio del archivo despeus de leer
    if file_type != 'image/svg+xml':
        raise ValidationError("Only SVG files are allowed.")