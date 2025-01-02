from pydantic import BaseModel
from typing import List, Optional

# User Pydantic schema
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

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
    creator : UserResponse
    
    class Config:
        orm_mode = True  

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    email: str
    password: str

class SignUp(BaseModel):
    email: str
    password: str