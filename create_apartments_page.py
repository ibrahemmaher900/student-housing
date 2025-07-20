#!/usr/bin/env python
"""
سكريبت لإنشاء صفحة بديلة للشقق
"""
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

def create_apartments_page():
    """إنشاء صفحة بديلة للشقق"""
    print("جاري إنشاء صفحة بديلة للشقق...")
    
    # إنشاء قالب HTML بسيط
    html_content = """
from django.shortcuts import render
from django.http import HttpResponse

def apartment_list(request):
    \"\"\"
    صفحة قائمة الشقق البديلة
    \"\"\"
    html = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>قائمة الشقق - سكن طالب</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Tajawal', sans-serif;
                background-color: #f8f9fa;
            }
            .apartment-card {
                border: none;
                border-radius: 10px;
                box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                transition: transform 0.3s;
                margin-bottom: 2rem;
                overflow: hidden;
            }
            .apartment-card:hover {
                transform: translateY(-5px);
            }
            .apartment-img {
                height: 200px;
                object-fit: cover;
            }
            .price {
                font-size: 1.5rem;
                font-weight: bold;
                color: #dc3545;
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
                            <a class="nav-link" href="/">الرئيسية</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/apartments/">استكشف الشقق</a>
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

        <!-- Apartments Section -->
        <div class="container py-5">
            <h1 class="mb-4">قائمة الشقق المتاحة</h1>
            
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="ابحث عن شقة...">
                        <button class="btn btn-primary" type="button"><i class="fas fa-search"></i></button>
                    </div>
                </div>
                <div class="col-md-4">
                    <select class="form-select">
                        <option selected>اختر الجامعة</option>
                        <option>جامعة القاهرة</option>
                        <option>جامعة عين شمس</option>
                        <option>جامعة الإسكندرية</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <select class="form-select">
                        <option selected>نوع السكن</option>
                        <option>شقة كاملة</option>
                        <option>غرفة مشتركة</option>
                        <option>سرير في غرفة مشتركة</option>
                    </select>
                </div>
            </div>
            
            <div class="row">
                <!-- Apartment 1 -->
                <div class="col-md-4">
                    <div class="card apartment-card">
                        <img src="https://via.placeholder.com/300x200?text=شقة+فاخرة" class="card-img-top apartment-img" alt="شقة فاخرة">
                        <div class="card-body">
                            <h5 class="card-title">شقة فاخرة قرب جامعة القاهرة</h5>
                            <p class="card-text text-muted">الجيزة، القاهرة</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="price">2500 ج.م/شهر</span>
                                <a href="#" class="btn btn-outline-primary">التفاصيل</a>
                            </div>
                        </div>
                        <div class="card-footer bg-white">
                            <div class="d-flex justify-content-between text-muted">
                                <small><i class="fas fa-bed me-1"></i> 3 غرف</small>
                                <small><i class="fas fa-bath me-1"></i> 2 حمام</small>
                                <small><i class="fas fa-ruler-combined me-1"></i> 120 م²</small>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Apartment 2 -->
                <div class="col-md-4">
                    <div class="card apartment-card">
                        <img src="https://via.placeholder.com/300x200?text=غرفة+مشتركة" class="card-img-top apartment-img" alt="غرفة مشتركة">
                        <div class="card-body">
                            <h5 class="card-title">غرفة مشتركة قرب جامعة عين شمس</h5>
                            <p class="card-text text-muted">مدينة نصر، القاهرة</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="price">1200 ج.م/شهر</span>
                                <a href="#" class="btn btn-outline-primary">التفاصيل</a>
                            </div>
                        </div>
                        <div class="card-footer bg-white">
                            <div class="d-flex justify-content-between text-muted">
                                <small><i class="fas fa-bed me-1"></i> 1 غرفة</small>
                                <small><i class="fas fa-bath me-1"></i> مشترك</small>
                                <small><i class="fas fa-ruler-combined me-1"></i> 20 م²</small>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Apartment 3 -->
                <div class="col-md-4">
                    <div class="card apartment-card">
                        <img src="https://via.placeholder.com/300x200?text=شقة+مفروشة" class="card-img-top apartment-img" alt="شقة مفروشة">
                        <div class="card-body">
                            <h5 class="card-title">شقة مفروشة في الإسكندرية</h5>
                            <p class="card-text text-muted">سموحة، الإسكندرية</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="price">3000 ج.م/شهر</span>
                                <a href="#" class="btn btn-outline-primary">التفاصيل</a>
                            </div>
                        </div>
                        <div class="card-footer bg-white">
                            <div class="d-flex justify-content-between text-muted">
                                <small><i class="fas fa-bed me-1"></i> 2 غرف</small>
                                <small><i class="fas fa-bath me-1"></i> 1 حمام</small>
                                <small><i class="fas fa-ruler-combined me-1"></i> 90 م²</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Pagination -->
            <nav class="mt-4">
                <ul class="pagination justify-content-center">
                    <li class="page-item disabled">
                        <a class="page-link" href="#" tabindex="-1">السابق</a>
                    </li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item">
                        <a class="page-link" href="#">التالي</a>
                    </li>
                </ul>
            </nav>
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
    '''
    return HttpResponse(html, content_type="text/html; charset=utf-8")

def apartment_detail(request, apartment_id):
    \"\"\"
    صفحة تفاصيل الشقة البديلة
    \"\"\"
    html = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تفاصيل الشقة - سكن طالب</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Tajawal', sans-serif;
                background-color: #f8f9fa;
            }
            .apartment-image {
                height: 400px;
                object-fit: cover;
                border-radius: 10px;
            }
            .price {
                font-size: 2rem;
                font-weight: bold;
                color: #dc3545;
            }
            .feature-icon {
                color: #28a745;
                margin-right: 5px;
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
                            <a class="nav-link" href="/">الرئيسية</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/apartments/">استكشف الشقق</a>
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

        <!-- Apartment Detail Section -->
        <div class="container py-5">
            <div class="row">
                <div class="col-md-8">
                    <img src="https://via.placeholder.com/800x400?text=شقة+فاخرة" class="img-fluid apartment-image mb-4" alt="شقة فاخرة">
                    
                    <h1 class="mb-3">شقة فاخرة قرب جامعة القاهرة</h1>
                    <p class="text-muted mb-4"><i class="fas fa-map-marker-alt me-2"></i>الجيزة، القاهرة</p>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">وصف الشقة</h5>
                            <p class="card-text">شقة مفروشة بالكامل قريبة من الجامعة، مناسبة للطلاب. تتميز بموقعها المميز على بعد 10 دقائق سيراً من جامعة القاهرة. الشقة مجهزة بالكامل وتشمل جميع الأثاث والأجهزة الكهربائية اللازمة.</p>
                            <p class="card-text">تتكون الشقة من 3 غرف نوم وصالة واسعة ومطبخ مجهز و2 حمام. جميع الغرف مفروشة بالكامل وتشمل أسرّة ومكاتب للدراسة وخزائن ملابس.</p>
                        </div>
                    </div>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">المميزات</h5>
                            <div class="row">
                                <div class="col-md-6">
                                    <ul class="list-unstyled">
                                        <li class="mb-2"><i class="fas fa-wifi feature-icon"></i> إنترنت واي فاي</li>
                                        <li class="mb-2"><i class="fas fa-snowflake feature-icon"></i> تكييف</li>
                                        <li class="mb-2"><i class="fas fa-utensils feature-icon"></i> مطبخ مجهز</li>
                                        <li class="mb-2"><i class="fas fa-tshirt feature-icon"></i> غسالة ملابس</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <ul class="list-unstyled">
                                        <li class="mb-2"><i class="fas fa-couch feature-icon"></i> مفروشة بالكامل</li>
                                        <li class="mb-2"><i class="fas fa-bath feature-icon"></i> حمام خاص</li>
                                        <li class="mb-2"><i class="fas fa-car feature-icon"></i> موقف سيارات</li>
                                        <li class="mb-2"><i class="fas fa-door-open feature-icon"></i> شرفة</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">التفاصيل</h5>
                            <div class="row">
                                <div class="col-md-6">
                                    <ul class="list-unstyled">
                                        <li class="mb-2"><strong>المساحة:</strong> 120 م²</li>
                                        <li class="mb-2"><strong>عدد الغرف:</strong> 3</li>
                                        <li class="mb-2"><strong>عدد الحمامات:</strong> 2</li>
                                        <li class="mb-2"><strong>الطابق:</strong> الثاني</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <ul class="list-unstyled">
                                        <li class="mb-2"><strong>نوع السكن:</strong> شقة كاملة</li>
                                        <li class="mb-2"><strong>مناسب لـ:</strong> طلاب وطالبات</li>
                                        <li class="mb-2"><strong>المسافة للجامعة:</strong> 500 متر</li>
                                        <li class="mb-2"><strong>وقت المشي للجامعة:</strong> 10 دقائق</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card mb-4 sticky-top" style="top: 20px;">
                        <div class="card-body">
                            <h5 class="card-title">تفاصيل الإيجار</h5>
                            <div class="price mb-3">2500 ج.م/شهر</div>
                            <p class="text-muted mb-3">التأمين: 2500 ج.م</p>
                            <p class="text-muted mb-3">الفواتير: مشمولة في الإيجار</p>
                            <p class="text-muted mb-3">طريقة الدفع: شهري</p>
                            <hr>
                            <h5 class="card-title">معلومات الاتصال</h5>
                            <p><strong>المالك:</strong> أحمد محمد</p>
                            <p><strong>الهاتف:</strong> 01012345678</p>
                            <p><strong>واتساب:</strong> متاح</p>
                            <div class="d-grid gap-2">
                                <a href="#" class="btn btn-primary"><i class="fas fa-phone-alt me-2"></i>اتصل الآن</a>
                                <a href="#" class="btn btn-success"><i class="fab fa-whatsapp me-2"></i>تواصل عبر واتساب</a>
                                <a href="#" class="btn btn-outline-primary"><i class="far fa-heart me-2"></i>أضف للمفضلة</a>
                            </div>
                        </div>
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
    '''
    return HttpResponse(html, content_type="text/html; charset=utf-8")
    """
    
    # كتابة الملف
    with open(os.path.join('apartments', 'views_static.py'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("تم إنشاء صفحة بديلة للشقق بنجاح")

if __name__ == "__main__":
    create_apartments_page()