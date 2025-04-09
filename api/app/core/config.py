from pydantic import BaseSettings
import os
from typing import Optional

class Settings(BaseSettings):
    # Configuración de la base de datos
    DATABASE_URL: str = "postgresql://bloguser:blogpassword@db:5432/blogdb"
    
    # Configuración de seguridad
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de la API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Blog API"

settings = Settings()
