#!/usr/bin/env python
import os
import shutil

# قائمة بالملفات غير الضرورية التي يجب حذفها
unnecessary_files = [
    'apartments/views_debug.py',
    'apartments/views_fix.py',
    'apartments/views_safe.py',
    'apartments/views_simple.py',
    'apartments/views_static.py',
    'apartments/views_try.py',
    'apartments/simple_rating_view.py',
    'apartments/views_rating_fix.py',
    'fix_currency.py',
    'fix_nan_stats.py',
    'fix_profile_links.py',
    'fix_rating.py',
    'templates/base/base_fix.py',
    'templates/base/base_simple.html',
    'users/views_auth_pro.py',
    'users/views_login_fix.py',
    'users/views_logout.py',
    'users/views_register_fix.py',
    'users/forms_fix.py',
    'add_social_apps.py',
    'create_apartments_page.py',
]

# حذف الملفات غير الضرورية
for file_path in unnecessary_files:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"تم حذف {file_path}")

# إعادة ملف urls.py الرئيسي إلى الحالة الأصلية
urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apartments.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('apartments/', include('apartments.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
]

# Add static and media URLs
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

with open('student_housing/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)
    print("تم إعادة ملف urls.py الرئيسي إلى الحالة الأصلية")

# تعديل ملف app.py ليستخدم wsgi.py الأصلي
app_content = """"""
WSGI app for student_housing project.
"""
import os
import sys

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application  # For Gunicorn
"""

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)
    print("تم تعديل ملف app.py ليستخدم wsgi.py الأصلي")

# تعديل ملف build.sh ليكون بسيطًا وفعالًا
build_content = """#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"

# Install dependencies
pip install django django-allauth django-environ whitenoise pillow gunicorn dj-database-url django-cors-headers django-csp django-axes requests PyJWT cryptography oauthlib python3-openid requests-oauthlib psycopg2-binary

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser if not exists
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
"

echo "Build completed"
"""

with open('build.sh', 'w', encoding='utf-8') as f:
    f.write(build_content)
    os.chmod('build.sh', 0o755)
    print("تم تعديل ملف build.sh ليكون بسيطًا وفعالًا")

print("تم تنظيف المشروع بنجاح")
