"""
WSGI config for carbonara project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carbonara.settings")

SETTINGS_PATH = '/home/carbonara/Carbonara/backend/carbonara/'
ENV_FILE_PATH = os.path.join(SETTINGS_PATH, '.env')
if os.path.exists(ENV_FILE_PATH):
    with open(ENV_FILE_PATH) as f:
        for l in f:
            key, value = l.strip().split('=', 1)
            os.environ[key] = value

application = get_wsgi_application()
