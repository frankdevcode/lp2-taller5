from app.database.database import engine, Base
from app.models import user, post, category, comment, tag

def create_tables():
    """Crea todas las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)
