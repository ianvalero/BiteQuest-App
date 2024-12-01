from django.contrib import admin
from .models import Restaurant, Category

# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category)