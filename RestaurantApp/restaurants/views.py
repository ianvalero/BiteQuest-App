from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.expressions import Case, When
from django.http.response import Http404, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.db.models import Q, Avg, BooleanField
from django.conf import settings
from .models import Restaurant, Category, Comment, Rating, Favorite
from .forms import RestaurantForm
import os, random

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'

    def get(self, request):
        categories_list = Category.objects.all()
        context = {
            'categories_list': categories_list
        }
        return render(request, self.template_name, context)

    def post(self, request):
        disabled_categories = request.POST.get('disabled_categories', False)
        search = request.POST.get('search', False)
        categories_list = Category.objects.all()
        context = {
            'categories_list': categories_list,
            'search': search,
            'disabled_categories': [] if not disabled_categories else list(map(int, disabled_categories.split(",")))
        }
        return render(request, self.template_name, context)

@require_POST
def get_restaurants(request):
    disabled_categories = request.POST.get('disabled_categories', False)
    search = request.POST.get('search', False)
    page_number = request.GET.get('page', 1)

    if not disabled_categories and not search:
        restaurant_list = Restaurant.objects.annotate(avg_rating=Avg('rating__score'))
    else:
        restaurant_list = Restaurant.objects

        if disabled_categories:
            excluded_categories = list(disabled_categories.split(","))
            restaurant_list = restaurant_list.exclude(category__pk__in=excluded_categories)

        if search:
            query = Q(name__icontains=search)
            query.add(Q(description__icontains=search), Q.OR)
            restaurant_list = restaurant_list.filter(query).select_related().distinct()
        restaurant_list = restaurant_list.annotate(avg_rating=Avg('rating__score'))

    favorite_list = []
    if request.user.is_authenticated:
        favorite_list = Favorite.objects.filter(
            user=request.user,
            restaurant__in=restaurant_list.values_list('id', flat=True)
        ).values_list('restaurant', flat=True)

    restaurant_list = restaurant_list.annotate(
        is_favorite=Case(
            When(id__in=favorite_list, then=True),
            default=False,
            output_field=BooleanField()
        )
    ).order_by('-is_favorite', '-avg_rating')

    restaurant_paginator = Paginator(restaurant_list, per_page=10)
    restaurant_list = restaurant_paginator.get_page(page_number)

    data = {
        'restaurant_list': restaurant_list,
        'favorite_list': favorite_list,
        'search': search,
        'page': int(page_number) + 1,
        'has_more': restaurant_list.has_next()
    }
    return render(request, 'restaurants/snippet/_restaurant_list.html', data)

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/restaurant_detail.html'

    def get(self, request, slug):
        try:
            restaurant = get_object_or_404(Restaurant.objects.annotate(avg_rating=Avg('rating__score')), slug=slug)
            user_raiting = None
            favorite = False
            page_number = request.GET.get('page', 1)
            if request.user.is_authenticated:
                user_raiting = Rating.objects.filter(restaurant=restaurant, user=request.user).first()
                favorite = True if Favorite.objects.filter(restaurant=restaurant, user=request.user).first() else False
            comments = Comment.objects.filter(restaurant=restaurant).order_by('-created_at')
            paginator = Paginator(comments, per_page=5)
            page_object = paginator.get_page(page_number)
            context = {
                'restaurant': restaurant,
                'user_raiting': getattr(user_raiting,'score', 0),
                'favorite': favorite,
                'comments_list': page_object,
                'page_number': page_number,
                'paginator': list(paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1,))
            }
            return render(request, self.template_name, context)
        except Restaurant.DoesNotExist:
            raise Http404("Restaurant does not exist")

class RestaurantCreateView(View, LoginRequiredMixin):
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
        print(form.cleaned_data['category'].id)
        category_images_dir = os.path.join(settings.BASE_DIR, 'media', 'category_images', str(form.cleaned_data['category'].id))
        restaurant = form.save(False)
        restaurant.image = f"category_images/{str(form.cleaned_data['category'].id)}/{random.choice(os.listdir(category_images_dir))}"
        restaurant.owner = self.request.user
        restaurant.slug = slugify(form.cleaned_data['name'])
        restaurant.save()
        form.save_m2m()
        return redirect(self.success_url)

class RestaurantUpdateView(View, LoginRequiredMixin):
    model = Restaurant
    template = 'restaurants/restaurant_form.html'
    success_url = reverse_lazy('restaurants:restaurant_list')

    def get(self, request):
        form = RestaurantForm()
        return render(request, self.template, {'form': form})

class RestaurantDeleteView(View, LoginRequiredMixin):
    model = Restaurant
    template = 'restaurants/restaurant_form.html'
    success_url = reverse_lazy('restaurants:restaurant_list')

    def get(self, request):
        form = RestaurantForm()
        return render(request, self.template, {'form': form})

class RestaurantCommentCreateView(View, LoginRequiredMixin):
    model = Comment
    def post(self, request, slug):
        restaurant = get_object_or_404(Restaurant, slug=slug)
        success_url = reverse_lazy('restaurants:restaurant_detail', args=[slug])
        comment = Comment(text=request.POST['comment'], restaurant=restaurant, owner=request.user)
        comment.save()
        return redirect(success_url)

class RestaurantCommentDeleteView(View, LoginRequiredMixin):
    model = Comment
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        success_url = reverse_lazy('restaurants:restaurant_detail', args=[self.object.restaurant.slug])

class RestaurantRateView(View, LoginRequiredMixin):
    model = Rating
    def post(self, request, slug):
        restaurant = get_object_or_404(Restaurant, slug=slug)
        user_raiting = Rating.objects.filter(restaurant=restaurant, user=request.user).first()
        if user_raiting:
            user_raiting.score = request.POST['score']
        else:
            user_raiting = Rating(restaurant=restaurant, user=request.user, score=request.POST['score'])
        user_raiting.save()
        return HttpResponse()

class RestaurantToggleFavoriteView(View, LoginRequiredMixin):
    model = Favorite
    def post(self, request, slug):
        restaurant = get_object_or_404(Restaurant, slug=slug)
        favorite, created = Favorite.objects.get_or_create(restaurant=restaurant, user=request.user)
        if not created:
            favorite.delete()
            return JsonResponse({'favorited': False})
        return JsonResponse({'favorited': True})