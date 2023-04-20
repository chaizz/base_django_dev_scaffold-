"""
-------------------------------------------------
    File Name:   celery.py
    Description: 
        
    Author:      chaizz
    Date:        2023/4/20 14:51
-------------------------------------------------
    Change Activity:
          2023/4/20 14:51
-------------------------------------------------
"""
import os

from celery import Celery
from celery import platforms

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base_django_dev_scaffold.settings.dev")

app = Celery('base_django_dev_scaffold')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
