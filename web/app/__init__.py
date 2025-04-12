from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os

# Inicializar extensiones
db = SQLAlchemy()
cache = Cache()

def create_app(config_name='development'):
    """Factory para crear la aplicación Flask."""
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://bloguser:blogpassword@db:5432/blogdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    cache.init_app(app)
    
    # Registrar blueprints
    from . import blog, auth
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    
    # Función para verificar si el usuario está autenticado
    @app.context_processor
    def inject_user():
        from flask import session
        return {'user': session.get('username'), 'is_admin': session.get('is_admin', False)}
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)