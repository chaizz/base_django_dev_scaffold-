"""
-------------------------------------------------
    File Name:   prod.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/24 14:55
-------------------------------------------------
    Change Activity:
          2023/3/24 14:55
-------------------------------------------------
"""

import os
from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "NAME": "django-miniapp",
        'USER': os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
