from django.contrib import admin
from .models import *



admin.site.register(CustomUser)
admin.site.register(Mailing)
admin.site.register(MailingStatistic)
admin.site.register(Ticket)