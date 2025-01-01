from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# SQLite setup
DATABASE_URL = "sqlite:///./test.db" 

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

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
    #key that links session to the document thats being edited
    document_id = Column(Integer, ForeignKey("documents.id"))
    #relationship showing which document is being worked on
    document = relationship("Document", back_populates="sessions")
    #relationship to users involved in the collaboration session
    users = relationship("User", secondary="session_users")  

class SessionUser(Base):
    __tablename__ = "session_users"
    
    session_id = Column(Integer, ForeignKey("collaboration_sessions.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)