"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# application = get_wsgi_application()



"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Standard Django WSGI application
application = get_wsgi_application()

# Define BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Wrap with WhiteNoise to serve static + media
application = WhiteNoise(
    application,
    root=str(BASE_DIR / "staticfiles"),  # static files
    prefix="static/",                     # URL prefix
    autorefresh=False
)

# Add media files
application.add_files(
    str(BASE_DIR / "media"),             # media files
    prefix="media/"
)
