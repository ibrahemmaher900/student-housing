#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"

# Install all dependencies
pip install django
pip install django-allauth
pip install django-environ
pip install whitenoise
pip install pillow
pip install gunicorn
pip install dj-database-url
pip install django-cors-headers
pip install django-csp
pip install django-axes
pip install requests
pip install PyJWT
pip install cryptography
pip install oauthlib
pip install python3-openid
pip install requests-oauthlib

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser
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
