# Generated by Django 3.2 on 2022-10-09 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_auto_20221009_1211'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompages',
            name='image_galery',
            field=models.ManyToManyField(null=True, to='cinema.Galery'),
        ),
        migrations.AlterField(
            model_name='custompages',
            name='main_image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='custom_page_main_image', to='cinema.galery'),
        ),
        migrations.AlterField(
            model_name='custompages',
            name='seo_block',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='cinema.seoblock'),
        ),
    ]