from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from .database import Base
from datetime import datetime

# Modelos SQLAlchemy
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    country = Column(String)
    test_completed = Column(Boolean, default=False)
    
    responses = relationship("TestResponseDB", back_populates="user")

class TestResponseDB(Base):
    __tablename__ = "test_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer)
    response = Column(String)
    
    user = relationship("UserDB", back_populates="responses")

# Modelos Pydantic
class TestResponse(BaseModel):
    question_id: int
    response: List[str]

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    country: str

class User(UserCreate):
    id: int
    test_completed: bool = False

    class Config:
        from_attributes = True