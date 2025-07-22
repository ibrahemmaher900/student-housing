#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"

# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Install additional dependencies that might be missing
pip install django-environ django-allauth whitenoise gunicorn requests dj-database-url django-cors-headers django-csp django-axes

# Test Django setup
python -c "import django; print(f'Django version: {django.__version__}')"
python -c "import environ; print('django-environ installed successfully')"

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

echo "Build completed"
