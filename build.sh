#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "student_housing directory: $(ls -la student_housing)"

# Install dependencies
pip install django django-allauth whitenoise gunicorn requests

# Test Django setup
python -c "import django; print(f'Django version: {django.__version__}')"
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings'); import django; django.setup(); print('Django setup successful')" || echo "Django setup failed"

# Collect static files
python manage.py collectstatic --noinput || echo "Collectstatic failed"

# Apply migrations
python manage.py migrate || echo "Migrate failed"

echo "Build completed"
