# Generated by Django 3.1.4 on 2020-12-10 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='is_public',
            new_name='public',
        ),
    ]
