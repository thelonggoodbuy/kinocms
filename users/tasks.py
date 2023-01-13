import json
from celery import shared_task
from django.core.mail import send_mass_mail, get_connection, EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
import time
from users.models import DevicesStatisticCounter
from django.utils.datetime_safe import datetime

from .models import MailingStatistic


@shared_task
def send_mass_templates(email_list, template):


    for email_address in email_list:
        send_mail(
            'Topic',
            None,
            'markus1991kartal@gmail.com',
            (email_address, ),
            fail_silently=False,
            html_message = template
        )

@shared_task
def identify_user_device_task(current_device_type):
    statistic_cell, created = DevicesStatisticCounter.objects.get_or_create(
        date = datetime.now().date(),
        device_type = current_device_type
    )
    statistic_cell.number += 1
    statistic_cell.save()