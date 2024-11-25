from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import crud, models
from app.database import engine, get_db
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Rutas para las páginas
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/users")
async def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = crud.create_user(db=db, user=user)
        return {"id": new_user.id, "email": new_user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/test/response")
async def save_test_response(
    response: dict,
    db: Session = Depends(get_db)
):
    try:
        # Validar que todos los campos necesarios estén presentes
        if not all(k in response for k in ["user_id", "question_id", "response"]):
            raise HTTPException(
                status_code=400, 
                detail="Faltan campos requeridos en la respuesta"
            )
            
        return crud.save_test_response(
            db=db,
            user_id=response["user_id"],
            question_id=response["question_id"], 
            response=response["response"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/test/complete/{user_id}")
async def complete_test(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        success = crud.mark_test_completed(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chat")
async def chat(message: dict):
    try:
        from app.chatbot import llama_chat
        
        # Obtener el historial completo de mensajes
        messages = message.get("messages", [])
        
        try:
            response = llama_chat(messages)
            return {"response": response}
        except Exception as e:
            print(f"Error en llama_chat: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Error al procesar el mensaje: {str(e)}"
            )
            
    except Exception as e:
        print(f"Error general en /api/chat: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno del servidor"
        )

@app.get("/api/users/{user_id}/test-status")
async def get_test_status(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"test_completed": user.test_completed}

@app.get("/api/users/{user_id}/test-responses")
async def get_user_test_responses(user_id: int, db: Session = Depends(get_db)):
    try:
        responses = crud.get_user_test_responses(db, user_id)
        # Convertir las respuestas a un formato más amigable
        formatted_responses = []
        for resp in responses:
            formatted_responses.append({
                "question_id": resp.question_id,
                "response": json.loads(resp.response)
            })
        return formatted_responses
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))