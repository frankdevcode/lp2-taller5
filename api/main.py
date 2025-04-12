from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import posts, users, auth, categories, comments, health
from app.database.init_db import create_tables
import logging
from app.scripts.migrate_slugs import migrate_posts_slugs

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blog API",
    description="API para el blog personal",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limitar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(health.router, prefix="/health", tags=["health"])

@app.on_event("startup")
async def startup():
    # Crear tablas si no existen
    logger.info("Iniciando aplicación y creando tablas si no existen")
    create_tables()
    
    # Migrar slugs para posts existentes
    logger.info("Ejecutando migración de slugs")
    migrate_posts_slugs()

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a la API del Blog"}
