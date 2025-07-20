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

from django.template.loader import render_to_string
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
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Tajawal', sans-serif;
                background-color: #f8f9fa;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .coming-soon {
                text-align: center;
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
            .countdown {
                font-size: 2rem;
                margin: 2rem 0;
                color: #343a40;
            }
            .social-icons {
                margin-top: 2rem;
            }
            .social-icons a {
                color: #6c757d;
                font-size: 1.5rem;
                margin: 0 0.5rem;
                transition: color 0.3s;
            }
            .social-icons a:hover {
                color: #dc3545;
            }
        </style>
    </head>
    <body>
        <div class="coming-soon">
            <div class="logo">سكن طالب</div>
            <h2>قريبًا</h2>
            <p class="lead">نعمل على تجهيز الموقع لمساعدة الطلاب في العثور على سكن مناسب بالقرب من جامعاتهم.</p>
            <div class="countdown" id="countdown">00:00:00</div>
            <p>تابعنا للحصول على آخر التحديثات</p>
            <div class="social-icons">
                <a href="#"><i class="fab fa-facebook"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-instagram"></i></a>
            </div>
            <div class="mt-4">
                <a href="/admin/" class="btn btn-outline-secondary">تسجيل الدخول للإدارة</a>
            </div>
        </div>
        
        <script>
            // عد تنازلي لمدة 24 ساعة
            const countDownDate = new Date().getTime() + (24 * 60 * 60 * 1000);
            
            const countdown = setInterval(function() {
                const now = new Date().getTime();
                const distance = countDownDate - now;
                
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
                document.getElementById("countdown").innerHTML = 
                    hours.toString().padStart(2, '0') + ":" +
                    minutes.toString().padStart(2, '0') + ":" +
                    seconds.toString().padStart(2, '0');
                
                if (distance < 0) {
                    clearInterval(countdown);
                    document.getElementById("countdown").innerHTML = "00:00:00";
                }
            }, 1000);
        </script>
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