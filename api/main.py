from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import posts, users, auth, categories, comments
from app.database.init_db import create_tables

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
app.include_router(auth.router, tags=["Autenticación"], prefix="/api")
app.include_router(users.router, tags=["Usuarios"], prefix="/api/users")
app.include_router(posts.router, tags=["Publicaciones"], prefix="/api/posts")
app.include_router(categories.router, tags=["Categorías"], prefix="/api/categories")
app.include_router(comments.router, tags=["Comentarios"], prefix="/api/comments")

@app.on_event("startup")
async def startup():
    # Crear tablas si no existen
    create_tables()

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a la API del Blog"}
