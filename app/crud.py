from sqlalchemy.orm import Session
from . import models

def get_user(db: Session, user_id: int):
    return db.query(models.UserDB).filter(models.UserDB.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def create_user(db: Session, user: models.UserCreate):
    db_user = models.UserDB(
        name=user.name,
        email=user.email,
        age=user.age,
        country=user.country
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_class(db: Session, class_data: models.ClassCreate, user_id: int):
    db_class = models.ClassDB(**class_data.dict(), user_id=user_id)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class 