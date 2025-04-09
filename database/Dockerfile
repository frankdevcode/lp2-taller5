FROM postgres:14

# Variables de entorno para configurar la base de datos
ENV POSTGRES_USER=bloguser
ENV POSTGRES_PASSWORD=blogpassword
ENV POSTGRES_DB=blogdb

# Copiar script de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto de PostgreSQL
EXPOSE 5432
