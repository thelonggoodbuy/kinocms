# Generated by Django 3.2 on 2022-10-18 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_auto_20221018_1101'),
        ('pages', '0004_alter_newsandpromotions_title_news_or_promo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompages',
            name='image_galery',
            field=models.ManyToManyField(to='cinema.Galery'),
        ),
    ]
