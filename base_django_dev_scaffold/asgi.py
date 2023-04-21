"""
ASGI config for base_django_dev_scaffold project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application

from .settings import set_environ

set_environ()

application = get_asgi_application()
