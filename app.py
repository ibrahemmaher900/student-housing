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
    raise