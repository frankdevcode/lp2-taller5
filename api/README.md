# API del Blog con FastAPI

Este componente implementa la API RESTful para el blog utilizando FastAPI y SQLAlchemy.

## Estructura

- `main.py`: Punto de entrada de la aplicación FastAPI
- `app/`: Directorio principal de la aplicación
  - `core/`: Configuración y utilidades centrales
    - `config.py`: Configuración de la aplicación
    - `security.py`: Funciones de autenticación y seguridad
  - `database/`: Configuración de la base de datos
    - `database.py`: Configuración de SQLAlchemy
    - `init_db.py`: Inicialización de la base de datos
  - `models/`: Modelos SQLAlchemy para las tablas de la base de datos
  - `schemas/`: Esquemas Pydantic para validación de datos
  - `routers/`: Endpoints de la API organizados por entidad

## Endpoints

La API proporciona los siguientes endpoints:

### Autenticación
- `POST /api/login`: Obtener token de acceso

### Usuarios
- `POST /api/users/`: Crear un nuevo usuario
- `GET /api/users/`: Obtener lista de usuarios
- `GET /api/users/me`: Obtener información del usuario actual
- `GET /api/users/{user_id}`: Obtener información de un usuario específico
- `PUT /api/users/{user_id}`: Actualizar información de un usuario
- `DELETE /api/users/{user_id}`: Eliminar un usuario

### Publicaciones
- `POST /api/posts/`: Crear una nueva publicación
- `GET /api/posts/`: Obtener lista de publicaciones
- `GET /api/posts/{post_id}`: Obtener información de una publicación específica
- `PUT /api/posts/{post_id}`: Actualizar una publicación
- `DELETE /api/posts/{post_id}`: Eliminar una publicación

### Categorías
- `POST /api/categories/`: Crear una nueva categoría
- `GET /api/categories/`: Obtener lista de categorías
- `GET /api/categories/{category_id}`: Obtener información de una categoría específica
- `PUT /api/categories/{category_id}`: Actualizar una categoría
- `DELETE /api/categories/{category_id}`: Eliminar una categoría

### Comentarios
- `POST /api/comments/`: Crear un nuevo comentario
- `GET /api/comments/`: Obtener lista de comentarios
- `GET /api/comments/{comment_id}`: Obtener información de un comentario específico
- `PUT /api/comments/{comment_id}`: Actualizar un comentario
- `DELETE /api/comments/{comment_id}`: Eliminar un comentario

## Ejecución

Para ejecutar la API en modo desarrollo:

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

Para ejecutar con Docker:

```bash
docker-compose up -d api
```

## Documentación

La documentación interactiva de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
