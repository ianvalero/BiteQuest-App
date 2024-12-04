from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.db.models import Q
from .models import Restaurant, Category
from .forms import RestaurantForm

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'

    def get(self, request):
        categories_list = Category.objects.all()
        restaurant_list = Restaurant.objects.all()
        context = {'categories_list': categories_list, 'restaurant_list': restaurant_list}
        return render(request, self.template_name, context)

    def post(self, request):
        disabled_categories = request.POST.get('disabled_categories', False)
        search = request.POST.get('search', False)
        categories_list = Category.objects.all()
        if not disabled_categories and not search:
            restaurant_list = Restaurant.objects.all()
        else:
            restaurant_list = Restaurant.objects
            if disabled_categories:
                excluded_categories = list(disabled_categories.split(","))
                restaurant_list = restaurant_list.exclude(category__pk__in=excluded_categories)
            if search:
                query = Q(name__icontains=search)
                query.add(Q(description__icontains=search), Q.OR)
                restaurant_list = restaurant_list.filter(query).select_related().distinct()
        context = {
            'categories_list': categories_list,
            'restaurant_list': restaurant_list,
            'search': search,
            'disabled_categories': [] if not disabled_categories else list(map(int, disabled_categories.split(",")))
        }
        return render(request, self.template_name, context)


# class RestaurantCreateView(LoginRequiredMixin):
class RestaurantCreateView(View):
    model = Restaurant
    template = 'restaurants/restaurant_form.html'
    success_url = reverse_lazy('restaurants:restaurant_list')

    def get(self, request):
        form = RestaurantForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = RestaurantForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template, {'form': form})
        restaurant = form.save(False)
        restaurant.owner = self.request.user
        restaurant.slug = slugify(form.cleaned_data['name'])
        restaurant.save()
        form.save_m2m()
        return redirect(self.success_url)
