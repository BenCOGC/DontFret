"""
WSGI config for dontfret project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

"""
Title: dontfret:wsgi
Author: Ben Frame
Date: 06/04/2020
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dontfret.settings')

application = get_wsgi_application()
