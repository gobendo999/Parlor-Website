"""
ASGI config for beauty_parlor project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_parlor.settings')
application = get_asgi_application()
