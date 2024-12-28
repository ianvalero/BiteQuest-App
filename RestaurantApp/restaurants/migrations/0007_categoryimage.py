# Generated by Django 5.1.3 on 2024-12-21 12:03

import django.db.models.deletion
import restaurants.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_alter_restaurant_image_alter_restaurant_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=restaurants.models.category_image_path)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='restaurants.category')),
            ],
        ),
    ]