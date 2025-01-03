from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from models import User, Document, get_db
from auth import create_access_token, get_current_user, bcrypt_context, authenticate_user
from schemas import UserCreate, UserResponse, DocumentCreate, DocumentResponse, Token, Login
from typing import List

user_router = APIRouter()


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

@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail = f"ID {user_id} : Does not exist")
    user_model.email = user.email
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@user_router.delete("/{user_id}", response_model = None)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail = f"ID {user_id} : Does not exist")

    db.delete(user_model)
    db.commit()

    #return the deleted user id with confirmation msg
    return {"message": f"User with ID {user_id} has been deleted successfully"}



document_router = APIRouter()

@document_router.post("/", response_model=DocumentResponse)
async def create_document(document: DocumentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_document = Document(
        title=document.title, 
        content=document.content, 
        creator=current_user
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@document_router.get("/{document_id}", response_model = DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):

    document_model = db.query(Document).filter(Document.id == document_id).first()
    if document_model is None:
        raise HTTPException(status_code=404, detail=f"Document : {document_id} not found")
    return document_model

@document_router.put("/{document_id}", response_model = DocumentResponse)
async def update_document(document_id: int,document: DocumentCreate ,db: Session = Depends(get_db)):
    document_model = db.query(Document).filter(Document.id == document_id).first()

    if document_model is None:
        raise HTTPException(status_code=404, detail = f"ID {document_id} : Does not exist")
    
    document_model.title = document.title
    document_model.content = document.content
  
    db.add(document_model)
    db.commit()
    db.refresh(document_model)

    return document_model

@document_router.delete("/{document_id}", response_model=None)
async def delete_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_model = db.query(Document).filter(Document.id == document_id).first()
    if document_model is None:
        raise HTTPException(status_code=404, detail = f"Document ID {document_id} : Does not exist")
    if document_model.creator_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    db.delete(document_model)
    db.commit()

    return {"message: " f"Document with ID {document_id} has been deleted successfully"}

@document_router.get("/user/{user_id}", response_model=List[DocumentResponse])
async def get_documents_by_user(user_id: int, db: Session = Depends(get_db)):
    documents = db.query(Document).filter(Document.creator_id == user_id).all()
    return documents

auth_router = APIRouter()

@auth_router.post("/signup", response_model=UserResponse)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt_context.hash(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@auth_router.post("/signin", response_model=Token)
async def sign_in(login: Login, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, login.email, login.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(email=db_user.email, user_id=db_user.id, expires_delta=timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/users/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user