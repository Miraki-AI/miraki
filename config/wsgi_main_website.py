# wsgi_main_website.py
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.public")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()