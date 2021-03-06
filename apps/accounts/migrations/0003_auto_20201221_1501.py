# Generated by Django 3.1.4 on 2020-12-21 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0002_ingredient_alocholic'),
        ('accounts', '0002_user_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='inventory',
            field=models.ManyToManyField(blank=True, related_name='users', related_query_name='user', to='ingredients.Ingredient'),
        ),
    ]
