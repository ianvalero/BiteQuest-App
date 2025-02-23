from django.contrib.messages import success
from django.urls import path, reverse_lazy
from . import views

app_name='restaurants'
urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurant/<slug:slug>', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurant/create',
         views.RestaurantCreateView.as_view(),
         name='restaurant_create'),
    path('restaurant/<slug:slug>/update',
         views.RestaurantUpdateView.as_view(success_url=reverse_lazy('restaurant_list')),
         name='restaurant_update'),
    path('restaurant/<slug:slug>/delete',
         views.RestaurantDeleteView.as_view(success_url=reverse_lazy('restaurant_list')),
         name='restaurant_delete'),
    path('restaurant/<slug:slug>/restaurant-toggle-favorite',
         views.RestaurantToggleFavoriteView.as_view(),
         name='restaurant_toggle_favorite'),
    path('restaurant/<slug:slug>/comment',
         views.RestaurantCommentCreateView.as_view(),
         name='restaurant_comment_create'),
    path('restaurant/comment/<int:pk>/delete',
         views.RestaurantCommentDeleteView.as_view(),
         name='restaurant_comment_delete'),
    path('restaurant/<slug:slug>/rate',
         views.RestaurantRateView.as_view(),
         name='restaurant_rate'),
]