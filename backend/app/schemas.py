from pydantic import BaseModel
from typing import List, Optional

# User Pydantic schema
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True  #tells Pydantic to treat SQLAlchemy models like dictionaries

# Document Pydantic schema
class DocumentBase(BaseModel):
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True  
