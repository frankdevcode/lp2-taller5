from pydantic_settings import BaseSettings
import os
from typing import Optional

class Settings(BaseSettings):
    # Configuración de la API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Blog API"

    # Configuración de la base de datos
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "bloguser"
    POSTGRES_PASSWORD: str = "blogpassword"
    POSTGRES_DB: str = "blogdb"
    SQLALCHEMY_DATABASE_URI: str = "postgresql://bloguser:blogpassword@db:5432/blogdb"

    # Configuración de seguridad
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

    @property
    def get_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    def __init__(self):
        super().__init__()
        self.SQLALCHEMY_DATABASE_URI = self.get_database_url

settings = Settings()
