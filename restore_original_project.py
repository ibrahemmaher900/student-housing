#!/usr/bin/env python
import os
import shutil
import subprocess

# تأكد من أن المشروع في الحالة الأصلية
print("استعادة المشروع الأصلي...")

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

# تعديل ملف settings.py ليكون مثل الإعدادات المحلية
settings_content = """import os
import secrets
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import environ
import dj_database_url

# Initialize environ
env = environ.Env()
# Read .env file if it exists
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable for SECRET_KEY in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-key-for-development-only')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,.onrender.com').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'corsheaders',
    'csp',
    'axes',
    
    # Local apps
    'apartments',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'student_housing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apartments.context_processors.notifications_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'student_housing.wsgi.application'

# Database
# Always use DATABASE_URL if available (for Render PostgreSQL)
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
    print(f"Using database from DATABASE_URL: {DATABASES['default']['ENGINE']}")
else:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }
    print(f"Using SQLite database at: {DATABASES['default']['NAME']}")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# django-allauth settings
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Temporarily disable social providers
SOCIALACCOUNT_PROVIDERS = {}
"""

with open('student_housing/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings_content)
    print("تم تعديل ملف settings.py ليكون مثل الإعدادات المحلية")

# تعديل ملف app.py ليستخدم wsgi.py الأصلي
app_content = """\"\"\"
WSGI app for student_housing project.
\"\"\"
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

# Create sample data
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
import django
django.setup()
from django.contrib.auth.models import User
from apartments.models import University, Apartment
from users.models import Profile
from decimal import Decimal

# Create universities
if University.objects.count() == 0:
    print('Creating universities...')
    universities = [
        University.objects.create(name='جامعة القاهرة', city='القاهرة'),
        University.objects.create(name='جامعة عين شمس', city='القاهرة'),
        University.objects.create(name='جامعة الإسكندرية', city='الإسكندرية')
    ]
else:
    universities = list(University.objects.all())
    print(f'Using existing universities: {len(universities)}')

# Create owner
owner = User.objects.filter(username='owner').first()
if not owner:
    print('Creating owner user...')
    owner = User.objects.create_user('owner', 'owner@example.com', 'password123')
    Profile.objects.filter(user=owner).update(user_type='owner')

# Create apartments
if Apartment.objects.count() == 0:
    print('Creating apartments...')
    apartments = [
        {
            'title': 'شقة فاخرة قرب جامعة القاهرة',
            'description': 'شقة مفروشة بالكامل قريبة من الجامعة، مناسبة للطلاب',
            'price': Decimal('2500.00'),
            'deposit': Decimal('2500.00'),
            'city': 'القاهرة',
            'district': 'الجيزة',
            'address': 'شارع الجامعة، الجيزة',
            'rooms': 3,
            'area': Decimal('120.00'),
            'floor': 2,
            'furnished': True,
            'gender': 'mixed',
            'payment_method': 'monthly',
            'bills_included': True,
            'available': True,
            'university': universities[0],
            'owner': owner,
            'contact_name': 'أحمد محمد',
            'phone': '01012345678',
            'whatsapp_available': True,
            'advertiser_type': 'owner',
            'has_wifi': True,
            'has_ac': True,
            'has_fridge': True,
            'has_washer': True,
            'has_kitchen': True,
            'has_private_bathroom': True,
            'apartment_type': 'apartment'
        }
    ]
    
    for data in apartments:
        try:
            Apartment.objects.create(**data)
            print(f'Created apartment: {data[\"title\"]}')
        except Exception as e:
            print(f'Error creating apartment: {e}')
else:
    print(f'Using existing apartments: {Apartment.objects.count()}')
"

echo "Build completed"
"""

with open('build.sh', 'w', encoding='utf-8') as f:
    f.write(build_content)
    os.chmod('build.sh', 0o755)
    print("تم تعديل ملف build.sh ليكون بسيطًا وفعالًا")

# تعديل ملف render.yaml
render_content = """services:
  - type: web
    name: student-housing
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn app:app"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "True"
      - key: ALLOWED_HOSTS
        value: ".onrender.com,localhost,127.0.0.1"
      - key: DJANGO_SETTINGS_MODULE
        value: "student_housing.settings"
    plan: free
"""

with open('render.yaml', 'w', encoding='utf-8') as f:
    f.write(render_content)
    print("تم تعديل ملف render.yaml")

print("تم استعادة المشروع الأصلي بنجاح")
