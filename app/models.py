from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from .database import Base

# Modelos SQLAlchemy para la base de datos
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    country = Column(String)
    
    classes = relationship("ClassDB", back_populates="user")

class ClassDB(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    grade = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("UserDB", back_populates="classes")

# Modelos Pydantic para la API
class UserBase(BaseModel):
    name: str
    email: str
    age: int
    country: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class ClassBase(BaseModel):
    name: str
    grade: float

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True