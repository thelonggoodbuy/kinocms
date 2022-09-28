import json
from celery import shared_task
from django.core.mail import send_mass_mail, get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
import time



@shared_task
def send_mass_templates(email_list, template):
    connection = get_connection()
    connection.open()
    text_content = "..."
    for email in email_list:
        # time.sleep(5)
        msg = EmailMultiAlternatives('topic!', text_content, 'markus1991kartal@gmail.com', (email, ), connection=connection)
        msg.attach_alternative(template, 'text/html')
        msg.send()

    connection.close()