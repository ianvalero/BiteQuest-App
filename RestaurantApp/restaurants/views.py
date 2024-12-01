from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Restaurant, Category
from .forms import RestaurantForm

class RestaurantListView(ListView):
    model = Restaurant

    def get_context_data(self):
        categories_list = Category.objects.all()
        restaurant_list = Restaurant.objects.all()
        context = {'categories_list': categories_list, 'restaurant_list': restaurant_list}
        return context


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
