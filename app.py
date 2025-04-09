from flask import Flask, render_template
from config import Config
from models.database import db

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos
db.init_app(app)

# Importar rutas
from routes import main_routes

# Registrar blueprints
app.register_blueprint(main_routes)

@app.route('/')
def index():
  return render_template('index.html', title='Inicio')

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)