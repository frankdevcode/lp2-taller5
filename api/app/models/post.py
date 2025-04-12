from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from slugify import slugify

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", backref="posts")
    category = relationship("Category", backref="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    # Método para generar un slug único a partir del título
    def generate_slug(self, session):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        
        while session.query(Post).filter(Post.slug == slug, Post.id != self.id).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug
