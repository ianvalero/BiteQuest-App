# Generated by Django 5.1.3 on 2024-11-24 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_alter_category_options_alter_category_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(upload_to='restaurant_icons/'),
        ),
    ]
