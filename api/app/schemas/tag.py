from pydantic import BaseModel
from typing import Optional, List

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None

class TagInDB(TagBase):
    id: int
    
    class Config:
        orm_mode = True

class Tag(TagInDB):
    class Config:
        orm_mode = True
