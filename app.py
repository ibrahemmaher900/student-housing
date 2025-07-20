from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
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
            .feature-card {
                border-radius: 10px;
                box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                margin-bottom: 2rem;
            }
            .footer {
                background-color: #343a40;
                color: white;
                padding: 2rem 0;
                margin-top: 3rem;
            }
        </style>
    </head>
    <body>
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
                            <a class="nav-link" href="/apartments">الشقق</a>
                        </li>
                    </ul>
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/login">تسجيل الدخول</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="hero">
            <div class="container text-center">
                <h1 class="display-4 fw-bold">ابحث عن سكن قريب من جامعتك</h1>
                <p class="lead">منصة متكاملة للطلاب للبحث عن سكن قريب من جامعاتهم</p>
                <div class="mt-4">
                    <a href="/apartments" class="btn btn-light btn-lg me-2">ابدأ البحث</a>
                    <a href="/add" class="btn btn-outline-light btn-lg">أضف عقارك</a>
                </div>
            </div>
        </div>

        <div class="container py-5">
            <h2 class="text-center mb-5">مميزات سكن طالب</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="card feature-card p-4 text-center">
                        <h4>بحث متقدم</h4>
                        <p>ابحث عن الشقق حسب معايير مختلفة (الجامعة، السعر، نوع السكن)</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card feature-card p-4 text-center">
                        <h4>تنوع السكن</h4>
                        <p>شقق كاملة، غرف مشتركة، أو أسرّة في غرف مشتركة</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card feature-card p-4 text-center">
                        <h4>حجز مباشر</h4>
                        <p>احجز سكنك مباشرة من خلال المنصة وتواصل مع المالك</p>
                    </div>
                </div>
            </div>
        </div>

        <footer class="footer">
            <div class="container text-center">
                <p>&copy; 2025 سكن طالب. جميع الحقوق محفوظة.</p>
            </div>
        </footer>
    </body>
    </html>
    """
    return html

@app.route('/apartments')
def apartments():
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>الشقق - سكن طالب</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
        <style>
            body {
                font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
                background-color: #f8f9fa;
            }
            .apartment-card {
                border-radius: 10px;
                box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                margin-bottom: 2rem;
            }
            .footer {
                background-color: #343a40;
                color: white;
                padding: 2rem 0;
                margin-top: 3rem;
            }
        </style>
    </head>
    <body>
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
                            <a class="nav-link active" href="/apartments">الشقق</a>
                        </li>
                    </ul>
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/login">تسجيل الدخول</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="container py-5">
            <h1 class="mb-4">قائمة الشقق المتاحة</h1>
            
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="ابحث عن شقة...">
                        <button class="btn btn-primary" type="button">بحث</button>
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
                <div class="col-md-4">
                    <div class="card apartment-card">
                        <img src="https://via.placeholder.com/300x200?text=شقة+فاخرة" class="card-img-top" alt="شقة فاخرة">
                        <div class="card-body">
                            <h5 class="card-title">شقة فاخرة قرب جامعة القاهرة</h5>
                            <p class="card-text text-muted">الجيزة، القاهرة</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="fw-bold">2500 ج.م/شهر</span>
                                <a href="/apartments/1" class="btn btn-outline-primary">التفاصيل</a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card apartment-card">
                        <img src="https://via.placeholder.com/300x200?text=غرفة+مشتركة" class="card-img-top" alt="غرفة مشتركة">
                        <div class="card-body">
                            <h5 class="card-title">غرفة مشتركة قرب جامعة عين شمس</h5>
                            <p class="card-text text-muted">مدينة نصر، القاهرة</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="fw-bold">1200 ج.م/شهر</span>
                                <a href="/apartments/2" class="btn btn-outline-primary">التفاصيل</a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card apartment-card">
                        <img src="https://via.placeholder.com/300x200?text=شقة+مفروشة" class="card-img-top" alt="شقة مفروشة">
                        <div class="card-body">
                            <h5 class="card-title">شقة مفروشة في الإسكندرية</h5>
                            <p class="card-text text-muted">سموحة، الإسكندرية</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="fw-bold">3000 ج.م/شهر</span>
                                <a href="/apartments/3" class="btn btn-outline-primary">التفاصيل</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="footer">
            <div class="container text-center">
                <p>&copy; 2025 سكن طالب. جميع الحقوق محفوظة.</p>
            </div>
        </footer>
    </body>
    </html>
    """
    return html

