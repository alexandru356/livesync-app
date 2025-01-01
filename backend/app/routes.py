from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User, Document, get_db
from schemas import UserCreate, UserResponse, DocumentCreate, DocumentResponse
from typing import List

user_router = APIRouter()

@user_router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  

@user_router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users  
@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user  


document_router = APIRouter()

@document_router.post("/", response_model=DocumentResponse)
async def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    db_document = Document(title=document.title, content=document.content, creator_id=document.creator_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document