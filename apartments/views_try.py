from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os

def try_home(request):
    """
    محاولة عرض الصفحة الرئيسية الأصلية مع التعامل مع الأخطاء
    """
    try:
        # محاولة استيراد home من apartments.views
        from apartments.views import home
        return home(request)
    except Exception as e:
        # في حالة حدوث خطأ، عرض الصفحة البديلة
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>سكن طالب</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Tajawal', sans-serif;
                    background-color: #f8f9fa;
                }
                .hero {
                    background-color: #dc3545;
                    color: white;
                    padding: 4rem 0;
                    margin-bottom: 2rem;
                }
                .feature-card {
                    border: none;
                    border-radius: 10px;
                    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                    transition: transform 0.3s;
                    margin-bottom: 2rem;
                }
                .feature-card:hover {
                    transform: translateY(-5px);
                }
                .feature-icon {
                    font-size: 2.5rem;
                    color: #dc3545;
                    margin-bottom: 1rem;
                }
                .footer {
                    background-color: #343a40;
                    color: white;
                    padding: 2rem 0;
                    margin-top: 3rem;
                }
                .footer a {
                    color: rgba(255, 255, 255, 0.8);
                    text-decoration: none;
                }
                .footer a:hover {
                    color: white;
                }
            </style>
        </head>
        <body>
            <!-- Navbar -->
            <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
                <div class="container">
                    <a class="navbar-brand" href="/">سكن طالب</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav me-auto">
                            <li class="nav-item">
                                <a class="nav-link active" href="/">الرئيسية</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/apartments/">استكشف الشقق</a>
                            </li>
                        </ul>
                        <ul class="navbar-nav">
                            <li class="nav-item">
                                <a class="nav-link" href="/admin/"><i class="fas fa-sign-in-alt me-1"></i> تسجيل الدخول</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link btn btn-primary text-white px-3 mx-2" href="/admin/">التسجيل</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>

            <!-- Hero Section -->
            <div class="hero">
                <div class="container text-center">
                    <h1 class="display-4 fw-bold">ابحث عن سكن قريب من جامعتك</h1>
                    <p class="lead">منصة متكاملة للطلاب للبحث عن سكن قريب من جامعاتهم، ولمالكي العقارات لعرض شققهم للإيجار.</p>
                    <div class="mt-4">
                        <a href="/admin/" class="btn btn-light btn-lg me-2">ابدأ البحث</a>
                        <a href="/admin/" class="btn btn-outline-light btn-lg">أضف عقارك</a>
                    </div>
                </div>
            </div>

            <!-- Features Section -->
            <div class="container">
                <h2 class="text-center mb-5">مميزات سكن طالب</h2>
                <div class="row">
                    <div class="col-md-4">
                        <div class="card feature-card p-4 text-center">
                            <div class="feature-icon">
                                <i class="fas fa-search"></i>
                            </div>
                            <h4>بحث متقدم</h4>
                            <p>ابحث عن الشقق حسب معايير مختلفة (الجامعة، السعر، نوع السكن، إلخ)</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card feature-card p-4 text-center">
                            <div class="feature-icon">
                                <i class="fas fa-home"></i>
                            </div>
                            <h4>تنوع السكن</h4>
                            <p>شقق كاملة، غرف مشتركة، أو أسرّة في غرف مشتركة</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card feature-card p-4 text-center">
                            <div class="feature-icon">
                                <i class="fas fa-calendar-check"></i>
                            </div>
                            <h4>حجز مباشر</h4>
                            <p>احجز سكنك مباشرة من خلال المنصة وتواصل مع المالك</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <footer class="footer">
                <div class="container">
                    <div class="row">
                        <div class="col-md-3">
                            <h5>سكن طالب</h5>
                            <p>منصة لمساعدة طلاب الجامعات في العثور على سكن مناسب بالقرب من جامعاتهم.</p>
                        </div>
                        <div class="col-md-3">
                            <h5>استكشف</h5>
                            <ul class="list-unstyled">
                                <li><a href="/">الرئيسية</a></li>
                                <li><a href="/apartments/">الشقق</a></li>
                                <li><a href="/admin/">تسجيل الدخول</a></li>
                            </ul>
                        </div>
                        <div class="col-md-3">
                            <h5>المساعدة</h5>
                            <ul class="list-unstyled">
                                <li><a href="#">الأسئلة الشائعة</a></li>
                                <li><a href="#">سياسة الخصوصية</a></li>
                                <li><a href="#">شروط الاستخدام</a></li>
                            </ul>
                        </div>
                        <div class="col-md-3">
                            <h5>تواصل معنا</h5>
                            <p>
                                <i class="fas fa-envelope me-2"></i> info@studenthousing.com
                            </p>
                        </div>
                    </div>
                    <hr class="my-4">
                    <div class="text-center">
                        <p>&copy; 2025 سكن طالب. جميع الحقوق محفوظة.</p>
                    </div>
                </div>
            </footer>

            <!-- Bootstrap JS -->
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
        return HttpResponse(html, content_type="text/html; charset=utf-8")