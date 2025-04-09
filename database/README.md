# Componente de Base de Datos

Este componente utiliza PostgreSQL para almacenar los datos del blog.

## Estructura

- `Dockerfile`: Configuración para crear la imagen de Docker de PostgreSQL
- `init.sql`: Script SQL para inicializar la base de datos con las tablas necesarias y datos de ejemplo

## Tablas

- `users`: Almacena información de los usuarios
- `categories`: Categorías para las publicaciones
- `posts`: Publicaciones del blog
- `comments`: Comentarios en las publicaciones
- `tags`: Etiquetas para clasificar publicaciones
- `post_tags`: Relación muchos a muchos entre publicaciones y etiquetas
