from typing import Annotated
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Base, engine, get_db
from routes import user_router, document_router
import auth


# FastAPI app initialization, database setup, and app start
app = FastAPI()


app.add_middleware(
     CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


#SQLite setup
DATABASE_URL = "sqlite:///./livesync.db" 

# SQLAlchemy setup
Base.metadata.create_all(bind=engine)
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(document_router, prefix="/documents", tags=["documents"])
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message" : "Welcome to livesync API"}
