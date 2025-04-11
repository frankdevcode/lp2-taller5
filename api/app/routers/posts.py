from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.security import get_current_active_user
from app.database.database import get_db
from app.models.user import User
from app.models.post import Post
from app.schemas.post import Post as PostSchema, PostCreate, PostUpdate

router = APIRouter()

@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crea una nueva publicación."""
    db_post = Post(
        title=post.title,
        content=post.content,
        category_id=post.category_id,
        user_id=current_user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostSchema])
def read_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtiene la lista de publicaciones."""
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostSchema)
def read_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene información de una publicación específica."""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    return db_post

@router.get("/slug/{slug}", response_model=PostSchema)
def read_post_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Obtiene información de una publicación por su slug."""
    db_post = db.query(Post).filter(Post.slug == slug).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    return db_post

@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualiza una publicación."""
    # Verificar si la publicación existe
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Verificar permisos
    if db_post.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar esta publicación"
        )
    
    # Actualizar campos
    if post.title is not None:
        db_post.title = post.title
    if post.content is not None:
        db_post.content = post.content
    if post.category_id is not None:
        db_post.category_id = post.category_id
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Elimina una publicación."""
    # Verificar si la publicación existe
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Verificar permisos
    if db_post.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta publicación"
        )
    
    # Eliminar publicación
    db.delete(db_post)
    db.commit()
    return None
