from pydantic import BaseModel
from typing import Optional, List
from app.schemas.post import Post

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True

class Category(CategoryInDB):
    posts: Optional[List[Post]] = []
    
    class Config:
        orm_mode = True
