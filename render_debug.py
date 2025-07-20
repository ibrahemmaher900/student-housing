import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('render_debug')

def check_environment():
    """Check environment variables and paths"""
    logger.info("=== ENVIRONMENT DIAGNOSTICS ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Directory contents: {os.listdir('.')}")
    
    # Check important directories
    base_dir = Path(__file__).resolve().parent
    logger.info(f"Base directory: {base_dir}")
    logger.info(f"Base directory exists: {os.path.exists(base_dir)}")
    
    # Check for important files
    settings_path = os.path.join(base_dir, 'student_housing', 'settings.py')
    logger.info(f"Settings path: {settings_path}")
    logger.info(f"Settings file exists: {os.path.exists(settings_path)}")
    
    # Check environment variables
    logger.info(f"Environment variables: {list(os.environ.keys())}")
    logger.info(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    logger.info(f"DATABASE_URL: {'Set' if 'DATABASE_URL' in os.environ else 'Not set'}")
    
    # Check Python path
    logger.info(f"Python path: {sys.path}")

# Run diagnostics
check_environment()