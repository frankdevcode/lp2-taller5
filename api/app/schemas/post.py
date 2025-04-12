from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.user import User

class PostBase(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None

class PostInDB(PostBase):
    id: int
    user_id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Post(PostInDB):
    user: Optional[User] = None
    
    class Config:
        orm_mode = True
