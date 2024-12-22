from django.contrib.messages import success
from django.urls import path, reverse_lazy
from . import views

app_name='restaurants'
urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('resturant/<slug:slug>', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurant/create',
         views.RestaurantCreateView.as_view(),
         name='restaurant_create'),
    path('restaurant/<slug:slug>/update',
         views.RestaurantUpdateView.as_view(success_url=reverse_lazy('restaurant_list')),
         name='restaurant_update'),
    path('restaurant/<slug:slug>/delete',
         views.RestaurantDeleteView.as_view(success_url=reverse_lazy('restaurant_list')),
         name='restaurant_delete'),
]