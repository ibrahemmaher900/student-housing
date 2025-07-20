#!/usr/bin/env bash
# exit on error
set -o errexit

# Run diagnostics script
python render_debug.py

# Print environment information
echo "Python version:"
python --version
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Install dependencies
pip install -r requirements.txt

# Print Python path for debugging
echo "Python path:"
python -c "import sys; print(sys.path)"

# Check if Django is installed correctly
echo "Checking Django installation:"
python -c "import django; print(f'Django version: {django.__version__}')"

# Check if settings module can be imported
echo "Checking settings module:"
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings'); import django; django.setup(); from django.conf import settings; print(f'Debug mode: {settings.DEBUG}')"

# Collect static files
echo "Collecting static files:"
python manage.py collectstatic --no-input

# Apply migrations
echo "Applying migrations:"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Check if migrations were applied correctly
echo "Checking database tables:"
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings'); import django; django.setup(); from django.db import connection; print('Tables in database:', connection.introspection.table_names())"

# Run database initialization script
echo "Running database initialization script:"
python init_database.py

# Create default data
echo "Creating default data:"
python init_default_data.py

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file"
    echo "DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
    echo "DJANGO_DEBUG=True" >> .env
    echo "DJANGO_ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1" >> .env
fi

echo "Build completed successfully"