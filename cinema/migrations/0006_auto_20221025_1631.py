# Generated by Django 3.2 on 2022-10-25 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_auto_20221025_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='description_movie_de',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='description_movie_en',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='description_movie_ru',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='description_movie_uk',
        ),
    ]