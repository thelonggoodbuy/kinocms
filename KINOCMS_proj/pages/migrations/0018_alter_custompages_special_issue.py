# Generated by Django 3.2 on 2022-12-28 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_remove_contactcell_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompages',
            name='special_issue',
            field=models.CharField(blank=True, choices=[('about_cinema', 'про кінотеатр'), ('cafe_bar', 'кафе-бар'), ('vip-hall', 'VIP-зала'), ('advertising', 'реклама'), ('childrens_room', 'дитяча кімната'), ('mobile_app', 'мобільний додаток')], max_length=100, null=True),
        ),
    ]
