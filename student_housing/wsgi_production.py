"""
WSGI config for student_housing project in production.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.production')

application = get_wsgi_application()