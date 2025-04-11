from flask import Flask
from config.base import Config
from models.database import db
from routes.main import bp
from routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(bp)
    app.register_blueprint(health_bp)

    return app
