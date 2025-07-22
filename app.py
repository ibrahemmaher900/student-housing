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

# Log debug information
logger.info(f"Project path: {project_path}")
logger.info(f"Directory contents: {os.listdir(project_path)}")

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
    
    # Simple fallback application
    def app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, response_headers)
        return [b"<h1>Student Housing</h1><p>We're experiencing technical difficulties. Please try again later.</p>"]
