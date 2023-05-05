import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codio_omdb.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations

configurations.setup()

app = Celery("codio_omdb")
app.config_from_object("django.conf:settings", namespace="CELERY") # prefix (broker_url -> CELERY_BROKER_URL)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)			# look for tasks in tasks.py and models.py in all INSTALLED_APPS
