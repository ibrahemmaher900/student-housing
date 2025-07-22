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

# Check if student_housing directory exists
student_housing_path = os.path.join(project_path, 'student_housing')
if os.path.exists(student_housing_path):
    logger.info(f"student_housing directory exists: {os.listdir(student_housing_path)}")
else:
    logger.error("student_housing directory does not exist")

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
    
    # Create a simple HTML page
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>سكن طالب</title>
        <style>
            body {
                font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                text-align: center;
            }
            header {
                background-color: #dc3545;
                color: white;
                padding: 2rem;
            }
            h1 {
                margin: 0;
                font-size: 2.5rem;
            }
            main {
                flex: 1;
                padding: 2rem;
                max-width: 800px;
                margin: 0 auto;
            }
            footer {
                background-color: #343a40;
                color: white;
                padding: 1rem;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>سكن طالب</h1>
            <p>منصة لمساعدة الطلاب في العثور على سكن قريب من جامعاتهم</p>
        </header>
        <main>
            <h2>مرحباً بك في موقع سكن طالب</h2>
            <p>نعمل حالياً على تطوير الموقع ليكون جاهزاً قريباً</p>
        </main>
        <footer>
            <p>جميع الحقوق محفوظة &copy; 2025 سكن طالب</p>
        </footer>
    </body>
    </html>
    """
    
    # Fallback to a simple app if Django fails
    def app(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [html.encode('utf-8')]
