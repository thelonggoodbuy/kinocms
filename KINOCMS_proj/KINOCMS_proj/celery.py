import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KINOCMS_proj.settings")
app = Celery("KINOCMS_proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()