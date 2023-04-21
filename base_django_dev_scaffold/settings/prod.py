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


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv("REDIS_PASSWORD")
        }
    }
}