# Generated by Django 3.2 on 2022-08-27 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_alter_bannercell_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highestbannerwithtimescrolling',
            name='on_of_status',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
