# Generated by Django 3.2 on 2022-09-05 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_alter_galery_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='main_image',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cinema.galery'),
        ),
    ]
