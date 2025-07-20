from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
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

def temp_home(request):
    """Temporary home page"""
    # Try to serve the static coming_soon.html file
    try:
        with open(os.path.join(settings.BASE_DIR, 'static', 'coming_soon.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type="text/html")
    except:
        # Fallback to a simple message
        return HttpResponse(
            "<h1>سكن طالب</h1><p>نعمل على تجهيز الموقع. يرجى العودة لاحقًا.</p>",
            content_type="text/html"
        )