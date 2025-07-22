from django.shortcuts import render
from django.http import HttpResponse

def simple_home(request):
    """صفحة رئيسية مبسطة"""
    try:
        # محاولة استخدام القالب الأصلي
        return render(request, 'apartments/home.html', {})
    except Exception as e:
        # إذا فشل، استخدم صفحة HTML بسيطة
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>سكن طالب</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
            <style>
                body {
                    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
                    background-color: #f8f9fa;
                }
                .hero {
                    background-color: #dc3545;
                    color: white;
                    padding: 4rem 0;
                }
            </style>
        </head>
        <body>
            <div class="hero">
                <div class="container text-center">
                    <h1 class="display-4 fw-bold">سكن طالب</h1>
                    <p class="lead">ابحث عن سكن قريب من جامعتك</p>
                </div>
            </div>
            <div class="container py-5">
                <div class="row">
                    <div class="col-md-12 text-center">
                        <h2>مرحباً بك في موقع سكن طالب</h2>
                        <p>موقع لإيجار الشقق لطلبة الجامعات</p>
                        <a href="/apartments/" class="btn btn-primary">استعرض الشقق</a>
                        <a href="/admin/" class="btn btn-secondary">لوحة الإدارة</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html, content_type="text/html; charset=utf-8")
