#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"

# Install dependencies
pip install django django-allauth whitenoise gunicorn requests

# Collect static files
python manage.py collectstatic --noinput || echo "Collectstatic failed"

# Apply migrations
python manage.py migrate || echo "Migrate failed"

echo "Build completed"
