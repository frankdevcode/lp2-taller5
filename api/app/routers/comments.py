from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.security import get_current_active_user
from app.database.database import get_db
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import Comment as CommentSchema, CommentCreate, CommentUpdate

router = APIRouter()

@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crea un nuevo comentario."""
    # Verificar si la publicación existe
    db_post = db.query(Post).filter(Post.id == comment.post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Crear nuevo comentario
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/", response_model=List[CommentSchema])
def read_comments(
    skip: int = 0,
    limit: int = 100,
    post_id: int = None,
    db: Session = Depends(get_db)
):
    """Obtiene la lista de comentarios, opcionalmente filtrados por publicación."""
    if post_id:
        comments = db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
    else:
        comments = db.query(Comment).offset(skip).limit(limit).all()
    return comments

@router.get("/{comment_id}", response_model=CommentSchema)
def read_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene información de un comentario específico."""
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentario no encontrado"
        )
    return db_comment

@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualiza un comentario."""
    # Verificar si el comentario existe
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentario no encontrado"
        )
    
    # Verificar permisos
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este comentario"
        )
    
    # Actualizar campos
    if comment.content is not None:
        db_comment.content = comment.content
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Elimina un comentario."""
    # Verificar si el comentario existe
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentario no encontrado"
        )
    
    # Verificar permisos
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este comentario"
        )
    
    # Eliminar comentario
    db.delete(db_comment)
    db.commit()
    return None
