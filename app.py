"""
WSGI app for student_housing project.
"""
import os
import sys

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application  # For Gunicorn
