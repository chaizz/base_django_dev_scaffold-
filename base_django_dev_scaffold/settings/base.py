"""
Django settings for base_django_dev_scaffold project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import logging.config
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b(%nd+g-18%&5(s_ve$6x80xyfi*7sias17r6*dw(fmjhmx353"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "simpleui",
    "django_comment_migrate",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.system.apps.SystemConfig",
    "rest_framework",
    "rest_framework_simplejwt",
    "captcha",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "base_django_dev_scaffold.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "base_django_dev_scaffold.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# rest framework 设置
REST_FRAMEWORK = {
    # 认证
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication', ],

    # 权限
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated', ],

    # 全局配置异常模块
    'EXCEPTION_HANDLER': "utils.c_restframework.c_exception.custom_exception_handler",

    # 修改默认返回JSON的renderer的类
    "DEFAULT_RENDERER_CLASSES": ("utils.c_restframework.c_renderer.custom_renderer",),

    # 全局分页
    'DEFAULT_PAGINATION_CLASS': "utils.c_restframework.c_pagination.MyPageNumberPagination",
    'PAGE_SIZE': 50,  # 这是每页显示的数目

    # 全局接口版本
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",  # 正则形式
    "ALLOWED_VERSIONS": ["v1"],  # 允许的版本
    "VERSION_PARAM": "version",  # 参数
    "DEFAULT_VERSION": "v1",  # 默认版本
}

AUTH_USER_MODEL = "system.Users"

LOGGING_CONFIG = None  # This empties out Django's logging config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s %(levelname)-8s %(asctime)s %(request_id)s  %(process)s --- "
                      "%(lineno)-8s [%(name)s] %(funcName)-24s : %(message)s",
            "log_colors": {
                "DEBUG": "blue",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "request_id": {"()": "log_request_id.filters.RequestIDFilter"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        # Default logger for any logger name
        "": {
            "level": "INFO",
            "handlers": ["console", ],
            "propagate": False,
        },
        # Logger for django server logs with django.server logger name
        "django.server": {
            "level": "DEBUG",
            "handlers": ["console", ],
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING)  # Finally replace our config in python logging

# simple-ui 配置
SIMPLEUI_LOGO = 'https://i.328888.xyz/2023/03/20/Pz1EL.png'  # 去掉默认的系统图标
# 隐藏右侧SimpleUI广告链接和使用分析# 认Logo或换成自己Logo链接
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
# 设置默认主题，指向主题css文件名。Admin Lte风格
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'
# SIMPLEUI_CONFIG = {
#     # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
#     'menu_display': ['系统设置', ],
# }
# 系统默认的菜单图标，注意key名为菜单上实际显示的名字，不是模型或App名。
# SIMPLEUI_ICON = {
#     '系统设置': 'fa-solid fa-gears',
#     # '用户管理': 'fas fa-user-tie',
#     # '图片管理': 'fa-solid fa-image'
# }


# SIMPLE_JWT 配置

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),  # 认证的标签头，类似jwt token中的jwt
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # 身份验证的授权标头名称
}

AUTHENTICATION_BACKENDS = (
    'utils.c_auth_backend.backend.MyModelBackendBackend',
)

# django simple captcha 配置
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'  # 验证码类型， 简单算术
CAPTCHA_TIMEOUT = 10  # 验证码过期时间，单位：分钟
