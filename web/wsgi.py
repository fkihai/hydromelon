"""
WSGI config for hydromelon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv()

env = os.getenv('DJANGO_ENV', 'dev')
if env == "prod":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.config.prod'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.config.dev'

application = get_wsgi_application()

