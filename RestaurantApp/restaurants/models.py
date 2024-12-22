from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.db.models import UniqueConstraint
from .validators import *

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.FileField(upload_to='category_icons/', validators=[validate_icon])

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

def category_image_path(instance, filename):
    return f'category_images/{instance.category.id}/{filename}'

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=category_image_path)

    def __str__(self):
        return f'{self.category.name} image'

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=13)
    link = models.URLField(max_length=500, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_restaurants')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Favorite',
                                       related_name='favorite_restaurant')
    ratings = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Rating', name='rating_restaurant')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    slug = models.SlugField(max_length=100, default='', null=False)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField(max_length=500, validators=[
        MinLengthValidator(limit_value=3, message='Comment must be greater than 3 characters')
    ])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text if len(self.text) < 25 else f'{self.text[:22]}...'

class Favorite(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites_users')

    def Meta(self):
        constraints = UniqueConstraint(fields=['restaurant', 'user'], name='unique_favorite')

    def __str__(self) -> str:
        return f'{self.user.username} likes {self.restaurant.name}'

class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_users')
    score = models.IntegerField(validators=[
        MinValueValidator(limit_value=0),
        MaxValueValidator(limit_value=5)
    ])

    def Meta(self):
        constraints = [
            UniqueConstraint(fields=['restaurant', 'user'], name='unique_rating')
        ]

    def __str__(self) -> str:
        return f'{self.user.username} rated {self.restaurant.name} with {self.score} stars'