@app.route('/apartments/<int:id>')
def apartment_detail(id):
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تفاصيل الشقة - سكن طالب</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
        <style>
            body {
                font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
                background-color: #f8f9fa;
            }
            .footer {
                background-color: #343a40;
                color: white;
                padding: 2rem 0;
                margin-top: 3rem;
            }
        </style>
    </head>
    <body>
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
                            <a class="nav-link active" href="/apartments">الشقق</a>
                        </li>
                    </ul>
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/login">تسجيل الدخول</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="container py-5">
            <div class="row">
                <div class="col-md-8">
                    <img src="https://via.placeholder.com/800x400?text=شقة+فاخرة" class="img-fluid rounded mb-4" alt="شقة فاخرة">
                    
                    <h1 class="mb-3">شقة فاخرة قرب جامعة القاهرة</h1>
                    <p class="text-muted mb-4">الجيزة، القاهرة</p>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">وصف الشقة</h5>
                            <p class="card-text">شقة مفروشة بالكامل قريبة من الجامعة، مناسبة للطلاب. تتميز بموقعها المميز على بعد 10 دقائق سيراً من جامعة القاهرة. الشقة مجهزة بالكامل وتشمل جميع الأثاث والأجهزة الكهربائية اللازمة.</p>
                        </div>
                    </div>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">المميزات</h5>
                            <div class="row">
                                <div class="col-md-6">
                                    <ul>
                                        <li>إنترنت واي فاي</li>
                                        <li>تكييف</li>
                                        <li>مطبخ مجهز</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <ul>
                                        <li>مفروشة بالكامل</li>
                                        <li>حمام خاص</li>
                                        <li>شرفة</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">تفاصيل الإيجار</h5>
                            <div class="fs-3 fw-bold text-danger mb-3">2500 ج.م/شهر</div>
                            <p class="text-muted mb-3">التأمين: 2500 ج.م</p>
                            <p class="text-muted mb-3">الفواتير: مشمولة في الإيجار</p>
                            <hr>
                            <h5 class="card-title">معلومات الاتصال</h5>
                            <p><strong>المالك:</strong> أحمد محمد</p>
                            <p><strong>الهاتف:</strong> 01012345678</p>
                            <div class="d-grid gap-2">
                                <a href="#" class="btn btn-primary">اتصل الآن</a>
                                <a href="#" class="btn btn-success">تواصل عبر واتساب</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="footer">
            <div class="container text-center">
                <p>&copy; 2025 سكن طالب. جميع الحقوق محفوظة.</p>
            </div>
        </footer>
    </body>
    </html>
    """
    return html

@app.route('/login')
def login():
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تسجيل الدخول - سكن طالب</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
        <style>
            body {
                font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
                background-color: #f8f9fa;
                height: 100vh;
                display: flex;
                align-items: center;
            }
            .login-card {
                border-radius: 10px;
                box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                padding: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card login-card">
                        <div class="card-body">
                            <h2 class="text-center mb-4">تسجيل الدخول</h2>
                            <form>
                                <div class="mb-3">
                                    <label for="username" class="form-label">اسم المستخدم</label>
                                    <input type="text" class="form-control" id="username" required>
                                </div>
                                <div class="mb-3">
                                    <label for="password" class="form-label">كلمة المرور</label>
                                    <input type="password" class="form-control" id="password" required>
                                </div>
                                <div class="mb-3 form-check">
                                    <input type="checkbox" class="form-check-input" id="remember">
                                    <label class="form-check-label" for="remember">تذكرني</label>
                                </div>
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary">تسجيل الدخول</button>
                                </div>
                            </form>
                            <div class="text-center mt-3">
                                <a href="/">العودة للصفحة الرئيسية</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')