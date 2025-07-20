#!/usr/bin/env python
"""
سكريبت لإنشاء صفحة بديلة مؤقتة
"""
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.conf import settings
import os

def create_temp_home():
    """إنشاء صفحة بديلة مؤقتة"""
    print("جاري إنشاء صفحة بديلة مؤقتة...")
    
    # إنشاء قالب HTML بسيط
    html_content = """
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
    """
    
    # إنشاء ملف HTML في المجلد الثابت
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    with open(os.path.join(static_dir, 'coming_soon.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("تم إنشاء صفحة بديلة مؤقتة في static/coming_soon.html")

if __name__ == "__main__":
    create_temp_home()