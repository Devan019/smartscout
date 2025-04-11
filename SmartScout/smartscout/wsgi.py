"""
WSGI config for smartscout project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import collections
import collections.abc
collections.Sequence = collections.abc.Sequence
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartscout.settings')

application = get_wsgi_application()
app = application