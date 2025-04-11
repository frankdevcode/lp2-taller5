import requests
from flask import current_app
from functools import wraps
from requests.exceptions import RequestException

def get_api_url(endpoint):
    """Construye la URL completa para un endpoint de la API."""
    return f"{current_app.config['API_URL']}/api/v1{endpoint}"

def handle_api_error(func):
    """Decorador para manejar errores de la API."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestException as e:
            current_app.logger.error(f"Error en la API: {str(e)}")
            return None
    return wrapper

@handle_api_error
def fetch_posts(page=1, per_page=None):
    """Obtiene posts de la API con paginación."""
    if per_page is None:
        per_page = current_app.config['POSTS_PER_PAGE']
    
    response = requests.get(
        get_api_url('/posts'),
        params={'skip': (page - 1) * per_page, 'limit': per_page}
    )
    response.raise_for_status()
    return response.json()

@handle_api_error
def fetch_post_by_slug(slug):
    """Obtiene un post por su slug."""
    response = requests.get(get_api_url(f'/posts/slug/{slug}'))
    response.raise_for_status()
    return response.json()

def format_date(date_str):
    """Formatea una fecha para mostrarla en la interfaz."""
    from datetime import datetime
    try:
        date = datetime.fromisoformat(date_str)
        return date.strftime('%d de %B de %Y')
    except (ValueError, TypeError):
        return date_str 