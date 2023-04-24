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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "localhost",
        "PORT": 6033,
        "NAME": "base_django_dev_scaffold",
        'USER': "root",
        "PASSWORD": "PASSWORD",
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://localhost:6379/0",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "password",
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},  # 添加这一行,防止取出的值带有b'' bytes

        }
    },
    'verify_codes': {  # 缓存验证码
        'BACKEND': 'django_redis.cache.RedisCache',  # 缓存后端 Redis
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置多个Redis，写走第一台，读走其他的机器)
        "LOCATION": [
            "redis://localhost:6379/1",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "password",
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},  # 添加这一行,防止取出的值带有b'' bytes

        }
    },

}

# Celery 配置
CELERY_BROKER_URL = "redis://:password@localhost:6379/10"
REDBEAT_REDIS_URL = "redis://:password@localhost:6379/11"

# django allauth 配置
GITHUB_CLIENT_ID = 'xxxxxxxxxxxxx'
GITHUB_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

DINGTALK_KEY = "xxxxxxxxxxxxxxxxxx"
DINGTALK_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
