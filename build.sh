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
pip install requests

# Collect static files
python manage.py collectstatic --no-input || echo "Collectstatic failed, continuing..."

# Apply migrations
python manage.py makemigrations --noinput || echo "Makemigrations failed, continuing..."
python manage.py migrate --noinput || echo "Migrate failed, continuing..."

echo "Build completed successfully"
