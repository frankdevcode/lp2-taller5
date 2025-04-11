from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.user import User

class CommentBase(BaseModel):
    content: str
    post_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentInDB(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class Comment(CommentInDB):
    user: Optional[User] = None
    
    class Config:
        orm_mode = True
