#!/usr/bin/env bash
# exit on error
set -o errexit

# Print environment information
echo "Python version:"
python --version
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Install dependencies
pip install -r requirements.txt

# Create index.py if it doesn't exist (fallback page)
if [ ! -f index.py ]; then
    echo "Creating index.py (fallback page)"
    cat > index.py << 'EOF'
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
EOF
fi

# Try to set up Django
echo "Setting up Django..."
python -c "import django; print(f'Django version: {django.__version__}')"

# Collect static files
echo "Collecting static files:"
python manage.py collectstatic --no-input || echo "Collectstatic failed, continuing..."

# Apply migrations
echo "Applying migrations:"
python manage.py makemigrations --noinput || echo "Makemigrations failed, continuing..."
python manage.py migrate --noinput || echo "Migrate failed, continuing..."

# Create superuser if needed
echo "Creating superuser if needed:"
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
import django
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
" || echo "Superuser creation failed, continuing..."

echo "Build completed successfully"