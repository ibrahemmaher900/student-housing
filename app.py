import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from django.core.wsgi import get_wsgi_application
    
    logger.info("Setting DJANGO_SETTINGS_MODULE to student_housing.settings")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
    
    logger.info("Initializing WSGI application")
    application = get_wsgi_application()
    app = application  # Gunicorn is looking for 'app'
    
    logger.info("WSGI application initialized successfully")
except Exception as e:
    logger.error(f"Error initializing WSGI application: {e}", exc_info=True)
    raise