# Generated by Django 3.2 on 2022-10-26 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_auto_20221025_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='title_movie_de',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='title_movie_en',
        ),
    ]
