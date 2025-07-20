import os
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
# Temporarily enable debug for troubleshooting
DEBUG = True

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

# إضافة وسائط إضافية في بيئة الإنتاج فقط
# لتجنب المشاكل في بيئة التطوير
if not DEBUG:
    # إضافة WhiteNoise لخدمة الملفات الثابتة
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    # إضافة CSP لسياسة أمان المحتوى
    MIDDLEWARE.insert(5, 'csp.middleware.CSPMiddleware')
    # إضافة وسيط الأمان المخصص
    MIDDLEWARE.append('student_housing.security_middleware.SecurityMiddleware')

# Security Middleware settings
if not DEBUG:  # تطبيق إعدادات الأمان فقط في بيئة الإنتاج
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override database settings with DATABASE_URL environment variable if available
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    print(f"Using database: {DATABASES['default']['ENGINE']}")
else:
    print("Using SQLite database")
    # Make sure the SQLite database file is in a writable location
    db_path = BASE_DIR / 'db.sqlite3'
    print(f"SQLite database path: {db_path}")
    print(f"Directory exists: {os.path.exists(os.path.dirname(db_path))}")
    print(f"Directory is writable: {os.access(os.path.dirname(db_path), os.W_OK)}")
    DATABASES['default']['NAME'] = db_path

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'users.password_validation.PasswordValidator',
        'OPTIONS': {
            'min_length': 10,
        }
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
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # تغيير إلى 'mandatory' في بيئة الإنتاج

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'picture',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
    }
}

# Map Settings
MAP_SETTINGS = {
    'default_lat': 24.7136,  # Default latitude (Saudi Arabia)
    'default_lng': 46.6753,  # Default longitude (Saudi Arabia)
    'default_zoom': 10,      # Default zoom level
}

# Security Settings

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://maps.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com", "https://cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "https://maps.googleapis.com", "https://maps.gstatic.com")
CSP_CONNECT_SRC = ("'self'",)

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:8000',
    'http://127.0.0.1:8000',
])
CORS_ALLOW_CREDENTIALS = True

# Django Axes Settings (Login Security)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
AXES_FAILURE_LIMIT = 5  # Number of login attempts before lockout
AXES_LOCKOUT_TIME = 1  # Lockout time in hours
AXES_RESET_ON_SUCCESS = True  # Reset failed login attempts on successful login

# Email settings
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@studenthousing.com')

# Whitenoise settings for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Session settings
SESSION_COOKIE_AGE = 3600  # 1 hour in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True