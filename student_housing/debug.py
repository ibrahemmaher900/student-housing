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
    # Return a simple HTML page with proper encoding
    html = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>سكن طالب - قريبًا</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
        <style>
            body {
                font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif;
                background-color: #f8f9fa;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .coming-soon {
                padding: 2rem;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                max-width: 600px;
                width: 90%;
            }
            .logo {
                font-size: 2.5rem;
                font-weight: bold;
                color: #dc3545;
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        <div class="coming-soon">
            <div class="logo">سكن طالب</div>
            <h2>قريبًا</h2>
            <p class="lead">نعمل على تجهيز الموقع لمساعدة الطلاب في العثور على سكن مناسب بالقرب من جامعاتهم.</p>
            <div class="mt-4">
                <a href="/admin/" class="btn btn-outline-secondary">تسجيل الدخول للإدارة</a>
            </div>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html, content_type="text/html; charset=utf-8")