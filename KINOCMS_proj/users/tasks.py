import json
from celery import shared_task
from django.core.mail import send_mass_mail, get_connection, EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
import time


# render to string с темплейтом мы перебрасываем в body
@shared_task
def send_mass_templates(email_list, template):
    print(template)
    for email_address in email_list:
        send_mail(
            'Topic_29_09_2022',
            None,
            'markus1991kartal@gmail.com',
            (email_address, ),
            fail_silently=False,
            html_message = template
        )
