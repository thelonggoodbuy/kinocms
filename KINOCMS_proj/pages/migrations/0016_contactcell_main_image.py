# Generated by Django 3.2 on 2022-12-14 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_alter_contactcell_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactcell',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
