from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.get_database_url

echo = False

# Crear el motor de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, echo=echo
)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base para los modelos
Base = declarative_base()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
