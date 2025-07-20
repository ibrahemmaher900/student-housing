from django.http import HttpResponse
from django.conf import settings
import sys
import os
import django

def debug_view(request):
    """View for debugging server issues"""
    debug_info = [
        f"Python version: {sys.version}",
        f"Django version: {django.__version__}",
        f"Debug mode: {settings.DEBUG}",
        f"Base directory: {settings.BASE_DIR}",
        f"Database engine: {settings.DATABASES['default']['ENGINE']}",
        f"Static root: {settings.STATIC_ROOT}",
        f"Media root: {settings.MEDIA_ROOT}",
        f"Installed apps: {', '.join(settings.INSTALLED_APPS)}",
        f"Middleware: {', '.join([str(m) for m in settings.MIDDLEWARE])}",
        f"Environment variables: {list(os.environ.keys())}",
    ]
    
    return HttpResponse("<br>".join(debug_info), content_type="text/html")