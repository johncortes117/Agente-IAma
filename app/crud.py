from sqlalchemy.orm import Session
from . import models
import json

def get_user(db: Session, user_id: int):
    return db.query(models.UserDB).filter(models.UserDB.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def create_user(db: Session, user: models.UserCreate):
    try:
        db_user = models.UserDB(
            name=user.name,
            email=user.email,
            age=user.age,
            country=user.country,
            test_completed=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def save_test_response(db: Session, user_id: int, question_id: int, response: list):
    try:
        # Verificar si ya existe una respuesta para esta pregunta
        existing_response = db.query(models.TestResponseDB).filter(
            models.TestResponseDB.user_id == user_id,
            models.TestResponseDB.question_id == question_id
        ).first()
        
        if existing_response:
            # Actualizar respuesta existente
            existing_response.response = json.dumps(response)
            db.commit()
            return existing_response
            
        # Crear nueva respuesta
        db_response = models.TestResponseDB(
            user_id=user_id,
            question_id=question_id,
            response=json.dumps(response)
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        return db_response
    except Exception as e:
        db.rollback()
        raise Exception(f"Error al guardar la respuesta: {str(e)}")

def mark_test_completed(db: Session, user_id: int):
    try:
        user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
        if user:
            user.test_completed = True
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e

def get_user_test_responses(db: Session, user_id: int):
    try:
        responses = db.query(models.TestResponseDB).filter(
            models.TestResponseDB.user_id == user_id
        ).all()
        return responses
    except Exception as e:
        raise Exception(f"Error al obtener las respuestas: {str(e)}") 