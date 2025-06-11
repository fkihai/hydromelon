"""
ASGI config for hydromelon project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

load_dotenv()

env = os.getenv('DJANGO_ENV', 'dev')
if env == "prod":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.config.prod'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.config.dev'

application = get_asgi_application()

