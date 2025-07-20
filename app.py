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
    # Import the index function
    from index import index
    
    # Define a simple WSGI application
    def app(environ, start_response):
        """Simple WSGI application that serves the index page"""
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        
        # Return the index page
        return [index(None).content]
    
    # For compatibility with gunicorn
    application = app
    
    logger.info("WSGI application initialized successfully")
except Exception as e:
    logger.error(f"Error initializing WSGI application: {e}", exc_info=True)
    raise