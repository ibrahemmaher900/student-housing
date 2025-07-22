"""
WSGI app for student_housing project.
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('app')

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

try:
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
    
    # Import Django WSGI application
    from django.core.wsgi import get_wsgi_application
    
    # Get the application
    application = get_wsgi_application()
    app = application  # For Gunicorn
    
    logger.info("Django WSGI application initialized successfully")
except Exception as e:
    logger.error(f"Error initializing WSGI application: {e}", exc_info=True)
    
    # Fallback to a simple app if Django fails
    def app(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [b"<h1>\u0633\u0643\u0646 \u0637\u0627\u0644\u0628</h1><p>\u062d\u062f\u062b \u062e\u0637\u0623 \u0641\u064a \u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0645\u0648\u0642\u0639. \u064a\u0631\u062c\u0649 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0644\u0627\u062d\u0642\u064b\u0627.</p>"]
