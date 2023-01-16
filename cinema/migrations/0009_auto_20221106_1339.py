# Generated by Django 3.2 on 2022-11-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0008_auto_20221026_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='conditions_cinema_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cinema',
            name='conditions_cinema_uk',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cinema',
            name='description_cinema_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cinema',
            name='description_cinema_uk',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cinema',
            name='title_cinema_ru',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='cinema',
            name='title_cinema_uk',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='cinemahall',
            name='cinema_hall_name_ru',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='cinemahall',
            name='cinema_hall_name_uk',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='cinemahall',
            name='description_cinema_hall_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cinemahall',
            name='description_cinema_hall_uk',
            field=models.TextField(null=True),
        ),
    ]