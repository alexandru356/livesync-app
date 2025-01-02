from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext


# SQLite setup
DATABASE_URL = "sqlite:///./livesync.db" 

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#hashing password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy database models


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    #relationship to documents created by this user
    documents = relationship("Document", back_populates="creator")
    #relationship to sessions the user is part of
    sessions = relationship("CollaborationSession", secondary="session_users")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    
    #key that links document to user who created it
    creator_id = Column(Integer, ForeignKey("users.id"))
    #relationship back to user model to get creators detail
    creator = relationship("User", back_populates="documents")
    #relationship to sessions where the document is being edited
    sessions = relationship("CollaborationSession", back_populates="document")

class CollaborationSession(Base):
    __tablename__ = "collaboration_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    #key that links session to the d# Hashing password before savingocument thats being edited
    document_id = Column(Integer, ForeignKey("documents.id"))
    #relationship showing which document is being worked on
    document = relationship("Document", back_populates="sessions")
    #relationship to users involved in the collaboration session
    users = relationship("User", secondary="session_users")  

class SessionUser(Base):
    __tablename__ = "session_users"
    
    session_id = Column(Integer, ForeignKey("collaboration_sessions.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_admin_user(db: Session):
    hashed_password = pwd_context.hash("CB9tu83t13")
    admin_exists = db.query(User).filter(User.id == 1).first()
    if not admin_exists:
        admin_user = User(
            id=1,
            name="Admin",
            email="alexandru356.c@gmail.com",
            password= hashed_password
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user created with ID 1")
    else:
        print("Admin user already exists")

def setup_db(db: Session):
    create_admin_user(db)
