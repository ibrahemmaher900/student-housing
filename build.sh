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
pip install requests django-allauth whitenoise gunicorn dj-database-url django-cors-headers django-csp django-axes

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

echo "Build completed successfully"
