from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from .models import Restaurant, Category, CategoryImage


# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_display')
    inlines = [CategoryImageInline]

    def icon_display(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.icon.url)
        return "No Icon"
    icon_display.short_description = 'Icon'

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)