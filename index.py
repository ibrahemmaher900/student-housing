from django.http import HttpResponse

def index(request):
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>سكن طالب</title>
        <style>
            body {
                font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                text-align: center;
            }
            header {
                background-color: #dc3545;
                color: white;
                padding: 2rem;
            }
            h1 {
                margin: 0;
                font-size: 2.5rem;
            }
            main {
                flex: 1;
                padding: 2rem;
                max-width: 800px;
                margin: 0 auto;
            }
            footer {
                background-color: #343a40;
                color: white;
                padding: 1rem;
                text-align: center;
            }
            .btn {
                display: inline-block;
                background-color: #dc3545;
                color: white;
                padding: 0.5rem 1rem;
                text-decoration: none;
                border-radius: 0.25rem;
                margin: 1rem;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>سكن طالب</h1>
            <p>منصة لمساعدة الطلاب في العثور على سكن قريب من جامعاتهم</p>
        </header>
        <main>
            <h2>مرحباً بك في موقع سكن طالب</h2>
            <p>نعمل حالياً على تطوير الموقع ليكون جاهزاً قريباً</p>
            <p>يمكنك الدخول إلى لوحة الإدارة من خلال الرابط أدناه</p>
            <a href="/admin/" class="btn">لوحة الإدارة</a>
        </main>
        <footer>
            <p>جميع الحقوق محفوظة &copy; 2025 سكن طالب</p>
        </footer>
    </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html; charset=utf-8")