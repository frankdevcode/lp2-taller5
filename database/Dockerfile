FROM postgres:14-alpine

# Copiar scripts de inicialización
COPY docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/

# Configuración de PostgreSQL
ENV POSTGRES_USER=bloguser
ENV POSTGRES_PASSWORD=blogpassword
ENV POSTGRES_DB=blogdb

# Exponer el puerto
EXPOSE 5432
