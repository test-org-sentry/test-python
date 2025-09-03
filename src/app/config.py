"""
Configuration settings for the test application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    
    # Sentry Configuration
    SENTRY_DSN = "https://962ef567507fd1e7459344e849417167@o4509872718544896.ingest.us.sentry.io/4509914005438464"
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/testdb')
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # External API Configuration
    EXTERNAL_API_BASE_URL = os.environ.get('EXTERNAL_API_BASE_URL', 'https://httpbin.org')
    
    # Application Settings
    MAX_RETRIES = int(os.environ.get('MAX_RETRIES', '3'))
    TIMEOUT_SECONDS = int(os.environ.get('TIMEOUT_SECONDS', '30'))
