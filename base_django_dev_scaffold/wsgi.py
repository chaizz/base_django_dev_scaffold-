"""
WSGI config for base_django_dev_scaffold project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application

from .settings import set_environ

set_environ()

application = get_wsgi_application()
