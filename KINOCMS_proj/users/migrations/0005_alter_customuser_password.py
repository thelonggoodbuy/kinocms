# Generated by Django 3.2 on 2022-07-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220726_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
