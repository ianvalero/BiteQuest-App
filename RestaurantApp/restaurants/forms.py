from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "description", "category", "address", "phone_number",
                  "link", "image"]
        labels = {
            "phone_number": _("Phone number")
        }