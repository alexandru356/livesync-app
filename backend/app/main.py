from fastapi import FastAPI
from models import Base, engine, get_db
from routes import user_router, document_router


# FastAPI app initialization, database setup, and app start
app = FastAPI()

#SQLite setup
DATABASE_URL = "sqlite:///./test.db" 

# SQLAlchemy setup
Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(document_router, prefix="/documents", tags=["documents"])

@app.get("/")
async def root():
    return {"message" : "Welcome to livesync API"}
