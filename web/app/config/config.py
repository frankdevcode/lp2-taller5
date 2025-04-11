import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-predeterminada'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://bloguser:blogpassword@db:5432/blogdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    API_URL = os.environ.get('API_URL', 'http://localhost:8000')
    
    # Configuración de paginación
    POSTS_PER_PAGE = 10
    
    # Configuración de caché
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Configuración de sesión
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de seguridad
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'clave-csrf-predeterminada'

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dev.db'
    API_URL = os.environ.get('API_URL', 'http://localhost:8000')

class TestingConfig(Config):
    """Configuración para pruebas."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///test.db'
    API_URL = os.environ.get('API_URL', 'http://localhost:8000')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    API_URL = os.environ.get('API_URL', 'http://api:8000')
    
    # Configuración de seguridad adicional para producción
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}