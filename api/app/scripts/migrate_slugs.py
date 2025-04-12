from sqlalchemy.orm import Session
from app.database.database import engine, get_db
from app.models.post import Post
import logging

logger = logging.getLogger(__name__)

def migrate_posts_slugs():
    """
    Migra los posts existentes que no tienen slug.
    Este script debe ejecutarse una sola vez después de añadir el campo slug al modelo.
    """
    logger.info("Iniciando migración de slugs para posts existentes")
    
    # Obtener una sesión de BD
    db = Session(engine)
    
    try:
        # Obtener todos los posts sin slug
        posts_sin_slug = db.query(Post).filter(Post.slug == None).all()
        
        if not posts_sin_slug:
            logger.info("No hay posts sin slug, la migración no es necesaria")
            return
            
        logger.info(f"Encontrados {len(posts_sin_slug)} posts sin slug")
        
        # Generar slugs para cada post
        for post in posts_sin_slug:
            post.slug = post.generate_slug(db)
            logger.info(f"Generado slug '{post.slug}' para el post ID {post.id}: '{post.title}'")
        
        # Guardar los cambios
        db.commit()
        logger.info("Migración de slugs completada con éxito")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error durante la migración de slugs: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    migrate_posts_slugs() 