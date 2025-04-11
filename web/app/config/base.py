import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://bloguser:blogpassword@db:5432/blogdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
