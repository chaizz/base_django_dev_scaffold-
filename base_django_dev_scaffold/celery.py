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
from celery import Celery

from .settings import set_environ

# Set the default Django settings module for the 'celery' program.

# 指定 当前的配置文件

set_environ()

app = Celery('base_django_dev_scaffold')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
