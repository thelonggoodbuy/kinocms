# Generated by Django 3.2 on 2022-12-14 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_auto_20221126_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactcell',
            name='location',
            field=models.CharField(max_length=1500),
        ),
    ]
