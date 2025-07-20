#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Print Python path for debugging
python -c "import sys; print(sys.path)"

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate