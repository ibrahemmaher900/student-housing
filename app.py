"""
WSGI app for student_housing project.
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')

# Import Django WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    app = application  # For Gunicorn
    logger.info("Django application loaded successfully")
except Exception as e:
    logger.error(f"Error loading Django application: {e}")
    raise
