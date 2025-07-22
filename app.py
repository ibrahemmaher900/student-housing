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
    # Use the original wsgi.py file
    from student_housing.wsgi import application
    app = application  # For Gunicorn
    logger.info("Django application loaded successfully from wsgi.py")
except Exception as e:
    logger.error(f"Error loading Django application: {e}")
    raise
