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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to use Django if available
    try:
        logger.info("Trying to use Django...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        app = application
        logger.info("Django WSGI application initialized successfully")
    except Exception as django_error:
        # Fallback to simple app if Django fails
        logger.warning(f"Django initialization failed: {django_error}")
        logger.info("Falling back to simple app...")
        from index import index
        
        def app(environ, start_response):
            """Simple WSGI application that serves the index page"""
            status = '200 OK'
            headers = [('Content-type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            return [index(None).content]
        
        application = app
        logger.info("Simple WSGI application initialized successfully")
except Exception as e:
    logger.error(f"Error initializing WSGI application: {e}", exc_info=True)
    raise