# Generated by Django 3.2 on 2022-10-23 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_alter_custompages_image_galery'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_undeleteble',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mainpage',
            name='is_undeleteble',
            field=models.BooleanField(default=True),
        ),
    ]
